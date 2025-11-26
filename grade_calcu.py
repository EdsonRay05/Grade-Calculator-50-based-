import streamlit as st

def main():
    st.title("Grade Calculator")

    app_mode = st.sidebar.radio("Choose Option", [
        "Predict Major Exam Grade",
        "Calculate Overall Grade",
        "Calculate Class Standing"
    ])

    if app_mode == "Predict Major Exam Grade":
        predict_major_exam_grade()
    elif app_mode == "Calculate Overall Grade":
        calculate_overall_grade()
    elif app_mode == "Calculate Class Standing":
        calculate_class_standing()

    st.write("___")
    st.markdown("Developed by Edson Ray San Juan")


def grading_scheme(percent_score):
    # Official grading based on percentage
    if 99 <= percent_score <= 100:
        return (1.00, "Excellent")
    elif 96 <= percent_score < 99:
        return (1.25, "Superior")
    elif 93 <= percent_score < 96:
        return (1.50, "Meritorious")
    elif 90 <= percent_score < 93:
        return (1.75, "Very Good")
    elif 87 <= percent_score < 90:
        return (2.00, "Good")
    elif 84 <= percent_score < 87:
        return (2.25, "Very Satisfactory")
    elif 81 <= percent_score < 84:
        return (2.50, "Satisfactory")
    elif 78 <= percent_score < 81:
        return (2.75, "Fair")
    elif 75 <= percent_score < 78:
        return (3.00, "Passing")
    elif percent_score < 75:
        return (5.00, "Failed")
    else:
        return (4.00, "Incomplete")


def predict_major_exam_grade():
    st.header("Predict Major Exam Grade")
    desired_grade = st.number_input("Enter your desired grade (0-100):", min_value=0.0, max_value=100.0)
    grade_period = st.selectbox("Grade period:", ["Prelim", "Mid-Term", "Final"])
    noq = st.number_input("Enter your predicted number of exam questions:", min_value=1, step=1)

    if grade_period == "Prelim":
        prelim_class_standing = st.number_input("Enter the percentage of your class standing (0-100):", min_value=0.0, max_value=100.0)
        if st.button("Calculate needed Prelim exam score"):
            prelim_cs = prelim_class_standing * 0.5
            average = desired_grade - prelim_cs
            needed_score = (average / 0.5) * (noq / 100)
            if needed_score > noq:
                st.error(f"Cannot achieve {desired_grade} because Prelim Class Standing is too low.")
            else:
                st.success(f"The score you need on your exam: {needed_score:.2f} out of {noq}")
    elif grade_period == "Mid-Term":
        midterm_class_standing = st.number_input("Enter your Midterm class standing (0-100):", min_value=0.0, max_value=100.0)
        prelim_grade = st.number_input("Enter your Prelim Grade (0-100):", min_value=0.0, max_value=100.0)
        if st.button("Calculate needed Midterm exam score"):
            midterm_cs_w = midterm_class_standing * (1/3)
            prelim_grade_w = prelim_grade * (1/3)
            average = desired_grade - (midterm_cs_w + prelim_grade_w)
            needed_score = (average / (1/3)) * (noq / 100)
            if needed_score > noq:
                reason = "Midterm Class Standing" if midterm_class_standing < prelim_grade else "Prelim Grade"
                st.error(f"Cannot achieve {desired_grade} because {reason} is too low.")
            else:
                st.success(f"Score needed on exam: {needed_score:.2f} out of {noq}")
    elif grade_period == "Final":
        final_class_standing = st.number_input("Enter your Final class standing (0-100):", min_value=0.0, max_value=100.0)
        midterm_grade = st.number_input("Enter your Midterm Grade (0-100):", min_value=0.0, max_value=100.0)
        if st.button("Calculate needed Final exam score"):
            final_cs_w = final_class_standing * (1/3)
            midterm_grade_w = midterm_grade * (1/3)
            average = desired_grade - (final_cs_w + midterm_grade_w)
            needed_score = (average / (1/3)) * (noq / 100)
            if needed_score > noq:
                reason = "Final Class Standing" if final_class_standing < midterm_grade else "Midterm Grade"
                st.error(f"Cannot achieve {desired_grade} because {reason} is too low.")
            else:
                st.success(f"Score needed on exam: {needed_score:.2f} out of {noq}")


