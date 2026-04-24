import streamlit as st
from groq import Groq

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Grade Calculator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e6f0;
}

/* ── Background ── */
.stApp {
    background: #0d0b14;
    background-image:
        radial-gradient(ellipse 80% 60% at 20% 0%, rgba(99,60,180,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(30,180,140,0.12) 0%, transparent 60%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(18,14,30,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #c5bfda !important;
    padding: 6px 0;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 4px;
}

/* ── Headers ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}
h1 { font-size: 2.2rem !important; font-weight: 800 !important; }
h2 { font-size: 1.4rem !important; font-weight: 700 !important; color: #c5bfda !important; }
h3 { font-size: 1.1rem !important; font-weight: 600 !important; }

/* ── Cards / containers ── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(8px);
}
.card-accent {
    background: linear-gradient(135deg, rgba(99,60,180,0.25) 0%, rgba(30,180,140,0.15) 100%);
    border: 1px solid rgba(99,60,180,0.35);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.result-box {
    background: linear-gradient(135deg, rgba(30,180,140,0.2) 0%, rgba(99,60,180,0.2) 100%);
    border: 1px solid rgba(30,180,140,0.4);
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin-top: 1rem;
    text-align: center;
}
.result-number {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #1eb48c, #a87fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.result-label {
    font-size: 0.85rem;
    color: #9994b0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}
.grade-badge {
    display: inline-block;
    background: rgba(99,60,180,0.3);
    border: 1px solid rgba(99,60,180,0.5);
    border-radius: 8px;
    padding: 4px 14px;
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #c5a8ff;
    margin-top: 6px;
}
.error-box {
    background: rgba(220,60,60,0.15);
    border: 1px solid rgba(220,60,60,0.35);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-top: 1rem;
    color: #ff9999;
    font-size: 0.9rem;
}
.info-chip {
    display: inline-block;
    background: rgba(30,180,140,0.15);
    border: 1px solid rgba(30,180,140,0.3);
    border-radius: 100px;
    padding: 3px 12px;
    font-size: 0.78rem;
    color: #1eb48c;
    margin: 2px;
    font-weight: 500;
}
.section-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 1.4rem 0;
}
.formula-box {
    background: rgba(0,0,0,0.3);
    border-left: 3px solid #7c4aff;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    font-family: 'DM Sans', monospace;
    font-size: 0.85rem;
    color: #c5bfda;
    margin: 0.6rem 0;
}
.period-tag {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #7c4aff;
    margin-bottom: 0.2rem;
}
.category-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e8e6f0;
    text-transform: capitalize;
    margin-bottom: 0.5rem;
}

/* ── Inputs ── */
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: rgba(99,60,180,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,60,180,0.15) !important;
}

/* ── Buttons ── */
.stButton button {
    background: linear-gradient(135deg, #6B3CB4 0%, #1eb48c 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton button:active { transform: translateY(0) !important; }

/* ── Checkbox ── */
.stCheckbox label { color: #c5bfda !important; font-size: 0.9rem !important; }

/* ── Chat ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    margin-bottom: 8px !important;
}
.stChatInput textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.8rem 1rem;
}

/* ── Hide default streamlit branding ── */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(99,60,180,0.4); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Groq client ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


# ── Grading scheme ─────────────────────────────────────────────────────────────
def grading_scheme(percent_score):
    if 99 <= percent_score <= 100:  return (1.00, "Excellent")
    elif 96 <= percent_score < 99:  return (1.25, "Superior")
    elif 93 <= percent_score < 96:  return (1.50, "Meritorious")
    elif 90 <= percent_score < 93:  return (1.75, "Very Good")
    elif 87 <= percent_score < 90:  return (2.00, "Good")
    elif 84 <= percent_score < 87:  return (2.25, "Very Satisfactory")
    elif 81 <= percent_score < 84:  return (2.50, "Satisfactory")
    elif 78 <= percent_score < 81:  return (2.75, "Fair")
    elif 75 <= percent_score < 78:  return (3.00, "Passing")
    elif percent_score < 75:        return (5.00, "Failed")
    else:                           return (4.00, "Incomplete")


def calculate_percentage(score, total):
    return (score / total) * 100 if total > 0 else 0


# ── System prompt ──────────────────────────────────────────────────────────────
def build_system_prompt(app_mode, numeric_context_text=""):
    return f"""
You are an expert Grade Calculator Assistant for this Streamlit app.

The app has three modes:

1) PREDICT MAJOR EXAM GRADE
   • Prelim:
       prelim_final_grade = 0.5 * prelim_class_standing + 0.5 * prelim_exam_score
       solve for prelim_exam_score = (desired_grade - 0.5 * prelim_class_standing) / 0.5
   • Mid-Term:
       midterm_partial = 0.5 * midterm_class_standing + 0.5 * midterm_exam_score
       midterm_final_grade = (2/3) * midterm_partial + (1/3) * prelim_grade
       solve for midterm_exam_score:
         partial_needed = (desired_grade - (1/3)*prelim_grade) / (2/3)
         midterm_exam_score = (partial_needed - 0.5 * midterm_class_standing) / 0.5
   • Final:
       final_partial = 0.5 * final_class_standing + 0.5 * final_exam_score
       final_final_grade = (2/3) * final_partial + (1/3) * midterm_grade
       solve for final_exam_score:
         partial_needed = (desired_grade - (1/3)*midterm_grade) / (2/3)
         final_exam_score = (partial_needed - 0.5 * final_class_standing) / 0.5

2) CALCULATE OVERALL GRADE
   • Prelim_grade   = 0.5 * class_standing + 0.5 * exam_score
   • Midterm_grade  = (2/3) * (0.5*class_standing + 0.5*exam_score) + (1/3)*prelim_grade
   • Final_grade    = (2/3) * (0.5*class_standing + 0.5*exam_score) + (1/3)*midterm_grade

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
- If the user is just greeting or chatting, respond with a short greeting and one-line description.
- If asked about a formula, restate only the relevant formula(s) for the current mode.
- If asked to compute/predict/calculate, use the formulas above with the numeric context.
  If a required value is 0.0 or missing, ask the user to provide it.
- For point grade conversion: use the grading scheme ranges provided.
- If the user uses slurs or hate speech, refuse briefly and ask to be respectful.
- If something is not defined, say the app doesn't define it.
- Keep answers concise but mathematically precise.
"""


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem 0;'>
        <p style='font-family: Syne, sans-serif; font-size: 1.5rem; font-weight: 800;
                  background: linear-gradient(135deg, #a87fff, #1eb48c);
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                  background-clip: text; margin: 0; line-height: 1.1;'>
            Grade<br>Calculator
        </p>
        <p style='font-size: 0.72rem; color: #6b6580; margin-top: 4px; letter-spacing: 0.06em;
                  text-transform: uppercase;'>Academic Tool</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.07); margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)

    app_mode = st.radio(
        "CHOOSE MODE",
        ["🔮 Predict Major Exam Grade", "📊 Calculate Overall Grade", "📋 Calculate Class Standing"],
        label_visibility="visible",
    )
    # strip emoji prefix for logic
    mode_clean = app_mode.split(" ", 1)[1]

    st.markdown("<hr style='border-color: rgba(255,255,255,0.07); margin: 1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 0.72rem; color: #504c66; line-height: 1.6;'>
        <span style='color:#7c4aff; font-weight:600;'>v2.0</span><br>
        Developed by<br>
        <span style='color:#9994b0; font-weight:500;'>Edson Ray San Juan</span>
    </div>
    """, unsafe_allow_html=True)


# ── Page header ────────────────────────────────────────────────────────────────
icon_map = {
    "Predict Major Exam Grade": "🔮",
    "Calculate Overall Grade": "📊",
    "Calculate Class Standing": "📋",
}
st.markdown(f"""
<div style='margin-bottom: 1.8rem;'>
    <p style='font-size: 0.72rem; color: #7c4aff; font-family: Syne, sans-serif;
              font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin: 0;'>
        {icon_map[mode_clean]}  {mode_clean}
    </p>
    <h1 style='margin: 4px 0 0 0;'>{mode_clean}</h1>
</div>
""", unsafe_allow_html=True)


# ── Mode: Predict ──────────────────────────────────────────────────────────────
def predict_major_exam_grade():
    numeric_ctx = {"mode": "Predict Major Exam Grade"}

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='period-tag'>Target</div>", unsafe_allow_html=True)
        st.markdown("<div class='category-header'>Desired Grade & Setup</div>", unsafe_allow_html=True)

        desired_grade = st.number_input("Desired Grade (%)", min_value=0.0, max_value=100.0, value=90.0, step=0.5)
        grade_period  = st.selectbox("Grade Period", ["Prelim", "Mid-Term", "Final"])
        noq           = st.number_input("Number of Exam Questions", min_value=1, step=1, value=50)
        st.markdown("</div>", unsafe_allow_html=True)

        numeric_ctx.update({"desired_grade": desired_grade, "grade_period": grade_period, "noq": noq})

    with col2:
        st.markdown("<div class='card-accent'>", unsafe_allow_html=True)
        st.markdown("<div class='period-tag'>Formula Reference</div>", unsafe_allow_html=True)
        st.markdown("<div class='category-header'>How it's calculated</div>", unsafe_allow_html=True)

        if grade_period == "Prelim":
            st.markdown("<div class='formula-box'>final = 0.5 × class_standing + 0.5 × exam_score<br>→ solve for exam_score</div>", unsafe_allow_html=True)
        elif grade_period == "Mid-Term":
            st.markdown("<div class='formula-box'>partial = 0.5 × cs + 0.5 × exam<br>final = (2/3)×partial + (1/3)×prelim<br>→ solve for exam_score</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='formula-box'>partial = 0.5 × cs + 0.5 × exam<br>final = (2/3)×partial + (1/3)×midterm<br>→ solve for exam_score</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Period inputs ──
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='period-tag'>{grade_period} Inputs</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='category-header'>Enter your known grades</div>", unsafe_allow_html=True)

    result_container = st.container()

    if grade_period == "Prelim":
        prelim_cs = st.number_input("Class Standing (%)", min_value=0.0, max_value=100.0, key="pred_p_cs")
        numeric_ctx["prelim_class_standing"] = prelim_cs

        if st.button("Calculate Needed Prelim Score →", use_container_width=True):
            needed_pct   = (desired_grade - 0.5 * prelim_cs) / 0.5
            needed_score = needed_pct * (noq / 100)
            with result_container:
                if needed_score > noq or needed_pct > 100:
                    st.markdown(f"<div class='error-box'>⚠️ Cannot achieve {desired_grade}% — your Class Standing is too low.</div>", unsafe_allow_html=True)
                else:
                    pct_str = f"{needed_pct:.1f}%"
                    st.markdown(f"""
                    <div class='result-box'>
                        <div class='result-label'>Score needed on exam</div>
                        <div class='result-number'>{needed_score:.1f} <span style='font-size:1.2rem;color:#9994b0;'>/ {noq}</span></div>
                        <div class='result-label' style='margin-top:6px;'>That's <span style='color:#1eb48c;font-weight:600;'>{pct_str}</span> correct</div>
                    </div>""", unsafe_allow_html=True)

    elif grade_period == "Mid-Term":
        c1, c2 = st.columns(2)
        with c1:
            midterm_cs = st.number_input("Midterm Class Standing (%)", min_value=0.0, max_value=100.0, key="pred_m_cs")
        with c2:
            prelim_grade = st.number_input("Prelim Grade (%)", min_value=0.0, max_value=100.0, key="pred_m_pg")
        numeric_ctx.update({"midterm_class_standing": midterm_cs, "prelim_grade": prelim_grade})

        if st.button("Calculate Needed Midterm Score →", use_container_width=True):
            partial_needed = (desired_grade - (1/3) * prelim_grade) / (2/3)
            needed_pct     = (partial_needed - 0.5 * midterm_cs) / 0.5
            needed_score   = needed_pct * (noq / 100)
            with result_container:
                if needed_score > noq or needed_pct > 100:
                    st.markdown(f"<div class='error-box'>⚠️ Cannot achieve {desired_grade}% — your inputs are too low.</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='result-box'>
                        <div class='result-label'>Score needed on midterm exam</div>
                        <div class='result-number'>{needed_score:.1f} <span style='font-size:1.2rem;color:#9994b0;'>/ {noq}</span></div>
                        <div class='result-label' style='margin-top:6px;'>That's <span style='color:#1eb48c;font-weight:600;'>{needed_pct:.1f}%</span> correct</div>
                    </div>""", unsafe_allow_html=True)

    elif grade_period == "Final":
        c1, c2 = st.columns(2)
        with c1:
            final_cs = st.number_input("Final Class Standing (%)", min_value=0.0, max_value=100.0, key="pred_f_cs")
        with c2:
            midterm_grade = st.number_input("Midterm Grade (%)", min_value=0.0, max_value=100.0, key="pred_f_mg")
        numeric_ctx.update({"final_class_standing": final_cs, "midterm_grade": midterm_grade})

        if st.button("Calculate Needed Final Score →", use_container_width=True):
            partial_needed = (desired_grade - (1/3) * midterm_grade) / (2/3)
            needed_pct     = (partial_needed - 0.5 * final_cs) / 0.5
            needed_score   = needed_pct * (noq / 100)
            with result_container:
                if needed_score > noq or needed_pct > 100:
                    st.markdown(f"<div class='error-box'>⚠️ Cannot achieve {desired_grade}% — your inputs are too low.</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='result-box'>
                        <div class='result-label'>Score needed on final exam</div>
                        <div class='result-number'>{needed_score:.1f} <span style='font-size:1.2rem;color:#9994b0;'>/ {noq}</span></div>
                        <div class='result-label' style='margin-top:6px;'>That's <span style='color:#1eb48c;font-weight:600;'>{needed_pct:.1f}%</span> correct</div>
                    </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    return numeric_ctx


# ── Mode: Overall Grade ────────────────────────────────────────────────────────
def calculate_overall_grade():
    numeric_ctx = {"mode": "Calculate Overall Grade"}

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    period = st.selectbox("Grade Period", ["Prelim", "Mid-Term", "Final"])
    numeric_ctx["period"] = period

    col1, col2 = st.columns(2, gap="large")
    result_container = st.container()

    if period == "Prelim":
        with col1:
            cs = st.number_input("Class Standing (%)", min_value=0.0, max_value=100.0, key="og_p_cs")
        with col2:
            exam = st.number_input("Prelim Exam Score (%)", min_value=0.0, max_value=100.0, key="og_p_ex")
        numeric_ctx.update({"cs": cs, "exam": exam})

        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Calculate Prelim Grade →", use_container_width=True):
            grade = 0.5 * cs + 0.5 * exam
            gv, desc = grading_scheme(grade)
            with result_container:
                _show_grade_result(grade, gv, desc)

    elif period == "Mid-Term":
        with col1:
            cs   = st.number_input("Class Standing (%)", min_value=0.0, max_value=100.0, key="og_m_cs")
            exam = st.number_input("Mid-Term Exam Score (%)", min_value=0.0, max_value=100.0, key="og_m_ex")
        with col2:
            prelim = st.number_input("Prelim Grade (%)", min_value=0.0, max_value=100.0, key="og_m_pg")
        numeric_ctx.update({"cs": cs, "exam": exam, "prelim": prelim})

        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Calculate Mid-Term Grade →", use_container_width=True):
            partial = 0.5 * cs + 0.5 * exam
            grade   = (2/3) * partial + (1/3) * prelim
            gv, desc = grading_scheme(grade)
            with result_container:
                _show_grade_result(grade, gv, desc)

    elif period == "Final":
        with col1:
            cs   = st.number_input("Class Standing (%)", min_value=0.0, max_value=100.0, key="og_f_cs")
            exam = st.number_input("Final Exam Score (%)", min_value=0.0, max_value=100.0, key="og_f_ex")
        with col2:
            midterm = st.number_input("Mid-Term Grade (%)", min_value=0.0, max_value=100.0, key="og_f_mg")
        numeric_ctx.update({"cs": cs, "exam": exam, "midterm": midterm})

        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Calculate Final Grade →", use_container_width=True):
            partial = 0.5 * cs + 0.5 * exam
            grade   = (2/3) * partial + (1/3) * midterm
            gv, desc = grading_scheme(grade)
            with result_container:
                _show_grade_result(grade, gv, desc)

    return numeric_ctx


def _show_grade_result(grade, grade_val, desc):
    passed = grade >= 75
    border_color = "#1eb48c" if passed else "#dc3c3c"
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba({"30,180,140" if passed else "220,60,60"},0.15) 0%,
                rgba(99,60,180,0.15) 100%);
                border: 1px solid {border_color}44; border-radius: 16px;
                padding: 1.6rem; margin-top: 1rem; text-align: center;'>
        <div class='result-label'>Your Grade</div>
        <div class='result-number'>{grade:.2f}%</div>
        <div style='display:flex; justify-content:center; gap:10px; margin-top:10px; flex-wrap:wrap;'>
            <span class='grade-badge'>{grade_val:.2f} Points</span>
            <span class='info-chip'>{'✅' if passed else '❌'} {desc}</span>
        </div>
    </div>""", unsafe_allow_html=True)


# ── Mode: Class Standing ───────────────────────────────────────────────────────
def calculate_class_standing():
    categories  = ["quiz", "assignment", "seatwork", "activity", "laboratory", "homework", "recitation"]
    class_standing = 0.0
    numeric_ctx = {"mode": "Calculate Class Standing"}

    for category in categories:
        has_cat = st.checkbox(f"Include {category.title()}s", key=f"chk_{category}")
        if has_cat:
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='category-header'>📝 {category.title()}</div>", unsafe_allow_html=True)

            num_items = st.number_input(f"How many {category}s?", min_value=1, step=1, key=f"{category}_count")
            percentages = []

            cols_per_row = 2
            items = list(range(int(num_items)))
            for i in range(0, len(items), cols_per_row):
                row_items = items[i:i+cols_per_row]
                cols = st.columns(len(row_items) * 2, gap="small")
                for j, idx in enumerate(row_items):
                    with cols[j * 2]:
                        score = st.number_input(f"{category.title()} {idx+1} Score", min_value=0.0,
                                                key=f"{category}_score_{idx}")
                    with cols[j * 2 + 1]:
                        total = st.number_input(f"{category.title()} {idx+1} Total", min_value=1.0,
                                                key=f"{category}_total_{idx}")
                    perc = calculate_percentage(score, total)
                    percentages.append(perc)
                    st.markdown(f"<span class='info-chip'>Item {idx+1}: {perc:.1f}%</span>", unsafe_allow_html=True)

            overall = sum(percentages) / len(percentages) if percentages else 0
            pct_equiv = st.number_input(f"Weight for {category.title()} (%)", min_value=0.0, max_value=100.0,
                                        key=f"{category}_pct_equiv")
            final_result = overall * (pct_equiv / 100)
            class_standing += final_result

            c1, c2 = st.columns(2)
            c1.metric("Category Average", f"{overall:.2f}%")
            c2.metric("Weighted Contribution", f"{final_result:.2f}%")

            numeric_ctx[f"{category}_overall"] = overall
            numeric_ctx[f"{category}_weight"]  = pct_equiv
            st.markdown("</div>", unsafe_allow_html=True)

    numeric_ctx["total_class_standing"] = class_standing

    if st.button("Calculate Total Class Standing →", use_container_width=True):
        gv, desc = grading_scheme(class_standing)
        st.markdown(f"""
        <div class='result-box'>
            <div class='result-label'>Total Class Standing</div>
            <div class='result-number'>{class_standing:.2f}%</div>
            <div style='margin-top:8px;'>
                <span class='grade-badge'>{gv:.2f} Points</span>
                <span class='info-chip'>{'✅' if class_standing >= 75 else '❌'} {desc}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    return numeric_ctx


# ── Main routing ───────────────────────────────────────────────────────────────
def main():
    client = get_groq_client()

    if mode_clean == "Predict Major Exam Grade":
        numeric_ctx = predict_major_exam_grade()
    elif mode_clean == "Calculate Overall Grade":
        numeric_ctx = calculate_overall_grade()
    else:
        numeric_ctx = calculate_class_standing()

    # ── AI Chat Section ──
    st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin: 2rem 0 1.4rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex; align-items:center; gap:10px; margin-bottom:1rem;'>
        <span style='font-size:1.4rem;'>🤖</span>
        <div>
            <p style='font-family:Syne,sans-serif; font-size:1.1rem; font-weight:700;
                      margin:0; color:#e8e6f0;'>AI Grade Assistant</p>
            <p style='font-size:0.75rem; color:#6b6580; margin:0;'>
                Ask about formulas, predictions, or grade conversions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    numeric_context_text = "\n".join(f"{k} = {v}" for k, v in numeric_ctx.items())

    if prompt := st.chat_input("Ask about formulas, predictions, or your grades…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            system_prompt = build_system_prompt(mode_clean, numeric_context_text)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": f"Current numeric context:\n{numeric_context_text}"},
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

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🗑️ Clear chat history", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        st.caption("Clears all messages and starts a new conversation.")


if __name__ == "__main__":
    main()
