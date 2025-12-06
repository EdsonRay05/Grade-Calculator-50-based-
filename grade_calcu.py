import streamlit as st
from groq import Groq
import os

# Initialize Groq client from Streamlit secrets (DEPLOYMENT READY)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.session_state.client_ready = True
except:
    client = None
    st.session_state.client_ready = False

# Your existing functions (COMPLETE)
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

def get_context(app_mode):
    context = f"Grade Calculator - Mode: {app_mode}\n"
    context += "Formulas:\n"
    context += "• Prelim: (Class Standing × 0.5) + (Exam × 0.5)\n"
    context += "• Midterm/Final: (New Partial × 2/3) + (Previous × 1/3)\n"
    context += "Grading: 75-78%=3.00(Passing), 99-100%=1.00(Excellent)"
    return context

def main():
    st.title("🎓 Grade Calculator with AI")
    
    # Status indicator
    if st.session_state.get("client_ready", False):
        st.sidebar.success("✅ Groq AI Ready (via secrets)")
    else:
        st.sidebar.error("❌ Groq API key missing in secrets.toml")
        st.sidebar.info("**For local testing:** Add to `.streamlit/secrets.toml`:\n``````")
    
    # Calculator mode selection
    app_mode = st.sidebar.radio("📊 Choose Calculator", [
        "Predict Major Exam Grade",
        "Calculate Overall Grade", 
        "Calculate Class Standing"
    ])
    
    # Your ORIGINAL calculators (100% unchanged)
    if app_mode == "Predict Major Exam Grade":
        predict_major_exam_grade()
    elif app_mode == "Calculate Overall Grade":
        calculate_overall_grade()
    elif app_mode == "Calculate Class Standing":
        calculate_class_standing()
    
    # AI Assistant (GROQ POWERED - works for EVERYONE)
    st.markdown("---")
    st.header("🤖 AI Grade Assistant")
    
    if not st.session_state.get("client_ready", False):
        st.warning("⚠️ AI disabled. Add `GROQ_API_KEY` to `.streamlit/secrets.toml`")
        st.info("**Deploy to Streamlit Cloud** → Add key in app settings")
        return
    
    # Chat interface with full history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your grade calculator expert. Ask me about formulas, what-if scenarios, or grade conversions!"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("💬 Ask about grades, formulas, or your calculation..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate Groq response (ultra-fast streaming)
        with st.chat_message("assistant"):
            context = get_context(app_mode)
            messages = [
                {"role": "system", "content": f"""You are an expert Grade Calculator Assistant.
Current app context: {context}

Help with:
• Exact grade calculations using app formulas
• What-if scenarios ("What exam score for 92?")
• Formula explanations  
• Grade point conversions
• Study tips for target grades

Be precise with math. Use official grading scheme."""},
                *st.session_state.messages  # Full conversation history
            ]
            
            try:
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",  # Best for math/precision
                    messages=messages,
                    temperature=0.1,
                    stream=True
                )
                
                response_container = st.empty()
                full_response = ""
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        response_container.markdown(full_response + "▌")
                
                response_container.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                st.info("Check your Groq quota at console.groq.com")
    
    # Chat controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Chat cleared! Ask me anything about grades."}
            ]
            st.rerun()
    with col2:
        if st.button("📋 Copy Context", use_container_width=True):
            context = get_context(app_mode)
            st.code(context, language="text")
    
    st.markdown("---")
    st.markdown("**Developed by Edson Ray San Juan**")

