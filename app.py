import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="centered"
)

# =========================
# DARK/LIGHT MODE STATE
# =========================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# =========================
# THEME TOGGLE BUTTON
# =========================
col_theme1, col_theme2, col_theme3 = st.columns([1, 1, 3])
with col_theme1:
    if st.button("🌙 Dark Mode", use_container_width=True):
        st.session_state.theme_mode = "dark"
        st.rerun()
with col_theme2:
    if st.button("☀️ Light Mode", use_container_width=True):
        st.session_state.theme_mode = "light"
        st.rerun()

# =========================
# DYNAMIC CSS BASED ON THEME
# =========================
if st.session_state.theme_mode == "dark":
    theme_css = """
    <style>
    .stApp {
        background: linear-gradient(to right, #0F2027, #203A43, #2C5364);
    }
    html, body, [class*="css"] {
        color: white !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    .stMarkdown, p, div, span {
        color: white !important;
    }
    .st-emotion-cache-1v0mbdj, .st-emotion-cache-10trblm {
        color: white !important;
    }
    label, .stSelectbox label, .stNumberInput label {
        color: white !important;
    }
    .stNumberInput input {
        background-color: #111111 !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid #555;
    }
    div[data-baseweb="select"] > div {
        background-color: #111111 !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #555 !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: white !important;
    }
    ul, li {
        background-color: #111111 !important;
        color: white !important;
    }
    li:hover {
        background-color: #333333 !important;
        color: #00FFD1 !important;
    }
    .stButton > button {
        background: linear-gradient(to right, #00C9FF, #92FE9D);
        color: black !important;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 18px rgba(0,255,200,0.5);
    }
    .stDownloadButton > button {
        background-color: #111111 !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid #00FFD1;
        font-weight: bold;
    }
    .stDownloadButton > button:hover {
        background-color: #00FFD1 !important;
        color: black !important;
    }
    .stProgress > div > div > div > div {
        background-color: #00FFD1;
    }
    .stAlert, .stSuccess, .stInfo, .stWarning, .stError {
        color: black !important;
    }
    .insight-card {
        background: rgba(255,255,255,0.15);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #00FFD1;
        color: white !important;
    }
    .insight-card strong {
        color: #00FFD1 !important;
    }
    .stCaption, caption {
        color: #cccccc !important;
    }
    </style>
    """
