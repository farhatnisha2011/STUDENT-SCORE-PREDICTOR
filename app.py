import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# USER DATABASE FILE
# ==========================================
USER_DB_FILE = "users.json"

default_users = {
    "student1": {
        "password": "pass123",
        "name": "John Doe",
        "role": "student",
        "email": "john@example.com"
    },
    "teacher1": {
        "password": "teach123",
        "name": "Ms. Smith",
        "role": "teacher",
        "email": "smith@school.com"
    },
    "parent1": {
        "password": "parent123",
        "name": "Robert Johnson",
        "role": "parent",
        "email": "parent@family.com",
        "child_name": "Emma Johnson"
    }
}

# ==========================================
# LOAD USERS
# ==========================================
def load_users():

    if not os.path.exists(USER_DB_FILE):

        with open(USER_DB_FILE, "w") as f:
            json.dump(default_users, f, indent=4)

    with open(USER_DB_FILE, "r") as f:
        return json.load(f)

# ==========================================
# SAVE USERS
# ==========================================
def save_users(users):

    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

users_db = load_users()

# ==========================================
# SESSION STATES
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_register" not in st.session_state:
    st.session_state.show_register = False

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# ==========================================
# LOGIN FUNCTION
# ==========================================
def login_user(username, user_data):

    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.user_name = user_data["name"]
    st.session_state.user_role = user_data["role"]
    st.session_state.user_email = user_data["email"]
    st.session_state.login_time = datetime.now()

    if user_data["role"] == "parent":
        st.session_state.child_name = user_data.get(
            "child_name",
            "Child"
        )

# ==========================================
# LOGOUT FUNCTION
# ==========================================
def logout_user():

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()

