import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# LOAD MODEL
# =========================
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")

# =========================
# TITLE
# =========================
st.title("🎓 Student Score Predictor")

# =========================
# INPUT FIELDS
# =========================
hours = st.number_input("Hours Studied", 0.0, 24.0)
attendance = st.number_input("Attendance", 0.0, 100.0)
previous = st.number_input("Previous Score", 0.0, 100.0)
sleep = st.number_input("Sleep Hours", 0.0, 12.0)

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
# PREDICTION BUTTON
# =========================
if st.button("Predict Score"):

    # Create input dictionary
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

    # Apply encoding
    input_df = pd.get_dummies(input_df)

    # Match training columns
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # =========================
    # PREDICT
    # =========================
    prediction = model.predict(input_df)

    # =========================
    # FIX UNREALISTIC VALUES
    # =========================
    final_score = max(40, min(100, prediction[0]))

    # Convert to integer
    final_score = int(round(final_score))

    # =========================
    # OUTPUT
    # =========================
    st.success(f"🎯 Predicted Exam Score: {final_score}")
    st.balloons()
    

# =========================
# DONUT CHART
# =========================
remaining = 100 - final_score

fig, ax = plt.subplots()

ax.pie(
    [final_score, remaining],
    labels=["Score", "Remaining"],
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops=dict(width=0.4)   # Makes donut shape
)

ax.set_title("Predicted Score Donut Chart")

st.pyplot(fig)
    