def calculate_overall_grade():
    st.header("Calculate Overall Grade")
    period = st.selectbox("Which period?", ["Prelim", "Mid-Term", "Final"])
    if period == "Prelim":
        cs = st.number_input("Class Standing:", min_value=0.0, max_value=100.0)
        exam = st.number_input("Preliminary Exam Score:", min_value=0.0, max_value=100.0)
        if st.button("Calculate Prelim Grade"):
            grade = (cs * 0.5) + (exam * 0.5)
            grade_val, desc = grading_scheme(grade)
            st.success(f"Your Preliminary Grade: {grade:.2f}")
            st.info(f"Equivalent Grade: {grade_val:.2f} ({desc})")
    elif period == "Mid-Term":
        cs = st.number_input("Class Standing:", min_value=0.0, max_value=100.0)
        exam = st.number_input("Mid-Term Exam Score:", min_value=0.0, max_value=100.0)
        prelim = st.number_input("Preliminary Grade:", min_value=0.0, max_value=100.0)
        if st.button("Calculate Mid-Term Grade"):
            partial = (cs * 0.5) + (exam * 0.5)
            grade = (partial * (2/3)) + (prelim * (1/3))
            grade_val, desc = grading_scheme(grade)
            st.success(f"Your Mid-Term Grade: {grade:.2f}")
            st.info(f"Equivalent Grade: {grade_val:.2f} ({desc})")
    elif period == "Final":
        cs = st.number_input("Class Standing:", min_value=0.0, max_value=100.0)
        exam = st.number_input("Final Exam Score:", min_value=0.0, max_value=100.0)
        midterm = st.number_input("Mid-Term Grade:", min_value=0.0, max_value=100.0)
        if st.button("Calculate Final Grade"):
            partial = (cs * 0.5) + (exam * 0.5)
            grade = (partial * (2/3)) + (midterm * (1/3))
            grade_val, desc = grading_scheme(grade)
            st.success(f"Your Final Grade: {grade:.2f}")
            st.info(f"Equivalent Grade: {grade_val:.2f} ({desc})")


def calculate_percentage(score, total):
    if total > 0:
        return (score / total) * 100
    return 0

def calculate_class_standing():
    st.header("Calculate Class Standing")
    categories = ["quiz", "assignment", "seatwork", "activity", "laboratory", "homework", "recitation"]
    class_standing = 0

    for category in categories:
        has_category = st.checkbox(f"Do you have {category}?", key=category)
        if has_category:
            num_items = st.number_input(f"How many {category}s?", min_value=1, step=1, key=f"{category}_count")
            percentages = []
            for i in range(int(num_items)):
                score = st.number_input(f"{category.title()} {i+1} score:", min_value=0.0, key=f"{category}_score_{i}")
                total = st.number_input(f"{category.title()} {i+1} total:", min_value=1.0, key=f"{category}_total_{i}")
                perc = calculate_percentage(score, total)
                percentages.append(perc)
                st.write(f"Percentage for {category} {i+1}: {perc:.2f}%")
            overall = sum(percentages) / len(percentages) if percentages else 0
            percent_equivalent = st.number_input(
                f"Enter percent equivalent for {category} (0-100):",
                min_value=0.0, max_value=100.0, key=f"{category}_percent_equiv")
            final_result = overall * (percent_equivalent / 100)
            st.info(f"Overall percentage for {category}: {overall:.2f}% (weighted: {final_result:.2f}%)")
            class_standing += final_result
    if st.button("Calculate Total Class Standing"):
        st.success(f"Class standing: {class_standing:.2f}%")

if __name__ == "__main__":
    main()
