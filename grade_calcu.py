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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"], .stApp, p, span, label, div, button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: #080c14;
    background-image:
        radial-gradient(ellipse 70% 50% at 10% 0%,  rgba(56,100,220,0.16) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 90% 90%, rgba(20,200,150,0.11) 0%, transparent 55%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0b0f1a !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
[data-testid="stSidebar"] .stRadio label { color: #a0a8c0 !important; font-size: 0.88rem !important; }

/* Headings */
h1, h2, h3, h4 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -0.03em !important;
    color: #dde2f0 !important;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 9px !important;
    color: #6b7494 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 8px 22px !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3864dc 0%, #14c896 100%) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.4rem !important; }

/* Cards */
.gc-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem 1.6rem 1.6rem;
    margin-bottom: 1rem;
}
.gc-card-blue {
    background: linear-gradient(135deg, rgba(56,100,220,0.18) 0%, rgba(56,100,220,0.06) 100%);
    border: 1px solid rgba(56,100,220,0.28);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1rem;
}
.gc-card-green {
    background: linear-gradient(135deg, rgba(20,200,150,0.16) 0%, rgba(20,200,150,0.05) 100%);
    border: 1px solid rgba(20,200,150,0.28);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1rem;
}

/* Term pill labels */
.term-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.pill-blue   { background: rgba(56,100,220,0.25); color: #7ca4ff; border: 1px solid rgba(56,100,220,0.4); }
.pill-indigo { background: rgba(120,60,220,0.25); color: #c09fff; border: 1px solid rgba(120,60,220,0.4); }
.pill-green  { background: rgba(20,200,150,0.2);  color: #30d4a8; border: 1px solid rgba(20,200,150,0.35); }

.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #dde2f0;
    margin: 0 0 1rem 0;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Formula box */
.formula-box {
    background: rgba(0,0,0,0.35);
    border-left: 3px solid #3864dc;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.76rem;
    color: #a0b0d8;
    margin: 0.8rem 0 0;
    line-height: 1.8;
}

/* Result boxes */
.result-pass {
    background: linear-gradient(135deg, rgba(20,200,150,0.18) 0%, rgba(56,100,220,0.12) 100%);
    border: 1px solid rgba(20,200,150,0.35);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    margin-top: 1rem;
}
.result-fail {
    background: linear-gradient(135deg, rgba(220,60,60,0.18) 0%, rgba(56,100,220,0.10) 100%);
    border: 1px solid rgba(220,60,60,0.35);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    margin-top: 1rem;
}
.result-warn {
    background: rgba(220,60,60,0.12);
    border: 1px solid rgba(220,60,60,0.3);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    color: #ff9999;
    font-size: 0.88rem;
    margin-top: 1rem;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.big-num {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #14c896, #7ca4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    letter-spacing: -0.04em;
}
.big-num-fail {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff6b6b, #ff9966);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    letter-spacing: -0.04em;
}
.res-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #5a6280;
    margin-bottom: 4px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 700;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.badge-purple { background: rgba(120,60,220,0.3); border:1px solid rgba(120,60,220,0.45); color: #c09fff; }
.badge-green  { background: rgba(20,200,150,0.2); border:1px solid rgba(20,200,150,0.4);  color: #30d4a8; }
.badge-red    { background: rgba(220,60,60,0.2);  border:1px solid rgba(220,60,60,0.4);   color: #ff9999; }

/* Inputs */
.stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #dde2f0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
.stNumberInput input:focus {
    border-color: rgba(56,100,220,0.55) !important;
    box-shadow: 0 0 0 3px rgba(56,100,220,0.12) !important;
}
label[data-testid="stWidgetLabel"] p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
    color: #8890aa !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3864dc 0%, #14c896 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.6rem !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.18s, transform 0.12s !important;
}
.stButton > button:hover  { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0)  !important; }

/* Checkbox */
.stCheckbox label p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #a0a8c0 !important;
}

/* Chat */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    margin-bottom: 8px !important;
}
.stChatInput textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #dde2f0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    color: #dde2f0 !important;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #6b7494 !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* Chip */
.chip {
    display: inline-block;
    background: rgba(20,200,150,0.12);
    border: 1px solid rgba(20,200,150,0.28);
    border-radius: 100px;
    padding: 2px 10px;
    font-size: 0.75rem;
    color: #14c896;
    font-weight: 600;
    margin: 2px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.gc-divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.8rem 0; }

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(56,100,220,0.35); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Groq client ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


# ── Grading scheme ─────────────────────────────────────────────────────────────
def grading_scheme(pct):
    if   99  <= pct <= 100: return (1.00, "Excellent")
    elif 96  <= pct <   99: return (1.25, "Superior")
    elif 93  <= pct <   96: return (1.50, "Meritorious")
    elif 90  <= pct <   93: return (1.75, "Very Good")
    elif 87  <= pct <   90: return (2.00, "Good")
    elif 84  <= pct <   87: return (2.25, "Very Satisfactory")
    elif 81  <= pct <   84: return (2.50, "Satisfactory")
    elif 78  <= pct <   81: return (2.75, "Fair")
    elif 75  <= pct <   78: return (3.00, "Passing")
    else:                   return (5.00, "Failed")

def calc_pct(score, total):
    return (score / total * 100) if total > 0 else 0

# Convert a point grade (1.00–5.00) to its minimum percentage equivalent
POINT_TO_PCT = {
    1.00: 99.0, 1.25: 96.0, 1.50: 93.0, 1.75: 90.0,
    2.00: 87.0, 2.25: 84.0, 2.50: 81.0, 2.75: 78.0,
    3.00: 75.0, 5.00: 74.0,
}

def is_point_grade(val):
    """Return True if value looks like a point grade (1.00–5.00 range)."""
    return 1.0 <= val <= 5.0 and val not in range(6, 101)

def resolve_desired(val):
    """
    If val is a percentage (>5), return it directly.
    If val looks like a point grade (1.00–5.00), convert to its pct equivalent.
    Returns (resolved_pct, was_converted, point_val)
    """
    if val > 5.0:
        return val, False, None
    # round to nearest known point grade
    closest = min(POINT_TO_PCT.keys(), key=lambda k: abs(k - val))
    return POINT_TO_PCT[closest], True, closest


# ── System prompt ──────────────────────────────────────────────────────────────
def build_system_prompt(app_mode, ctx_text=""):
    return f"""You are an expert Grade Calculator Assistant.

Formulas:
PREDICT MAJOR EXAM GRADE:
  Prelim:   final = 0.5*cs + 0.5*exam  → exam = (desired - 0.5*cs) / 0.5
  Midterm:  final = (2/3)*(0.5*cs + 0.5*exam) + (1/3)*prelim_grade
            partial_needed = (desired - (1/3)*prelim) / (2/3)
            exam = (partial_needed - 0.5*cs) / 0.5
  Final:    final = (2/3)*(0.5*cs + 0.5*exam) + (1/3)*midterm_grade
            partial_needed = (desired - (1/3)*midterm) / (2/3)
            exam = (partial_needed - 0.5*cs) / 0.5

CALCULATE OVERALL GRADE:
  Prelim  = 0.5*cs + 0.5*exam
  Midterm = (2/3)*(0.5*cs + 0.5*exam) + (1/3)*prelim_grade
  Final   = (2/3)*(0.5*cs + 0.5*exam) + (1/3)*midterm_grade

GRADING: 99-100→1.00 Excellent, 96-98→1.25 Superior, 93-95→1.50 Meritorious,
  90-92→1.75 Very Good, 87-89→2.00 Good, 84-86→2.25 Very Satisfactory,
  81-83→2.50 Satisfactory, 78-80→2.75 Fair, 75-77→3.00 Passing, <75→5.00 Failed

Current mode: {app_mode}
UI values: {ctx_text}

RULES: Greet casually if no math asked. Use correct formulas; ask for missing values.
Refuse hate speech politely. Be concise and precise.
"""


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.2rem 0 0.6rem;'>
        <p style='font-size:1.55rem; font-weight:800; letter-spacing:-0.04em;
                  margin:0; line-height:1.15;
                  background:linear-gradient(135deg,#7ca4ff,#14c896);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                  background-clip:text;'>Grade<br>Calculator</p>
        <p style='font-size:0.68rem; color:#3a4060; margin:5px 0 0;
                  text-transform:uppercase; letter-spacing:0.1em; font-weight:600;'>
            Academic Tool · v2.1</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.05);margin:0.6rem 0 1rem;'>", unsafe_allow_html=True)

    app_mode = st.radio(
        "SELECT MODE",
        ["🔮  Predict Exam Score", "📊  Calculate Grade", "📋  Class Standing"],
    )
    mode_key = app_mode.split("  ", 1)[1]

    st.markdown("<hr style='border-color:rgba(255,255,255,0.05);margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:0.7rem; color:#2e3450; line-height:1.7; margin:0;'>
        Developed by<br>
        <span style='color:#5a6280; font-weight:600;'>Edson Ray San Juan</span>
    </p>""", unsafe_allow_html=True)


# ── Helper: result card ────────────────────────────────────────────────────────
def show_grade_card(grade, label="Your Grade"):
    gv, desc = grading_scheme(grade)
    passed   = grade >= 75
    cls      = "result-pass" if passed else "result-fail"
    num_cls  = "big-num"     if passed else "big-num-fail"
    bdg_cls  = "badge-green" if passed else "badge-red"
    icon     = "✅" if passed else "❌"
    st.markdown(f"""
    <div class='{cls}'>
        <div class='res-label'>{label}</div>
        <div class='{num_cls}'>{grade:.2f}%</div>
        <div style='margin-top:10px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap;'>
            <span class='badge badge-purple'>{gv:.2f} pts</span>
            <span class='badge {bdg_cls}'>{icon} {desc}</span>
        </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODE 1 — PREDICT EXAM SCORE  (all 3 terms as tabs)
# ══════════════════════════════════════════════════════════════════════════════
def predict_major_exam_grade():
    st.markdown("<p style='color:#5a6280;font-size:0.88rem;margin:-0.4rem 0 1.2rem;'>Enter your desired grade and known scores — find exactly what you need on each exam.</p>", unsafe_allow_html=True)
    ctx = {"mode": "Predict Major Exam Grade"}

    t1, t2, t3 = st.tabs(["📘  Prelim", "📗  Mid-Term", "📙  Final"])

    # PRELIM
    with t1:
        st.markdown("<span class='term-pill pill-blue'>Prelim Term</span>", unsafe_allow_html=True)
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.78rem;color:#5a6280;margin:0 0 0.8rem;'>💡 You can enter a <b>percentage</b> (e.g. 85) <i>or</i> a <b>point grade</b> (e.g. 2.00) — it will be auto-converted.</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            p_des = st.number_input("Desired Prelim Grade (% or point)", 0.0, 100.0, 85.0, 0.5, key="pp_des")
            p_noq = st.number_input("No. of Exam Questions", 1, step=1, value=50, key="pp_noq")
        with c2:
            p_cs  = st.number_input("Class Standing (%)", 0.0, 100.0, 0.0, 0.5, key="pp_cs")
            st.markdown("<div class='formula-box'>final = 0.5 × cs + 0.5 × exam<br>→ exam = (desired − 0.5×cs) / 0.5</div>", unsafe_allow_html=True)
        ctx.update({"prelim_desired": p_des, "prelim_cs": p_cs, "prelim_noq": p_noq})
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Calculate Needed Prelim Score →", key="btn_pp", use_container_width=True):
            p_des_pct, was_conv, pt_val = resolve_desired(p_des)
            if was_conv:
                st.markdown(f"<div class='result-warn' style='background:rgba(56,100,220,0.1);border-color:rgba(56,100,220,0.3);color:#7ca4ff;'>ℹ️ Detected point grade <b>{pt_val:.2f}</b> → using <b>{p_des_pct:.0f}%</b> as target.</div>", unsafe_allow_html=True)
            needed_pct   = (p_des_pct - 0.5 * p_cs) / 0.5
            needed_score = needed_pct * (p_noq / 100)
            if needed_pct < 0:
                st.markdown(f"<div class='result-warn'>⚠️ Your Class Standing ({p_cs}%) already exceeds the target — you only need to show up and pass!</div>", unsafe_allow_html=True)
            elif needed_pct > 100 or needed_score > p_noq:
                st.markdown(f"<div class='result-warn'>⚠️ Cannot reach {p_des_pct:.0f}% — your Class Standing is too low to make it possible.</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-pass'>
                    <div class='res-label'>Score needed on Prelim exam</div>
                    <div class='big-num'>{needed_score:.1f} <span style='font-size:1.3rem;color:#4a5880;'>/ {p_noq}</span></div>
                    <div style='margin-top:8px;'><span class='chip'>= {needed_pct:.1f}% correct</span></div>
                </div>""", unsafe_allow_html=True)

    # MID-TERM
    with t2:
        st.markdown("<span class='term-pill pill-indigo'>Mid-Term</span>", unsafe_allow_html=True)
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.78rem;color:#5a6280;margin:0 0 0.8rem;'>💡 You can enter a <b>percentage</b> (e.g. 85) <i>or</i> a <b>point grade</b> (e.g. 2.00) for the desired grade — it will be auto-converted.</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            m_des    = st.number_input("Desired Midterm Grade (% or point)", 0.0, 100.0, 85.0, 0.5, key="pm_des")
            m_noq    = st.number_input("No. of Exam Questions", 1, step=1, value=50, key="pm_noq")
        with c2:
            m_cs     = st.number_input("Midterm Class Standing (%)", 0.0, 100.0, 0.0, 0.5, key="pm_cs")
            m_prelim = st.number_input("Your Prelim Grade (%)",      0.0, 100.0, 0.0, 0.5, key="pm_pg")
        st.markdown("""
        <div class='formula-box'>
            final = (2/3)×(0.5×cs + 0.5×exam) + (1/3)×prelim<br>
            partial_needed = (desired − (1/3)×prelim) / (2/3)<br>
            → exam = (partial_needed − 0.5×cs) / 0.5
        </div>""", unsafe_allow_html=True)
        ctx.update({"midterm_desired": m_des, "midterm_cs": m_cs, "midterm_prelim": m_prelim, "midterm_noq": m_noq})
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Calculate Needed Midterm Score →", key="btn_pm", use_container_width=True):
            m_des_pct, was_conv, pt_val = resolve_desired(m_des)
            if was_conv:
                st.markdown(f"<div class='result-warn' style='background:rgba(56,100,220,0.1);border-color:rgba(56,100,220,0.3);color:#7ca4ff;'>ℹ️ Detected point grade <b>{pt_val:.2f}</b> → using <b>{m_des_pct:.0f}%</b> as target.</div>", unsafe_allow_html=True)
            partial_needed = (m_des_pct - (1/3) * m_prelim) / (2/3)
            needed_pct     = (partial_needed - 0.5 * m_cs) / 0.5
            needed_score   = needed_pct * (m_noq / 100)
            if needed_pct < 0:
                st.markdown(f"<div class='result-warn'>⚠️ Your current inputs already exceed the target — you're on track!</div>", unsafe_allow_html=True)
            elif needed_pct > 100 or needed_score > m_noq:
                st.markdown(f"<div class='result-warn'>⚠️ Cannot reach {m_des_pct:.0f}% — your Class Standing or Prelim Grade is too low.</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-pass'>
                    <div class='res-label'>Score needed on Midterm exam</div>
                    <div class='big-num'>{needed_score:.1f} <span style='font-size:1.3rem;color:#4a5880;'>/ {m_noq}</span></div>
                    <div style='margin-top:8px;'><span class='chip'>= {needed_pct:.1f}% correct</span></div>
                </div>""", unsafe_allow_html=True)

    # FINAL
    with t3:
        st.markdown("<span class='term-pill pill-green'>Final Term</span>", unsafe_allow_html=True)
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.78rem;color:#5a6280;margin:0 0 0.8rem;'>💡 You can enter a <b>percentage</b> (e.g. 85) <i>or</i> a <b>point grade</b> (e.g. 2.00) for the desired grade — it will be auto-converted.</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            f_des     = st.number_input("Desired Final Grade (% or point)", 0.0, 100.0, 85.0, 0.5, key="pf_des")
            f_noq     = st.number_input("No. of Exam Questions", 1, step=1, value=50, key="pf_noq")
        with c2:
            f_cs      = st.number_input("Final Class Standing (%)", 0.0, 100.0, 0.0, 0.5, key="pf_cs")
            f_midterm = st.number_input("Your Midterm Grade (%)",   0.0, 100.0, 0.0, 0.5, key="pf_mg")
        st.markdown("""
        <div class='formula-box'>
            final = (2/3)×(0.5×cs + 0.5×exam) + (1/3)×midterm<br>
            partial_needed = (desired − (1/3)×midterm) / (2/3)<br>
            → exam = (partial_needed − 0.5×cs) / 0.5
        </div>""", unsafe_allow_html=True)
        ctx.update({"final_desired": f_des, "final_cs": f_cs, "final_midterm": f_midterm, "final_noq": f_noq})
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Calculate Needed Final Score →", key="btn_pf", use_container_width=True):
            f_des_pct, was_conv, pt_val = resolve_desired(f_des)
            if was_conv:
                st.markdown(f"<div class='result-warn' style='background:rgba(56,100,220,0.1);border-color:rgba(56,100,220,0.3);color:#7ca4ff;'>ℹ️ Detected point grade <b>{pt_val:.2f}</b> → using <b>{f_des_pct:.0f}%</b> as target.</div>", unsafe_allow_html=True)
            partial_needed = (f_des_pct - (1/3) * f_midterm) / (2/3)
            needed_pct     = (partial_needed - 0.5 * f_cs) / 0.5
            needed_score   = needed_pct * (f_noq / 100)
            if needed_pct < 0:
                st.markdown(f"<div class='result-warn'>⚠️ Your current inputs already exceed the target — you're on track!</div>", unsafe_allow_html=True)
            elif needed_pct > 100 or needed_score > f_noq:
                st.markdown(f"<div class='result-warn'>⚠️ Cannot reach {f_des_pct:.0f}% — your Class Standing or Midterm Grade is too low.</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-pass'>
                    <div class='res-label'>Score needed on Final exam</div>
                    <div class='big-num'>{needed_score:.1f} <span style='font-size:1.3rem;color:#4a5880;'>/ {f_noq}</span></div>
                    <div style='margin-top:8px;'><span class='chip'>= {needed_pct:.1f}% correct</span></div>
                </div>""", unsafe_allow_html=True)

    return ctx


# ══════════════════════════════════════════════════════════════════════════════
# MODE 2 — CALCULATE OVERALL GRADE  (all 3 terms as tabs)
# ══════════════════════════════════════════════════════════════════════════════
def calculate_overall_grade():
    st.markdown("<p style='color:#5a6280;font-size:0.88rem;margin:-0.4rem 0 1.2rem;'>Calculate your grade for any term — fill in what you have and hit Calculate.</p>", unsafe_allow_html=True)
    ctx = {"mode": "Calculate Overall Grade"}

    t1, t2, t3 = st.tabs(["📘  Prelim", "📗  Mid-Term", "📙  Final"])

    # PRELIM
    with t1:
        st.markdown("<span class='term-pill pill-blue'>Prelim Term</span>", unsafe_allow_html=True)
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            p_cs   = st.number_input("Class Standing (%)",    0.0, 100.0, key="og_p_cs")
        with c2:
            p_exam = st.number_input("Prelim Exam Score (%)", 0.0, 100.0, key="og_p_ex")
        st.markdown("<div class='formula-box'>Prelim Grade = 0.5 × Class Standing + 0.5 × Exam Score</div>", unsafe_allow_html=True)
        ctx.update({"prelim_cs": p_cs, "prelim_exam": p_exam})
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Calculate Prelim Grade →", key="btn_og_p", use_container_width=True):
            show_grade_card(0.5 * p_cs + 0.5 * p_exam, "Prelim Grade")

    # MID-TERM
    with t2:
        st.markdown("<span class='term-pill pill-indigo'>Mid-Term</span>", unsafe_allow_html=True)
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            m_cs     = st.number_input("Class Standing (%)",     0.0, 100.0, key="og_m_cs")
        with c2:
            m_exam   = st.number_input("Midterm Exam Score (%)", 0.0, 100.0, key="og_m_ex")
        with c3:
            m_prelim = st.number_input("Prelim Grade (%)",       0.0, 100.0, key="og_m_pg")
        st.markdown("<div class='formula-box'>partial = 0.5×cs + 0.5×exam<br>Midterm Grade = (2/3)×partial + (1/3)×Prelim Grade</div>", unsafe_allow_html=True)
        ctx.update({"midterm_cs": m_cs, "midterm_exam": m_exam, "midterm_prelim": m_prelim})
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Calculate Midterm Grade →", key="btn_og_m", use_container_width=True):
            partial = 0.5 * m_cs + 0.5 * m_exam
            show_grade_card((2/3) * partial + (1/3) * m_prelim, "Midterm Grade")

    # FINAL
    with t3:
        st.markdown("<span class='term-pill pill-green'>Final Term</span>", unsafe_allow_html=True)
        st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            f_cs      = st.number_input("Class Standing (%)",    0.0, 100.0, key="og_f_cs")
        with c2:
            f_exam    = st.number_input("Final Exam Score (%)",  0.0, 100.0, key="og_f_ex")
        with c3:
            f_midterm = st.number_input("Midterm Grade (%)",     0.0, 100.0, key="og_f_mg")
        st.markdown("<div class='formula-box'>partial = 0.5×cs + 0.5×exam<br>Final Grade = (2/3)×partial + (1/3)×Midterm Grade</div>", unsafe_allow_html=True)
        ctx.update({"final_cs": f_cs, "final_exam": f_exam, "final_midterm": f_midterm})
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Calculate Final Grade →", key="btn_og_f", use_container_width=True):
            partial = 0.5 * f_cs + 0.5 * f_exam
            show_grade_card((2/3) * partial + (1/3) * f_midterm, "Final Grade")

    return ctx


# ══════════════════════════════════════════════════════════════════════════════
# MODE 3 — CLASS STANDING
# ══════════════════════════════════════════════════════════════════════════════
def calculate_class_standing():
    st.markdown("<p style='color:#5a6280;font-size:0.88rem;margin:-0.4rem 0 1.2rem;'>Check the categories you have, enter your scores, and set each weight.</p>", unsafe_allow_html=True)

    categories     = ["Quiz", "Assignment", "Seatwork", "Activity", "Laboratory", "Homework", "Recitation"]
    class_standing = 0.0
    ctx            = {"mode": "Calculate Class Standing"}

    for cat in categories:
        key = cat.lower()
        has_cat = st.checkbox(f"Include {cat}s", key=f"chk_{key}")
        if has_cat:
            st.markdown("<div class='gc-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='section-title'>📝 {cat}</div>", unsafe_allow_html=True)

            num_items   = st.number_input(f"How many {cat}s?", min_value=1, step=1, key=f"{key}_count")
            percentages = []

            for i in range(int(num_items)):
                c1, c2, c3 = st.columns([2, 2, 1], gap="small")
                with c1:
                    score = st.number_input(f"{cat} {i+1} — Score", min_value=0.0, key=f"{key}_score_{i}")
                with c2:
                    total = st.number_input(f"{cat} {i+1} — Total", min_value=1.0, value=100.0, key=f"{key}_total_{i}")
                with c3:
                    pct = calc_pct(score, total)
                    st.metric(f"Item {i+1}", f"{pct:.1f}%")
                percentages.append(pct)

            overall  = sum(percentages) / len(percentages) if percentages else 0.0
            wt_col, _ = st.columns([1, 2])
            with wt_col:
                pct_equiv = st.number_input(f"Weight for {cat} (%)", 0.0, 100.0, key=f"{key}_wt")
            weighted        = overall * (pct_equiv / 100)
            class_standing += weighted

            m1, m2 = st.columns(2)
            m1.metric("Category Average",      f"{overall:.2f}%")
            m2.metric("Weighted Contribution", f"{weighted:.2f}%")

            ctx[f"{key}_avg"]    = overall
            ctx[f"{key}_weight"] = pct_equiv
            st.markdown("</div>", unsafe_allow_html=True)

    ctx["total_class_standing"] = class_standing

    st.markdown(f"""
    <div class='gc-card-blue' style='text-align:center;margin-top:0.5rem;'>
        <div class='res-label'>Running Total Class Standing</div>
        <div class='big-num' style='font-size:2.4rem;'>{class_standing:.2f}%</div>
    </div>""", unsafe_allow_html=True)

    if st.button("Finalize & Show Grade Equivalent →", use_container_width=True):
        show_grade_card(class_standing, "Class Standing")

    return ctx


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    client = get_groq_client()

    titles = {
        "Predict Exam Score": ("🔮", "Predict Exam Score"),
        "Calculate Grade":    ("📊", "Calculate Overall Grade"),
        "Class Standing":     ("📋", "Class Standing"),
    }
    icon, title = titles[mode_key]
    st.markdown(f"""
    <div style='margin-bottom:1.6rem;'>
        <p style='font-size:0.68rem; font-weight:700; text-transform:uppercase;
                  letter-spacing:0.12em; color:#3864dc; margin:0 0 4px;'>{icon}  {mode_key}</p>
        <h1 style='margin:0; font-size:2rem; font-weight:800; color:#dde2f0; letter-spacing:-0.04em;'>{title}</h1>
    </div>
    """, unsafe_allow_html=True)

    if mode_key == "Predict Exam Score":
        ctx = predict_major_exam_grade()
    elif mode_key == "Calculate Grade":
        ctx = calculate_overall_grade()
    else:
        ctx = calculate_class_standing()

    # ── AI Chat ──────────────────────────────────────────────────────────────
    st.markdown("<hr class='gc-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;margin-bottom:1rem;'>
        <div style='width:36px;height:36px;border-radius:10px;flex-shrink:0;
                    background:linear-gradient(135deg,#3864dc,#14c896);
                    display:flex;align-items:center;justify-content:center;font-size:1.1rem;'>🤖</div>
        <div>
            <p style='font-size:1rem;font-weight:700;margin:0;color:#dde2f0;'>AI Grade Assistant</p>
            <p style='font-size:0.72rem;color:#3a4060;margin:0;'>Ask about formulas, predictions, or grade conversions</p>
        </div>
    </div>""", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    ctx_text = "\n".join(f"{k} = {v}" for k, v in ctx.items())

    if prompt := st.chat_input("Ask about formulas, predictions, or your grades…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            sys_p = build_system_prompt(mode_key, ctx_text)
            msgs  = [
                {"role": "system", "content": sys_p},
                {"role": "user",   "content": f"Current UI context:\n{ctx_text}"},
                *st.session_state.messages,
            ]
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=msgs,
                temperature=0.1,
                stream=True,
            )
            full, placeholder = "", st.empty()
            for chunk in stream:
                full += chunk.choices[0].delta.content or ""
                placeholder.markdown(full + "▌")
            placeholder.markdown(full)
            st.session_state.messages.append({"role": "assistant", "content": full})

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with c2:
        st.caption("Clears all messages and starts a fresh conversation.")


if __name__ == "__main__":
    main()
