import streamlit as st

# CSS to replicate your React app styles
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

/* Buttons */
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

/* Menu buttons */
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

/* Input fields */
input[type="number"], select {
    padding: 5px 12px;
    margin: 8px 0;
    font-size: 15px;
    border-radius: 4px;
    border: 1px solid #bbb;
    width: 100%;
    box-sizing: border-box;
}

/* Labels */
label {
    font-size: 16px;
    margin-bottom: 2px;
    display: block;
    font-weight: bold;
}

/* Sections */
.section {
    margin: 20px 0;
    padding: 18px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 5px #eee;
}

/* Result box */
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

# Use containers with markdown and HTML to add the section and results box styling classes to parts of the UI

def round2(num):
    return round(num * 100) / 100

def grading_scheme(grade):
    scaled = (grade - 50) * 2
    if scaled >= 94 and scaled <= 100:
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
    with st.container():
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("### Predict Major Exam")

        desired_grade = st.number_input("Desired Grade (50-100):", min_value=50.0, max_value=100.0, step=0.1)
        grade_period = st.selectbox("Grade Period:", ["Prelims", "Midterms", "Finals"])
        class_standing = st.number_input("Class Standing % (0-100):", min_value=0.0, max_value=100.0)

        prev_grade = None
        if grade_period != "Prelims":
            prev_grade = st.number_input("Previous Grade (50-100):", min_value=50.0, max_value=100.0)

        num_questions = st.number_input("Number of Questions:", min_value=1, step=1)

        result = None
        if (
            desired_grade and class_standing and num_questions and
            (grade_period == "Prelims" or prev_grade is not None)
        ):
            dg = float(desired_grade)
            cs = float(class_standing)
            pg = float(prev_grade) if prev_grade is not None else 0.0
            nq = int(num_questions)

            if grade_period == "Prelims":
                prelim_cs = cs * 0.5
                average_needed = dg - prelim_cs
                score_needed = (average_needed / 0.5) * (nq / 100.0)
            elif grade_period == "Midterms":
                midterm_cs = cs * (1.0 / 3.0)
                prelim_g = pg * (1.0 / 3.0)
                average_needed = dg - (midterm_cs + prelim_g)
                score_needed = (average_needed / (1.0 / 3.0)) * (nq / 100.0)
            else:
                final_cs = cs * (1.0 / 3.0)
                mid_g = pg * (1.0 / 3.0)
                average_needed = dg - (final_cs + mid_g)
                score_needed = (average_needed / (1.0 / 3.0)) * (nq / 100.0)

            result = f"You need about {round2(score_needed)} out of {nq} questions to reach grade {dg}."

        if result:
            st.markdown(f'<div class="result">{result}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# Similar containers and styling can be added for the other two functional components (Calculate Overall Grades and Calculate Class Standing)
# ...

# For navigation buttons (like menu) you can create full-width blue buttons like:

def menu():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("### Grade Calculator Menu")

    if st.button("[1] Predict Major Exam", key="menu1"):
        st.session_state.page = "predict"
    if st.button("[2] Calculate Overall Grades", key="menu2"):
        st.session_state.page = "overall"
    if st.button("[3] Calculate Class Standing", key="menu3"):
        st.session_state.page = "classStanding"

    st.markdown('</div>', unsafe_allow_html=True)

# Put it together with a simple state machine:

if "page" not in st.session_state:
    st.session_state.page = "menu"

if st.session_state.page == "menu":
    menu()
elif st.session_state.page == "predict":
    if st.button("← Back to Menu"):
        st.session_state.page = "menu"
    predict_major_exam()

# Add similar structure for other pages.

