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
# PREMIUM DARK CSS
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #0F2027, #203A43, #2C5364);
}

/* Global Text */
html, body, [class*="css"] {
    color: white !important;
}

/* Title */
h1 {
    color: #00FFD1 !important;
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

/* Labels */
label {
    color: white !important;
    font-weight: 600;
}

/* Number Inputs */
.stNumberInput input {
    background-color: #111111 !important;
    color: white !important;
    border-radius: 10px;
    border: 1px solid #555;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #111111 !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #555 !important;
}

/* Selectbox Text */
div[data-baseweb="select"] span {
    color: white !important;
}

/* Dropdown Menu */
ul {
    background-color: #111111 !important;
    border-radius: 10px !important;
}

/* Dropdown Items */
li {
    background-color: #111111 !important;
    color: white !important;
}

/* Dropdown Hover */
li:hover {
    background-color: #333333 !important;
    color: #00FFD1 !important;
}

/* Predict Button */
.stButton > button {
    background: linear-gradient(to right, #00C9FF, #92FE9D);
    color: black !important;
    border: none;
    border-radius: 12px;
    height: 3.2em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s ease;
}

/* Button Hover */
.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 18px rgba(0,255,200,0.5);
}

/* Download Button */
.stDownloadButton > button {
    background-color: #111111 !important;
    color: white !important;
    border-radius: 10px;
    border: 1px solid #00FFD1;
    font-weight: bold;
    transition: 0.3s ease;
}

/* Download Hover */
.stDownloadButton > button:hover {
    background-color: #00FFD1 !important;
    color: black !important;
    transform: scale(1.02);
}

/* Progress Bar */
.stProgress > div > div > div > div {
    background-color: #00FFD1;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
try:
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")
except FileNotFoundError:
    st.error("❌ Model files not found! Please make sure 'student_model.pkl' and 'model_columns.pkl' exist in the current directory.")
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
    hours = st.number_input("Hours Studied", min_value=0.0, max_value=24.0, step=0.5)
    attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, step=1.0)
    previous = st.number_input("Previous Score", min_value=0.0, max_value=100.0, step=1.0)
    sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=12.0, step=0.5)

with col2:
    motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
    teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
    school = st.selectbox("School Type", ["Public", "Private"])
    internet = st.selectbox("Internet Access", ["Yes", "No"])

col3, col4 = st.columns(2)

with col3:
    income = st.selectbox("Family Income", ["Low", "Medium", "High"])
    parent = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
    education = st.selectbox("Parent Education", ["School", "College"])

with col4:
    peer = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
    resources = st.selectbox("Learning Resources", ["Low", "Medium", "High"])
    activities = st.selectbox("Extracurricular Activities", ["Yes", "No"])

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

    # One Hot Encoding
    input_df = pd.get_dummies(input_df)

    # Match Model Columns
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # Prediction
    prediction = model.predict(input_df)[0]

    # Score Range
    final_score = max(0, min(100, prediction))
    final_score = int(round(final_score))

    # =========================
    # GRADE SYSTEM
    # =========================
    if final_score >= 90:
        grade = "A+"
        grade_color = "#FFD700"
    elif final_score >= 80:
        grade = "A"
        grade_color = "#92FE9D"
    elif final_score >= 70:
        grade = "B"
        grade_color = "#64E986"
    elif final_score >= 60:
        grade = "C"
        grade_color = "#FFD700"
    elif final_score >= 50:
        grade = "D"
        grade_color = "#FFA500"
    else:
        grade = "F"
        grade_color = "#FF6B6B"

    # =========================
    # RESULT CARD (FIXED HTML)
    # =========================
    result_html = f"""
    <div style='
        background: linear-gradient(135deg, #141E30 0%, #243B55 100%);
        padding: 40px 30px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0px 10px 30px rgba(0,255,200,0.2);
        margin-top: 30px;
        border: 1px solid rgba(0,255,209,0.3);
    '>
        <h3 style='
            color: #00FFD1;
            margin-bottom: 15px;
            letter-spacing: 2px;
            font-size: 20px;
        '>
            📊 PREDICTED EXAM SCORE
        </h3>

        <h1 style='
            color: white;
            font-size: 70px;
            margin: 10px 0;
            font-weight: bold;
        '>
            {final_score}
            <span style='
                font-size: 28px;
                color: #bbbbbb;
            '>
                /100
            </span>
        </h1>

        <div style='
            background: {grade_color};
            display: inline-block;
            padding: 10px 25px;
            border-radius: 50px;
            margin-top: 10px;
        '>
            <h3 style='
                color: black;
                margin: 0;
                font-weight: bold;
            '>
                📘 Predicted Grade : {grade}
            </h3>
        </div>
    </div>
    """

    st.markdown(result_html, unsafe_allow_html=True)

    # =========================
    # PROGRESS BAR
    # =========================
    st.subheader("📈 Score Progress")
    st.progress(final_score / 100)

    # =========================
    # DONUT CHART
    # =========================
    st.subheader("🍩 Score Breakdown")
    fig, ax = plt.subplots(figsize=(6, 6))

    values = [final_score, 100 - final_score]
    labels = ["Your Score", "Remaining"]
    colors = ["#00FFD1", "#2C5364"]
    explode = (0.05, 0)

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        explode=explode,
        wedgeprops=dict(width=0.4, edgecolor='white'),
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )

    for text in texts:
        text.set_color('white')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title("Predicted Score Analysis", color='white', fontsize=14, pad=20)
    ax.axis('equal')

    st.pyplot(fig)

    # =========================
    # INSIGHTS
    # =========================
    st.subheader("💡 Performance Insights")
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        if final_score >= 75:
            st.success("🎉 Excellent performance!")
        elif final_score >= 50:
            st.warning("📚 Good, but room for improvement")
        else:
            st.error("⚠️ Needs significant improvement")
    
    with insight_col2:
        if hours >= 5:
            st.info(f"⏰ Studied {hours} hours - Good consistency!")
        else:
            st.info(f"⏰ Study more - {hours} hours is below average")
    
    with insight_col3:
        if attendance >= 75:
            st.info(f"📖 {attendance}% attendance - Keep it up!")
        else:
            st.info(f"📖 Low attendance ({attendance}%) affects performance")

    # =========================
    # REPORT
    # =========================
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    STUDENT SCORE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 PREDICTED SCORE: {final_score}/100
🎓 PREDICTED GRADE: {grade}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 INPUT DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Hours Studied     : {hours}
📋 Attendance (%)    : {attendance}
📈 Previous Score    : {previous}
😴 Sleep Hours       : {sleep}
💪 Motivation Level  : {motivation}
👨‍🏫 Teacher Quality   : {teacher}
🏫 School Type       : {school}
🌐 Internet Access   : {internet}
💰 Family Income     : {income}
👪 Parental Involvement : {parent}
🎓 Parent Education     : {education}
👥 Peer Influence    : {peer}
📚 Learning Resources : {resources}
⚽ Extracurricular Activities : {activities}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    GENERATED BY STUDENT SCORE PREDICTOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # =========================
    # DOWNLOAD BUTTON
    # =========================
    st.download_button(
        label="📥 Download Full Report (TXT)",
        data=report,
        file_name=f"student_report_score_{final_score}.txt",
        mime="text/plain",
        use_container_width=True
    )

    # =========================
    # CELEBRATION
    # =========================
    if final_score >= 80:
        st.balloons()
        st.snow()
    elif final_score >= 60:
        st.balloons()
    else:
        st.info("💪 Don't give up! Use this prediction as motivation to study harder!")
