import streamlit as st

# CSS for your original React styles
st.markdown("""
<style>
.main > div {
    max-width: 480px;
    margin: 40px auto;
    padding: 32px;
    background: #f6f6f6;
    border-radius: 10px;
    box-shadow: 0 2px 12px #ddd;
}
.stButton > button {
    margin: 10px 0;
    padding: 10px 22px;
    border-radius: 5px;
    border: none;
    background-color: #333;
    color: white;
    font-size: 16px;
    cursor: pointer;
}
.menu-btn > button {
    margin: 10px 0;
    padding: 8px 18px;
    border-radius: 5px;
    border: none;
    background-color: #1976d2;
    color: white;
    font-size: 15px;
    cursor: pointer;
    width: 100%;
    text-align: left;
}
input[type="number"], select {
    padding: 5px 12px;
    margin: 8px 0;
    font-size: 15px;
    border-radius: 4px;
    border: 1px solid #bbb;
    width: 100%;
    box-sizing: border-box;
}
label {
    font-size: 16px;
    margin-bottom: 2px;
    display: block;
    font-weight: bold;
}
.section {
    margin: 20px 0;
    padding: 18px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 5px #eee;
}
.result {
    background: #e3fcec;
    margin-top: 15px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    color: #126729;
}
</style>
""", unsafe_allow_html=True)


def round2(num):
    return round(num * 100) / 100


def grading_scheme(grade):
    scaled = (grade - 50) * 2
    if 94 <= scaled <= 100:
        return 1.0
    elif scaled >= 88.5:
        return 1.25
    elif scaled >= 83:
        return 1.5
    elif scaled >= 77.5:
        return 1.75
    elif scaled >= 72:
        return 2.0
    elif scaled >= 65.5:
        return 2.25
    elif scaled >= 61:
        return 2.5
    elif scaled >= 55.5:
        return 2.75
    elif scaled >= 50:
        return 3.0
    else:
        return 5.0


