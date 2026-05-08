# Enhanced Student Score Predictor (All Features Added)


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
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")

# =========================
# TITLE
# =========================
st.title("🎓 Student Score Predictor")
st.write("Fill student details to predict exam performance.")

# =========================
# INPUT FIELDS
# =========================
hours = st.number_input("Hours Studied", min_value=0.0, max_value=24.0)
attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0)
previous = st.number_input("Previous Score", min_value=0.0, max_value=100.0)
sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=12.0)

motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
school = st.selectbox("School Type", ["Public", "Private"])
internet = st.selectbox("Internet Access", ["Yes", "No"])
income = st.selectbox("Family Income", ["Low", "Medium", "High"])
parent = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
education = st.selectbox("Parent Education", ["School", "College"])
peer = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
resources = st.selectbox("Learning Resources", ["Low", "Medium", "High"])
activities = st.selectbox("Extracurricular Activities", ["Yes", "No"])

# =========================
# PREDICT BUTTON
# =========================
if st.button("Predict Score"):

    # Input data
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

    # One-hot encoding
    input_df = pd.get_dummies(input_df)

    # Match model columns
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # Predict score
    prediction = model.predict(input_df)[0]

    # Keep score between 0 and 100
    final_score = max(0, min(100, prediction))
    final_score = int(round(final_score))

    # =========================
    # GRADE SYSTEM
    # =========================
    if final_score >= 90:
        grade = "A+"
    elif final_score >= 80:
        grade = "A"
    elif final_score >= 70:
        grade = "B"
    elif final_score >= 60:
        grade = "C"
    elif final_score >= 50:
        grade = "D"
    else:
        grade = "F"

    # =========================
    # OUTPUT
    # =========================
    st.success(f"🎯 Predicted Exam Score: {final_score}")
    st.info(f"📘 Predicted Grade: {grade}")

    # =========================
    # PROGRESS BAR
    # =========================
    st.progress(final_score / 100)

    # =========================
    # DONUT CHART
    # =========================
    fig, ax = plt.subplots()

    values = [final_score, 100 - final_score]
    labels = ["Score", "Remaining"]

    ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        wedgeprops=dict(width=0.4)
    )

    ax.set_title("Predicted Score Analysis")

    st.pyplot(fig)

    # =========================
    # DOWNLOAD REPORT
    # =========================
    report = f"""
    STUDENT SCORE REPORT
    -------------------------
    Predicted Score : {final_score}
    Predicted Grade : {grade}

    Hours Studied : {hours}
    Attendance : {attendance}
    Previous Score : {previous}
    Sleep Hours : {sleep}
    """

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="student_report.txt",
        mime="text/plain"
    )

    # =========================
    # CELEBRATION
    # =========================
    st.balloons()