else:
    theme_css = """
    <style>
    .stApp {
        background: linear-gradient(to right, #f5f7fa, #c3cfe2);
    }
    html, body, [class*="css"] {
        color: #1a1a2e !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0f3460 !important;
    }
    label {
        color: #1a1a2e !important;
        font-weight: 600;
    }
    .stNumberInput input {
        background-color: white !important;
        color: #1a1a2e !important;
        border-radius: 10px;
        border: 1px solid #0f3460;
    }
    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #1a1a2e !important;
        border-radius: 10px !important;
        border: 1px solid #0f3460 !important;
    }
    div[data-baseweb="select"] span {
        color: #1a1a2e !important;
    }
    ul {
        background-color: white !important;
        border-radius: 10px !important;
    }
    li {
        background-color: white !important;
        color: #1a1a2e !important;
    }
    li:hover {
        background-color: #e0e0e0 !important;
        color: #0f3460 !important;
    }
    .stButton > button {
        background: linear-gradient(to right, #0f3460, #16213e);
        color: white !important;
        border: none;
        border-radius: 12px;
        font-weight: bold;
    }
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 18px rgba(15,52,96,0.5);
    }
    .stDownloadButton > button {
        background-color: #0f3460 !important;
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-color: #0f3460;
    }
    .insight-card {
        background: rgba(15,52,96,0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #0f3460;
        color: #1a1a2e !important;
    }
    .insight-card strong {
        color: #0f3460 !important;
    }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
try:
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")
except FileNotFoundError:
    st.error("❌ Model files not found! Please make sure 'student_model.pkl' and 'model_columns.pkl' exist.")
    st.stop()

# =========================
# TITLE
# =========================
st.title("🎓 Student Score Predictor")
st.write("Fill student details to predict exam performance.")

# =========================
# INPUT FIELDS
# =========================
col1, col2 = st.columns(2)

with col1:
    hours = st.number_input("📚 Hours Studied", min_value=0.0, max_value=24.0, step=0.5, value=5.0)
    attendance = st.number_input("📋 Attendance (%)", min_value=0.0, max_value=100.0, step=1.0, value=75.0)
    previous = st.number_input("📈 Previous Score", min_value=0.0, max_value=100.0, step=1.0, value=65.0)
    sleep = st.number_input("😴 Sleep Hours", min_value=0.0, max_value=12.0, step=0.5, value=7.0)

with col2:
    motivation = st.selectbox("💪 Motivation Level", ["Low", "Medium", "High"])
    teacher = st.selectbox("👨‍🏫 Teacher Quality", ["Poor", "Average", "Good"])
    school = st.selectbox("🏫 School Type", ["Public", "Private"])
    internet = st.selectbox("🌐 Internet Access", ["Yes", "No"])

col3, col4 = st.columns(2)

with col3:
    income = st.selectbox("💰 Family Income", ["Low", "Medium", "High"])
    parent = st.selectbox("👪 Parental Involvement", ["Low", "Medium", "High"])
    education = st.selectbox("🎓 Parent Education", ["School", "College"])

with col4:
    peer = st.selectbox("👥 Peer Influence", ["Negative", "Neutral", "Positive"])
    resources = st.selectbox("📚 Learning Resources", ["Low", "Medium", "High"])
    activities = st.selectbox("⚽ Extracurricular Activities", ["Yes", "No"])

# =========================
# PREDICT BUTTON
# =========================
if st.button("🔮 Predict Score", use_container_width=True):

    # Input Data
    data = {
        "Hours_Studied": hours,
        "Attendance": attendance,
        "Previous_Scores": previous,
        "Sleep_Hours": sleep,
        "Motivation_Level": motivation,
        "Teacher_Quality": teacher,
        "School_Type": school,
        "Internet_Access": internet,
        "Family_Income": income,
        "Parental_Involvement": parent,
        "Parental_Education_Level": education,
        "Peer_Influence": peer,
        "Learning_Resources": resources,
        "Extracurricular_Activities": activities
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([data])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # Prediction
    prediction = model.predict(input_df)[0]
    final_score = max(0, min(100, prediction))
    final_score = int(round(final_score))

    # Grade System
    if final_score >= 90:
        grade = "A+"
        grade_color = "#FFD700"
        grade_message = "🏆 Outstanding! Keep up the excellent work!"
    elif final_score >= 80:
        grade = "A"
        grade_color = "#92FE9D"
        grade_message = "🎉 Excellent! You're doing great!"
    elif final_score >= 70:
        grade = "B"
        grade_color = "#64E986"
        grade_message = "👍 Good job! A little more effort for an A!"
    elif final_score >= 60:
        grade = "C"
        grade_color = "#FFD700"
        grade_message = "📚 Not bad! Focus on weaker areas to improve."
    elif final_score >= 50:
        grade = "D"
        grade_color = "#FFA500"
        grade_message = "⚠️ Needs improvement. Consider studying harder."
    else:
        grade = "F"
        grade_color = "#FF6B6B"
        grade_message = "❌ Failing. Immediate action required!"

    # Result Card - Fixed for both themes
    if st.session_state.theme_mode == "dark":
        result_bg = "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)"
        text_color = "white"
    else:
        result_bg = "linear-gradient(135deg, #141E30 0%, #243B55 100%)"
        text_color = "white"
    
    result_html = f"""
    <div style='background: {result_bg}; padding: 40px 30px; border-radius: 25px; text-align: center; box-shadow: 0px 10px 30px rgba(0,200,255,0.2); margin-top: 30px; margin-bottom: 30px; border: 1px solid #00FFD1;'>
        <h3 style='color: #00FFD1; margin-bottom: 15px; letter-spacing: 2px; font-size: 20px;'>📊 PREDICTED EXAM SCORE</h3>
        <h1 style='color: {text_color}; font-size: 70px; margin: 10px 0; font-weight: bold;'>{final_score}<span style='font-size: 28px; color: #bbbbbb;'>/100</span></h1>
        <div style='background: {grade_color}; display: inline-block; padding: 10px 25px; border-radius: 50px; margin-top: 10px;'>
            <h3 style='color: black; margin: 0; font-weight: bold;'>📘 Predicted Grade : {grade}</h3>
        </div>
        <p style='color: #cccccc; margin-top: 20px; font-size: 14px;'>{grade_message}</p>
    </div>
    """
    st.markdown(result_html, unsafe_allow_html=True)

    # Progress Bar
    st.subheader("📈 Score Progress")
    st.progress(final_score / 100)
    st.caption(f"🎯 {final_score}% of maximum score achieved")

    # Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("🍩 Score Breakdown")
        fig, ax = plt.subplots(figsize=(5, 5))
        values = [final_score, 100 - final_score]
        labels = ["Your Score", "Remaining"]
        colors = ["#00FFD1", "#2C5364"]
        explode = (0.05, 0)
        
        # Set text color based on theme
        text_color = 'white' if st.session_state.theme_mode == "dark" else '#1a1a2e'
        
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, explode=explode, 
               wedgeprops=dict(width=0.4, edgecolor=text_color), textprops={'fontsize': 10, 'fontweight': 'bold', 'color': text_color})
        
        ax.set_title("Score Distribution", color=text_color, fontsize=12, pad=20)
        ax.axis('equal')
        st.pyplot(fig)

    with chart_col2:
        st.subheader("📊 Performance Meter")
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        categories = ['Your Score', 'Class Average', 'Target Score']
        values2 = [final_score, 65, 85]
        colors2 = ['#00FFD1' if st.session_state.theme_mode == "dark" else '#0f3460', '#FFA500', '#FF6B6B']
        bars = ax2.bar(categories, values2, color=colors2, alpha=0.7)
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Score')
        ax2.set_title('Performance Comparison', fontsize=12)
        
        # Set colors based on theme
        if st.session_state.theme_mode == "dark":
            ax2.tick_params(colors='white')
            ax2.spines['bottom'].set_color('white')
            ax2.spines['left'].set_color('white')
            ax2.yaxis.label.set_color('white')
            ax2.title.set_color('white')
            ax2.xaxis.label.set_color('white')
            for label in ax2.get_xticklabels():
                label.set_color('white')
        else:
            ax2.tick_params(colors='#1a1a2e')
            ax2.spines['bottom'].set_color('#1a1a2e')
            ax2.spines['left'].set_color('#1a1a2e')
            ax2.yaxis.label.set_color('#1a1a2e')
            ax2.title.set_color('#1a1a2e')
            ax2.xaxis.label.set_color('#1a1a2e')
            for label in ax2.get_xticklabels():
                label.set_color('#1a1a2e')
        
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        for bar, value in zip(bars, values2):
            height = bar.get_height()
            text_color = 'white' if st.session_state.theme_mode == "dark" else '#1a1a2e'
            ax2.text(bar.get_x() + bar.get_width()/2., height + 2, f'{value}', 
                    ha='center', va='bottom', color=text_color, fontweight='bold')
        st.pyplot(fig2)

    # =========================
    # FIXED INSIGHTS SECTION - WITH PROPER TEXT
    # =========================
    st.subheader("💡 Personalized Insights")
    
    # Create insight cards with proper text
    insight_html = f"""
    <div class="insight-card">
        <strong>📊 Score Analysis:</strong> {grade_message}
    </div>
    
    <div class="insight-card">
        <strong>⏰ Study Pattern:</strong> You studied {hours} hours. 
        {"Great consistency! 🌟" if hours >= 6 else "Try to increase study time to 6+ hours 📚"}
    </div>
    
    <div class="insight-card">
        <strong>📋 Attendance Impact:</strong> Your attendance is {attendance}%. 
        {"Excellent! Keep it up! 👏" if attendance >= 85 else "Higher attendance leads to better scores 🎯"}
    </div>
    
    <div class="insight-card">
        <strong>😴 Sleep & Performance:</strong> You sleep {sleep} hours.
        {"Perfect for learning! 🧠" if sleep >= 7 else "Try to get 7-8 hours of sleep 😊"}
    </div>
    """
    st.markdown(insight_html, unsafe_allow_html=True)

    # =========================
    # KEY FACTORS AFFECTING SCORE
    # =========================
    st.subheader("🔍 Key Factors Affecting Your Score")
    
    factors_html = f"""
    <div class="insight-card">
        <strong>💪 Motivation Level:</strong> {motivation}
        {" - Great! This boosts your performance! 🚀" if motivation == "High" else " - Try setting small daily goals to stay motivated 🎯"}
    </div>
    
    <div class="insight-card">
        <strong>👪 Parental Involvement:</strong> {parent}
        {" - Strong support system! 🤝" if parent == "High" else " - More parental support could improve scores 💕"}
    </div>
    
    <div class="insight-card">
        <strong>📚 Learning Resources:</strong> {resources}
        {" - Excellent resources available! 📖" if resources == "High" else " - Explore free online resources (YouTube, Khan Academy) 💻"}
    </div>
    
    <div class="insight-card">
        <strong>👥 Peer Influence:</strong> {peer}
        {" - Positive peer influence helps! 🌟" if peer == "Positive" else " - Surround yourself with motivated peers 👨‍🎓"}
    </div>
    """
    st.markdown(factors_html, unsafe_allow_html=True)

    # =========================
    # IMPROVEMENT TIPS
    # =========================
    st.subheader("📌 Improvement Tips")
    
    tips = []
    if final_score < 60:
        tips.append("🎯 Increase study hours to at least 6 hours daily")
    if attendance < 75:
        tips.append("🎯 Improve attendance to 85% or higher")
    if motivation != "High":
        tips.append("🎯 Set clear academic goals to boost motivation")
    if resources != "High":
        tips.append("🎯 Use Khan Academy, Coursera, or YouTube for free learning")
    if sleep < 7:
        tips.append("🎯 Maintain 7-8 hours of sleep for better concentration")
    if parent != "High":
        tips.append("🎯 Discuss your progress regularly with parents/guardians")
    
    if tips:
        for tip in tips:
            st.info(tip)
    else:
        st.success("🎉 You're doing everything right! Keep up the great work!")

    # =========================
    # REPORT
    # =========================
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              STUDENT SCORE PREDICTION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 PREDICTED SCORE: {final_score}/100
🎓 PREDICTED GRADE: {grade}
💬 ASSESSMENT: {grade_message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 STUDENT INPUT DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACADEMIC FACTORS:
  ⏰ Hours Studied        : {hours} hours
  📋 Attendance (%)       : {attendance}%
  📈 Previous Score       : {previous}/100
  😴 Sleep Hours          : {sleep} hours

PERSONAL FACTORS:
  💪 Motivation Level     : {motivation}
  👥 Peer Influence       : {peer}
  👪 Parental Involvement : {parent}
  🎓 Parent Education     : {education}

SCHOOL & RESOURCES:
  👨‍🏫 Teacher Quality      : {teacher}
  🏫 School Type          : {school}
  📚 Learning Resources   : {resources}
  ⚽ Extracurricular      : {activities}

ENVIRONMENT FACTORS:
  🌐 Internet Access      : {internet}
  💰 Family Income        : {income}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 RECOMMENDATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    for tip in tips:
        report += f"  ✓ {tip}\n"

    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         GENERATED BY STUDENT SCORE PREDICTOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """

    # Download Button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        st.download_button(
            label="📥 Download Complete Report (TXT)",
            data=report,
            file_name=f"student_report_{final_score}_{grade}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Celebration
    if final_score >= 80:
        st.balloons()
        st.snow()
        st.success("🏆 EXCELLENT WORK! Keep shining! 🌟")
    elif final_score >= 60:
        st.balloons()
        st.success("🎉 Good job! You're making progress!")
    else:
        st.info("💪 Remember: Every expert was once a beginner. Keep working hard!")

    st.markdown("---")
    st.caption("🎓 Student Score Predictor - Helping students achieve their academic goals")