def predict_major_exam():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("Predict Major Exam")
    with st.form("predict_form"):
        desired_grade = st.number_input("Desired Grade (50-100):", min_value=50.0, max_value=100.0, step=0.1)
        grade_period = st.selectbox("Grade Period:", ["Prelims", "Midterms", "Finals"])
        class_standing = st.number_input("Class Standing % (0-100):", min_value=0.0, max_value=100.0)

        prev_grade = None
        if grade_period != "Prelims":
            prev_grade = st.number_input("Previous Grade (50-100):", min_value=50.0, max_value=100.0)

        num_questions = st.number_input("Number of Questions:", min_value=1, step=1)

        submitted = st.form_submit_button("Calculate")

    if submitted:
        dg = float(desired_grade)
        cs = float(class_standing)
        pg = float(prev_grade) if prev_grade is not None else 0.0
        nq = int(num_questions)
        score_needed = 0.0

        if grade_period == "Prelims":
            prelim_cs = cs * 0.5
            average_needed = dg - prelim_cs
            score_needed = (average_needed / 0.5) * (nq / 100.0)
        elif grade_period == "Midterms":
            midterm_cs = cs * (1.0 / 3.0)
            prelim_g = pg * (1.0 / 3.0)
            average_needed = dg - (midterm_cs + prelim_g)
            score_needed = (average_needed / (1.0 / 3.0)) * (nq / 100.0)
        else:  # Finals
            final_cs = cs * (1.0 / 3.0)
            mid_g = pg * (1.0 / 3.0)
            average_needed = dg - (final_cs + mid_g)
            score_needed = (average_needed / (1.0 / 3.0)) * (nq / 100.0)

        st.markdown(f'<div class="result">You need about {round2(score_needed)} out of {nq} questions to reach grade {dg}.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def calculate_overall_grades():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("Calculate Overall Grades")
    with st.form("overall_form"):
        grade_type = st.selectbox("Grade Period:", ["Preliminary", "Mid-Term", "Final"])
        class_standing = st.number_input("Class Standing %:", min_value=0.0, max_value=100.0, step=0.1, key="overall_cs")
        exam_grade = st.number_input("Exam Grade %:", min_value=0.0, max_value=100.0, step=0.1, key="overall_exam")
        prev_grade = None
        if grade_type != "Preliminary":
            prev_grade = st.number_input("Previous Grade (50-100):", min_value=50.0, max_value=100.0, step=0.1, key="overall_prev")

        submitted = st.form_submit_button("Calculate")

    if submitted:
        cs = float(class_standing)
        eg = float(exam_grade)
        pg = float(prev_grade) if prev_grade is not None else 0.0
        raw_grade = 0.0
        if grade_type == "Preliminary":
            raw_grade = cs * 0.5 + eg * 0.5
        elif grade_type == "Mid-Term":
            partial_mid = cs * 0.5 + eg * 0.5
            raw_grade = partial_mid * (2.0 / 3.0) + pg * (1.0 / 3.0)
        else:  # Final
            partial_final = cs * 0.5 + eg * 0.5
            raw_grade = partial_final * (2.0 / 3.0) + pg * (1.0 / 3.0)

        adjusted_grade = (raw_grade / 2.0) + 50.0
        equivalent = grading_scheme(adjusted_grade)
        st.markdown(f'<div class="result">Your {grade_type} grade: {round2(adjusted_grade)}<br>Equivalent Grade: {equivalent:.2f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def calculate_class_standing():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("Calculate Class Standing")

    categories = ["quiz", "assignment", "seatwork", "activity", "laboratory", "homework", "recitation"]

    # Initialize session state for progress
    if "cs_total" not in st.session_state:
        st.session_state.cs_total = 0.0
    if "category_index" not in st.session_state:
        st.session_state.category_index = 0

    idx = st.session_state.category_index

    if idx >= len(categories):
        st.subheader(f"Total Class Standing: {round2(st.session_state.cs_total)}%")
        if st.button("Reset"):
            st.session_state.cs_total = 0.0
            st.session_state.category_index = 0
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.write(f"Next: {categories[idx]}")

    with st.form(f"category_form_{idx}"):
        percent_equivalent = st.number_input("Percent Equivalent:", min_value=0.0, max_value=100.0, step=0.1, key=f"pe_{idx}")
        num_items = st.number_input("Number of Items:", min_value=1, step=1, key=f"num_items_{idx}")

        scores = []
        for i in range(int(num_items)):
            score = st.number_input(f"Score {i+1}:", min_value=0.0, step=0.1, key=f"score_{idx}_{i}")
            total = st.number_input(f"Total {i+1}:", min_value=0.0, step=0.1, key=f"total_{idx}_{i}")
            scores.append((score, total))

        submitted = st.form_submit_button("Calculate Category")
        skipped = st.form_submit_button("Skip")

    if submitted:
        valid = True
        total_percent = 0.0
        for s, t in scores:
            if t <= 0 or s < 0 or s > t:
                valid = False
                break
            total_percent += (s / t) * 100.0

        if not valid or len(scores) == 0:
            st.error("Please enter valid scores.")
            return

        avg_percent = total_percent / len(scores)
        pe = float(percent_equivalent)
        if pe <= 0 or pe > 100:
            st.error("Valid percent equivalent is 1-100.")
            return

        final_category_score = (avg_percent * pe) / 100.0
        st.markdown(f'<div class="result">Category "{categories[idx]}" average: {round2(avg_percent)}%. Contribution: {round2(final_category_score)}%.</div>', unsafe_allow_html=True)

        st.session_state.cs_total += final_category_score
        st.session_state.category_index += 1
        st.experimental_rerun()

    if skipped:
        st.session_state.category_index += 1
        st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def main():
    st.title("Grade Calculator")

    if "page" not in st.session_state:
        st.session_state.page = "menu"

    if st.session_state.page == "menu":
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.header("Grade Calculator Menu")

        if st.button("[1] Predict Major Exam", key="menu1"):
            st.session_state.page = "predict"
        if st.button("[2] Calculate Overall Grades", key="menu2"):
            st.session_state.page = "overall"
        if st.button("[3] Calculate Class Standing", key="menu3"):
            st.session_state.page = "classStanding"

        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "predict":
        if st.button("← Back to Menu"):
            st.session_state.page = "menu"
        predict_major_exam()

    elif st.session_state.page == "overall":
        if st.button("← Back to Menu"):
            st.session_state.page = "menu"
        calculate_overall_grades()

    elif st.session_state.page == "classStanding":
        if st.button("← Back to Menu"):
            st.session_state.page = "menu"
        calculate_class_standing()


if __name__ == "__main__":
    main()