# ==========================================
# THEME CSS
# ==========================================
def apply_theme():

    if st.session_state.theme_mode == "dark":

        st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(
                to right,
                #0F2027,
                #203A43,
                #2C5364
            );
        }

        h1,h2,h3,h4,h5,h6,p,label,span,div {
            color: white !important;
        }

        .stTextInput input,
        .stNumberInput input {
            background-color: #111827 !important;
            color: white !important;
            border: 1px solid #00FFD1 !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #111827 !important;
            color: white !important;
        }

        .stButton button {
            background: linear-gradient(
                to right,
                #00C9FF,
                #92FE9D
            );

            color: black !important;
            font-weight: bold !important;
            border-radius: 10px;
            border: none;
        }

        [data-testid="stSidebar"] {
            background: #111827;
        }

        </style>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(
                to right,
                #f5f7fa,
                #c3cfe2
            );
        }

        h1,h2,h3,h4,h5,h6,p,label,span,div {
            color: black !important;
        }

        .stTextInput input,
        .stNumberInput input {
            background-color: white !important;
            color: black !important;
            border: 1px solid #0F2027 !important;
        }

        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: black !important;
        }

        .stButton button {
            background: linear-gradient(
                to right,
                #0F2027,
                #203A43
            );

            color: white !important;
            font-weight: bold !important;
            border-radius: 10px;
            border: none;
        }

        [data-testid="stSidebar"] {
            background: #e6ecf5;
        }

        </style>
        """, unsafe_allow_html=True)

# ==========================================
# LOGIN PAGE
# ==========================================
def show_login_page():

    apply_theme()

    st.markdown("""
    <h1 style='text-align:center;'>
        🎓 Student Score Predictor
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("---")

    role = st.selectbox(
        "Select Role",
        ["student", "teacher", "parent"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            if username in users_db:

                if users_db[username]["password"] == password:

                    if users_db[username]["role"] == role:

                        login_user(
                            username,
                            users_db[username]
                        )

                        st.success("Login Successful")

                        st.rerun()

                    else:
                        st.error("Wrong role selected")

                else:
                    st.error("Incorrect password")

            else:
                st.error("User not found")

    with col2:

        if st.button(
            "📝 Register",
            use_container_width=True
        ):

            st.session_state.show_register = True
            st.rerun()

# ==========================================
# REGISTER PAGE
# ==========================================
def show_register_page():

    apply_theme()

    st.markdown("""
    <h1 style='text-align:center;'>
        📝 Create Account
    </h1>
    """, unsafe_allow_html=True)

    username = st.text_input("New Username")

    password = st.text_input(
        "New Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    fullname = st.text_input("Full Name")

    email = st.text_input("Email")

    role = st.selectbox(
        "Role",
        ["student", "teacher", "parent"]
    )

    child_name = ""

    if role == "parent":
        child_name = st.text_input("Child Name")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Create Account",
            use_container_width=True
        ):

            if not username or not password or not fullname:

                st.warning("Please fill all fields")

            elif password != confirm:

                st.error("Passwords do not match")

            elif username in users_db:

                st.error("Username already exists")

            else:

                users_db[username] = {
                    "password": password,
                    "name": fullname,
                    "role": role,
                    "email": email
                }

                if role == "parent":
                    users_db[username]["child_name"] = child_name

                save_users(users_db)

                st.success("Account Created Successfully")

                st.session_state.show_register = False

                st.rerun()

    with col2:

        if st.button(
            "🔙 Back",
            use_container_width=True
        ):

            st.session_state.show_register = False
            st.rerun()

# ==========================================
# LOAD MODEL
# ==========================================
@st.cache_resource
def load_model():

    model = joblib.load("student_model.pkl")

    columns = joblib.load("model_columns.pkl")

    return model, columns

# ==========================================
# MAIN APP
# ==========================================
def main_app():

    apply_theme()

    # ======================================
    # TOP THEME SWITCHER
    # ======================================
    top1, top2, top3 = st.columns([8, 1, 1])

    with top2:

        if st.button("🌙", key="dark_btn"):

            st.session_state.theme_mode = "dark"

            st.rerun()

    with top3:

        if st.button("☀️", key="light_btn"):

            st.session_state.theme_mode = "light"

            st.rerun()

    # ======================================
    # SIDEBAR
    # ======================================
    with st.sidebar:

        st.title("👤 User Profile")

        st.write(
            f"**Name:** {st.session_state.user_name}"
        )

        st.write(
            f"**Role:** {st.session_state.user_role}"
        )

        st.write(
            f"**Email:** {st.session_state.user_email}"
        )

        if st.session_state.user_role == "parent":

            st.write(
                f"**Child:** "
                f"{st.session_state.child_name}"
            )

        st.write(
            f"**Login Time:** "
            f"{st.session_state.login_time.strftime('%H:%M:%S')}"
        )

        st.markdown("---")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout_user()

    # ======================================
    # TITLE
    # ======================================
    st.title("🎓 Student Score Predictor")

    st.markdown(
        "Predict student exam performance using ML"
    )

    # ======================================
    # LOAD MODEL
    # ======================================
    try:

        model, columns = load_model()

    except Exception as e:

        st.error(f"Model Loading Error: {e}")

        st.stop()

    # ======================================
    # INPUTS
    # ======================================
    col1, col2 = st.columns(2)

    with col1:

        hours = st.number_input(
            "📚 Hours Studied",
            0.0,
            24.0,
            5.0
        )

        attendance = st.number_input(
            "📋 Attendance %",
            0.0,
            100.0,
            75.0
        )

        previous = st.number_input(
            "📈 Previous Score",
            0.0,
            100.0,
            65.0
        )

        sleep = st.number_input(
            "😴 Sleep Hours",
            0.0,
            12.0,
            7.0
        )

    with col2:

        motivation = st.selectbox(
            "💪 Motivation",
            ["Low", "Medium", "High"]
        )

        teacher = st.selectbox(
            "👨‍🏫 Teacher Quality",
            ["Poor", "Average", "Good"]
        )

        school = st.selectbox(
            "🏫 School Type",
            ["Public", "Private"]
        )

        internet = st.selectbox(
            "🌐 Internet Access",
            ["Yes", "No"]
        )

    col3, col4 = st.columns(2)

    with col3:

        income = st.selectbox(
            "💰 Family Income",
            ["Low", "Medium", "High"]
        )

        parent = st.selectbox(
            "👪 Parental Involvement",
            ["Low", "Medium", "High"]
        )

        education = st.selectbox(
            "🎓 Parent Education",
            ["School", "College"]
        )

    with col4:

        peer = st.selectbox(
            "👥 Peer Influence",
            ["Negative", "Neutral", "Positive"]
        )

        resources = st.selectbox(
            "📚 Learning Resources",
            ["Low", "Medium", "High"]
        )

        activities = st.selectbox(
            "⚽ Extracurricular",
            ["Yes", "No"]
        )

    # ======================================
    # PREDICT BUTTON
    # ======================================
    if st.button(
        "🔮 Predict Score",
        use_container_width=True
    ):

        input_data = {
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

        input_df = pd.DataFrame([input_data])

        input_df = pd.get_dummies(input_df)

        input_df = input_df.reindex(
            columns=columns,
            fill_value=0
        )

        prediction = model.predict(input_df)[0]

        final_score = int(
            round(
                max(0, min(100, prediction))
            )
        )

        # ==================================
        # GRADE
        # ==================================
        if final_score >= 90:
            grade = "A+"
            msg = "🏆 Outstanding Performance!"

        elif final_score >= 80:
            grade = "A"
            msg = "🎉 Excellent Work!"

        elif final_score >= 70:
            grade = "B"
            msg = "👍 Good Performance!"

        elif final_score >= 60:
            grade = "C"
            msg = "📚 Average Performance"

        elif final_score >= 50:
            grade = "D"
            msg = "⚠️ Needs Improvement"

        else:
            grade = "F"
            msg = "❌ Failing Grade"

        # ==================================
        # RESULT CARD
        # ==================================
        st.markdown("---")

        st.metric(
            "📊 Predicted Score",
            f"{final_score}/100"
        )

        st.success(f"Grade: {grade}")

        st.info(msg)

        st.progress(final_score / 100)

        # ==================================
        # CHARTS
        # ==================================
        chart1, chart2 = st.columns(2)

        with chart1:

            fig, ax = plt.subplots(figsize=(5, 5))

            fig.patch.set_facecolor("#0F2027")

            ax.set_facecolor("#0F2027")

            values = [
                final_score,
                100 - final_score
            ]

            labels = [
                "Score",
                "Remaining"
            ]

            colors = [
                "#00FFD1",
                "#203A43"
            ]

            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                colors=colors
            )

            ax.set_title(
                "Score Distribution",
                color="white"
            )

            st.pyplot(fig)

        with chart2:

            fig2, ax2 = plt.subplots(figsize=(5, 5))

            fig2.patch.set_facecolor("#0F2027")

            ax2.set_facecolor("#0F2027")

            categories = [
                "Your Score",
                "Class Avg",
                "Target"
            ]

            values2 = [
                final_score,
                65,
                85
            ]

            colors2 = [
                "#00FFD1",
                "#FFA500",
                "#FF6B6B"
            ]

            ax2.bar(
                categories,
                values2,
                color=colors2
            )

            ax2.set_ylim(0, 100)

            ax2.tick_params(colors="white")

            ax2.set_title(
                "Performance Comparison",
                color="white"
            )

            st.pyplot(fig2)

        # ==================================
        # INSIGHTS
        # ==================================
        st.subheader("💡 Insights")

        if hours < 5:
            st.warning(
                "Increase study hours"
            )

        if attendance < 75:
            st.warning(
                "Improve attendance"
            )

        if sleep < 7:
            st.warning(
                "Take proper sleep"
            )

        if motivation != "High":
            st.info(
                "Stay motivated and focused"
            )

        # ==================================
        # REPORT DOWNLOAD
        # ==================================
        report = f"""
STUDENT REPORT
========================

Name:
{st.session_state.user_name}

Role:
{st.session_state.user_role}

Predicted Score:
{final_score}/100

Grade:
{grade}

Hours Studied:
{hours}

Attendance:
{attendance}

Previous Score:
{previous}

Generated On:
{datetime.now()}
"""

        st.download_button(
            "📥 Download Report",
            data=report,
            file_name="student_report.txt",
            mime="text/plain"
        )

# ==========================================
# APP ROUTING
# ==========================================
if not st.session_state.logged_in:

    if st.session_state.show_register:

        show_register_page()

    else:

        show_login_page()

else:

    main_app()
