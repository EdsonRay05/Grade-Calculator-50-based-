import streamlit as st
from groq import Groq

# ---------- Groq client from Streamlit secrets ----------
@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------- Helpers ----------
def grading_scheme(percent_score):
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

def calculate_percentage(score, total):
    if total > 0:
        return (score / total) * 100
    return 0

def build_system_prompt(app_mode, numeric_context_text=""):
    return f"""
You are an expert Grade Calculator Assistant for this Streamlit app.

The app has three modes:

1) PREDICT MAJOR EXAM GRADE
   • Prelim:
       prelim_final_grade = 0.5 * prelim_class_standing + 0.5 * prelim_exam_score
       Given desired_grade and prelim_class_standing, solve for prelim_exam_score.
   • Mid-Term:
       midterm_partial = 0.5 * midterm_class_standing + 0.5 * midterm_exam_score
       midterm_final_grade = (2/3) * midterm_partial + (1/3) * prelim_grade
       Given desired_grade, midterm_class_standing, prelim_grade, solve for midterm_exam_score.
   • Final:
       final_partial = 0.5 * final_class_standing + 0.5 * final_exam_score
       final_final_grade = (2/3) * final_partial + (1/3) * midterm_grade
       Given desired_grade, final_class_standing, midterm_grade, solve for final_exam_score.

2) CALCULATE OVERALL GRADE
   • Prelim_grade   = 0.5 * class_standing + 0.5 * exam_score
   • Midterm_grade  = (2/3) * (0.5 * class_standing + 0.5 * exam_score) + (1/3) * prelim_grade
   • Final_grade    = (2/3) * (0.5 * class_standing + 0.5 * exam_score) + (1/3) * midterm_grade

3) CALCULATE CLASS STANDING
   • For each category:
        item_percent_i = score_i / total_i * 100
        category_percent = average(item_percent_i)
        weighted = category_percent * (percent_equivalent / 100)
   • Overall_class_standing = sum(weighted for all categories).

Current active mode: {app_mode}.
Current numeric context (from UI):
{numeric_context_text}

RESPONSE RULES:
- If the user is just greeting or chatting (e.g., "hi", "hello", "hey"), respond with a short greeting
  and a one-line description of what you can do. Do NOT perform any calculation.
- If the user asks about a formula (e.g., "Predict Major Exam Grade formula"),
  restate ONLY the relevant formula(s) for the current mode and period, using the definitions above.
- If the user explicitly asks you to compute or predict (words like "compute", "calculate",
  "what score do I need", "predict", "how many points"), then:
    • Use the formulas above.
    • Use the numeric context values ONLY if they look like they were really entered by the user.
      If a required value is 0.0 or clearly missing, ask the user to provide it instead of assuming zero.
- If the user asks for point grade conversion (e.g., "92% is what point grade?"):
    • Explain that the app uses a grading scheme where ranges of percentages map to point grades.
    • Use these examples:
        99–100% → 1.00 (Excellent)
        96–98%  → 1.25 (Superior)
        93–95%  → 1.50 (Meritorious)
        90–92%  → 1.75 (Very Good)
        87–89%  → 2.00 (Good)
        84–86%  → 2.25 (Very Satisfactory)
        81–83%  → 2.50 (Satisfactory)
        78–80%  → 2.75 (Fair)
        75–77%  → 3.00 (Passing)
        below 75% → 5.00 (Failed)
    • For example, 92% is 1.75 (Very Good); 82% is 2.50 (Satisfactory); 76% is 3.00 (Passing).
    • When the user gives a specific percentage, state the corresponding point grade and description.
- If the user uses slurs, hate speech, or insulting language, do NOT answer their question.
  Instead reply briefly with something like:
  "I cannot respond to abusive or disrespectful language. Please ask your grade question respectfully."
- If something is not defined above, say:
  "This app does not define a formula for that. Please ask your instructor."
- Keep answers concise but mathematically precise.


# ---------- Main app ----------
def main():
    st.title("Grade Calculator")
    client = get_groq_client()

    app_mode = st.sidebar.radio(
        "Choose Option",
        ["Predict Major Exam Grade", "Calculate Overall Grade", "Calculate Class Standing"],
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='font-size: 12px; color: gray;'>"
        "Developed by <b>Edson Ray San Juan</b>"
        "</div>",
        unsafe_allow_html=True,
    )
    
    if app_mode == "Predict Major Exam Grade":
        numeric_ctx = predict_major_exam_grade()
    elif app_mode == "Calculate Overall Grade":
        numeric_ctx = calculate_overall_grade()
    else:
        numeric_ctx = calculate_class_standing()

    st.write("___")
    st.header("🤖 AI Grade Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # show history
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    numeric_context_text = "\n".join(f"{k} = {v}" for k, v in numeric_ctx.items())

    if prompt := st.chat_input("Ask about formulas, predictions, or your grades..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            system_prompt = build_system_prompt(app_mode, numeric_context_text)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is my current numeric context:\n{numeric_context_text}"},
                *st.session_state.messages,
            ]

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.1,
                stream=True,
            )

            full = ""
            placeholder = st.empty()
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full += delta
                placeholder.markdown(full + "▌")
            placeholder.markdown(full)

            st.session_state.messages.append({"role": "assistant", "content": full})

    # --- Clear chat button ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear chat history", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        st.caption("Clears all messages and starts a new conversation.")

    
# ---------- Your original calculator functions, returning numeric context ----------
def predict_major_exam_grade():
    st.header("Predict Major Exam Grade")
    desired_grade = st.number_input("Enter your desired grade (0-100):", min_value=0.0, max_value=100.0)
    grade_period = st.selectbox("Grade period:", ["Prelim", "Mid-Term", "Final"])
    noq = st.number_input("Enter your predicted number of exam questions:", min_value=1, step=1)

    numeric_ctx = {
        "mode": "Predict Major Exam Grade",
        "desired_grade": desired_grade,
        "grade_period": grade_period,
        "noq": noq,
    }

    if grade_period == "Prelim":
        prelim_class_standing = st.number_input(
            "Enter the percentage of your class standing (0-100):",
            min_value=0.0, max_value=100.0,
        )
        numeric_ctx["prelim_class_standing"] = prelim_class_standing

        if st.button("Calculate needed Prelim exam score"):
            prelim_cs = prelim_class_standing * 0.5
            average = desired_grade - prelim_cs
            needed_score = (average / 0.5) * (noq / 100)
            if needed_score > noq:
                st.error(f"Cannot achieve {desired_grade} because Prelim Class Standing is too low.")
            else:
                st.success(f"The score you need on your exam: {needed_score:.2f} out of {noq}")

    elif grade_period == "Mid-Term":
        midterm_class_standing = st.number_input(
            "Enter your Midterm class standing (0-100):",
            min_value=0.0, max_value=100.0,
        )
        prelim_grade = st.number_input(
            "Enter your Prelim Grade (0-100):",
            min_value=0.0, max_value=100.0,
        )
        numeric_ctx["midterm_class_standing"] = midterm_class_standing
        numeric_ctx["prelim_grade"] = prelim_grade

        if st.button("Calculate needed Midterm exam score"):
            midterm_cs_w = midterm_class_standing * (1 / 3)
            prelim_grade_w = prelim_grade * (1 / 3)
            average = desired_grade - (midterm_cs_w + prelim_grade_w)
            needed_score = (average / (1 / 3)) * (noq / 100)
            if needed_score > noq:
                reason = "Midterm Class Standing" if midterm_class_standing < prelim_grade else "Prelim Grade"
                st.error(f"Cannot achieve {desired_grade} because {reason} is too low.")
            else:
                st.success(f"Score needed on exam: {needed_score:.2f} out of {noq}")

    elif grade_period == "Final":
        final_class_standing = st.number_input(
            "Enter your Final class standing (0-100):",
            min_value=0.0, max_value=100.0,
        )
        midterm_grade = st.number_input(
            "Enter your Midterm Grade (0-100):",
            min_value=0.0, max_value=100.0,
        )
        numeric_ctx["final_class_standing"] = final_class_standing
        numeric_ctx["midterm_grade"] = midterm_grade

        if st.button("Calculate needed Final exam score"):
            final_cs_w = final_class_standing * (1 / 3)
            midterm_grade_w = midterm_grade * (1 / 3)
            average = desired_grade - (final_cs_w + midterm_grade_w)
            needed_score = (average / (1 / 3)) * (noq / 100)
            if needed_score > noq:
                reason = "Final Class Standing" if final_class_standing < midterm_grade else "Midterm Grade"
                st.error(f"Cannot achieve {desired_grade} because {reason} is too low.")
            else:
                st.success(f"Score needed on exam: {needed_score:.2f} out of {noq}")

    return numeric_ctx

def calculate_overall_grade():
    st.header("Calculate Overall Grade")
    period = st.selectbox("Which period?", ["Prelim", "Mid-Term", "Final"])
    numeric_ctx = {"mode": "Calculate Overall Grade", "period": period}

    if period == "Prelim":
        cs = st.number_input("Class Standing:", min_value=0.0, max_value=100.0)
        exam = st.number_input("Preliminary Exam Score:", min_value=0.0, max_value=100.0)
        numeric_ctx.update({"cs": cs, "exam": exam})
        if st.button("Calculate Prelim Grade"):
            grade = (cs * 0.5) + (exam * 0.5)
            grade_val, desc = grading_scheme(grade)
            st.success(f"Your Preliminary Grade: {grade:.2f}")
            st.info(f"Equivalent Grade: {grade_val:.2f} ({desc})")

    elif period == "Mid-Term":
        cs = st.number_input("Class Standing:", min_value=0.0, max_value=100.0)
        exam = st.number_input("Mid-Term Exam Score:", min_value=0.0, max_value=100.0)
        prelim = st.number_input("Preliminary Grade:", min_value=0.0, max_value=100.0)
        numeric_ctx.update({"cs": cs, "exam": exam, "prelim": prelim})
        if st.button("Calculate Mid-Term Grade"):
            partial = (cs * 0.5) + (exam * 0.5)
            grade = (partial * (2 / 3)) + (prelim * (1 / 3))
            grade_val, desc = grading_scheme(grade)
            st.success(f"Your Mid-Term Grade: {grade:.2f}")
            st.info(f"Equivalent Grade: {grade_val:.2f} ({desc})")

    elif period == "Final":
        cs = st.number_input("Class Standing:", min_value=0.0, max_value=100.0)
        exam = st.number_input("Final Exam Score:", min_value=0.0, max_value=100.0)
        midterm = st.number_input("Mid-Term Grade:", min_value=0.0, max_value=100.0)
        numeric_ctx.update({"cs": cs, "exam": exam, "midterm": midterm})
        if st.button("Calculate Final Grade"):
            partial = (cs * 0.5) + (exam * 0.5)
            grade = (partial * (2 / 3)) + (midterm * (1 / 3))
            grade_val, desc = grading_scheme(grade)
            st.success(f"Your Final Grade: {grade:.2f}")
            st.info(f"Equivalent Grade: {grade_val:.2f} ({desc})")

    return numeric_ctx

def calculate_class_standing():
    st.header("Calculate Class Standing")
    categories = ["quiz", "assignment", "seatwork", "activity", "laboratory", "homework", "recitation"]
    class_standing = 0
    numeric_ctx = {"mode": "Calculate Class Standing"}

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
                min_value=0.0, max_value=100.0, key=f"{category}_percent_equiv",
            )
            final_result = overall * (percent_equivalent / 100)
            st.info(f"Overall percentage for {category}: {overall:.2f}% (weighted: {final_result:.2f}%)")
            class_standing += final_result
            numeric_ctx[f"{category}_overall"] = overall
            numeric_ctx[f"{category}_weight"] = percent_equivalent

    numeric_ctx["total_class_standing"] = class_standing

    if st.button("Calculate Total Class Standing"):
        st.success(f"Class standing: {class_standing:.2f}%")

    return numeric_ctx

if __name__ == "__main__":
    main()