# YOUR ORIGINAL FUNCTIONS (COMPLETE - unchanged)
def predict_major_exam_grade():
    st.header("🔮 Predict Major Exam Grade")
    desired_grade = st.number_input("Desired grade (0-100):", min_value=0.0, max_value=100.0)
    grade_period = st.selectbox("Period:", ["Prelim", "Mid-Term", "Final"])
    noq = st.number_input("Exam questions:", min_value=1, step=1)

    if grade_period == "Prelim":
        cs = st.number_input("Class Standing %:", min_value=0.0, max_value=100.0)
        if st.button("🎯 Calculate needed score"):
            cs_weight = cs * 0.5
            needed_avg = desired_grade - cs_weight
            needed_score = (needed_avg / 0.5) * (noq / 100)
            if needed_score > noq:
                st.error(f"❌ Impossible - CS too low for {desired_grade}")
            else:
                st.success(f"🎉 Need **{needed_score:.1f}/{noq}** ({needed_score/noq*100:.1f}%)")
    elif grade_period == "Mid-Term":
        cs = st.number_input("Midterm CS %:", min_value=0.0, max_value=100.0)
        prelim = st.number_input("Prelim Grade:", min_value=0.0, max_value=100.0)
        if st.button("🎯 Calculate needed score"):
            cs_w = cs * (1/3); prelim_w = prelim * (1/3)
            needed_avg = desired_grade - (cs_w + prelim_w)
            needed_score = (needed_avg / (1/3)) * (noq / 100)
            if needed_score > noq:
                st.error("❌ Impossible")
            else:
                st.success(f"🎉 Need **{needed_score:.1f}/{noq}**")
    else:  # Final
        cs = st.number_input("Final CS %:", min_value=0.0, max_value=100.0)
        midterm = st.number_input("Midterm Grade:", min_value=0.0, max_value=100.0)
        if st.button("🎯 Calculate needed score"):
            cs_w = cs * (1/3); midterm_w = midterm * (1/3)
            needed_avg = desired_grade - (cs_w + midterm_w)
            needed_score = (needed_avg / (1/3)) * (noq / 100)
            if needed_score > noq:
                st.error("❌ Impossible")
            else:
                st.success(f"🎉 Need **{needed_score:.1f}/{noq}**")

def calculate_overall_grade():
    st.header("📊 Calculate Overall Grade")
    period = st.selectbox("Period:", ["Prelim", "Mid-Term", "Final"])
    if period == "Prelim":
        cs = st.number_input("Class Standing:", 0.0, 100.0)
        exam = st.number_input("Exam:", 0.0, 100.0)
        if st.button("Calculate"):
            grade = (cs * 0.5) + (exam * 0.5)
            val, desc = grading_scheme(grade)
            st.success(f"**Grade: {grade:.1f}%** = {val} ({desc})")
    elif period == "Mid-Term":
        cs = st.number_input("Class Standing:", 0.0, 100.0)
        exam = st.number_input("Exam:", 0.0, 100.0)
        prelim = st.number_input("Prelim Grade:", 0.0, 100.0)
        if st.button("Calculate"):
            partial = (cs * 0.5) + (exam * 0.5)
            grade = (partial * 2/3) + (prelim * 1/3)
            val, desc = grading_scheme(grade)
            st.success(f"**Grade: {grade:.1f}%** = {val} ({desc})")
    else:
        cs = st.number_input("Class Standing:", 0.0, 100.0)
        exam = st.number_input("Exam:", 0.0, 100.0)
        midterm = st.number_input("Midterm Grade:", 0.0, 100.0)
        if st.button("Calculate"):
            partial = (cs * 0.5) + (exam * 0.5)
            grade = (partial * 2/3) + (midterm * 1/3)
            val, desc = grading_scheme(grade)
            st.success(f"**Final Grade: {grade:.1f}%** = {val} ({desc})")

def calculate_class_standing():
    st.header("📈 Class Standing")
    categories = ["quiz", "assignment", "seatwork", "activity", "lab", "homework", "recitation"]
    total_cs = 0
    
    for cat in categories:
        if st.checkbox(f"📚 {cat.title()}", key=cat):
            n = st.number_input(f"{cat.title()}s:", 1, 20, 1, key=f"n_{cat}")
            scores = []
            for i in range(n):
                score = st.number_input(f"{cat.title()} {i+1} score:", 0.0, key=f"{cat}_s_{i}")
                total = st.number_input(f"Total:", 1.0, key=f"{cat}_t_{i}")
                scores.append(calculate_percentage(score, total))
            
            avg = sum(scores) / len(scores)
            weight = st.number_input(f"{cat.title()} weight %:", 0.0, 100.0, key=f"w_{cat}")
            weighted = avg * (weight / 100)
            st.info(f"**{cat.title()}: {avg:.1f}%** (weighted: {weighted:.1f}%)")
            total_cs += weighted
    
    if st.button("🎯 Total Class Standing"):
        st.success(f"**Total: {total_cs:.1f}%**")

if __name__ == "__main__":
    main()
