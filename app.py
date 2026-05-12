import streamlit as st
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
    layout="centered"
)

# ==========================================
# THEME MODE
# ==========================================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# ==========================================
# USER DATABASE
# ==========================================
USER_DB_FILE = "users.json"

default_users = {
    "admin": {
        "password": "admin123",
        "name": "Administrator",
        "role": "admin",
        "email": "admin@school.com"
    },
    "student1": {
        "password": "pass123",
        "name": "John Student",
        "role": "student",
        "email": "john@school.com"
    },
    "teacher1": {
        "password": "teach123",
        "name": "Ms. Smith",
        "role": "teacher",
        "email": "smith@school.com"
    },
    "parent1": {
        "password": "parent123",
        "name": "Robert Parent",
        "role": "parent",
        "email": "parent@family.com",
        "child_name": "Emma"
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

# ==========================================
# APPLY THEME
# ==========================================
def apply_theme():

    if st.session_state.theme_mode == "dark":

        st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(
                135deg,
                #0F2027,
                #203A43,
                #2C5364
            ) !important;
        }

        h1,h2,h3,h4,h5,h6,p,label {
            color: white !important;
        }

        .stMarkdown {
            color: white !important;
        }

        .stTextInput input,
        .stNumberInput input {
            background-color: #1a1a2e !important;
            color: white !important;
            border: 1px solid #00FFD1 !important;
            border-radius: 8px !important;
        }

        div[data-baseweb="select"] {
            background-color: #1a1a2e !important;
            border-radius: 8px !important;
            border: 1px solid #00FFD1 !important;
        }

        div[data-baseweb="select"] * {
            color: white !important;
            background-color: #1a1a2e !important;
        }

        .stButton button {
            background: linear-gradient(
                to right,
                #00C9FF,
                #92FE9D
            ) !important;

            color: black !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            border: none !important;
        }

        .stButton button p {
            color: black !important;
        }

        .stAlert {
            background-color: #1a1a2e !important;
        }

        [data-testid="stSidebar"] {
            background-color: #111827 !important;
        }

        </style>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(
                135deg,
                #f5f7fa,
                #c3cfe2
            ) !important;
        }

        h1,h2,h3,h4,h5,h6,p,label {
            color: #1a1a2e !important;
        }

        .stMarkdown {
            color: #1a1a2e !important;
        }

        .stTextInput input,
        .stNumberInput input {
            background-color: white !important;
            color: #1a1a2e !important;
            border: 1px solid #00C9FF !important;
            border-radius: 8px !important;
        }

        div[data-baseweb="select"] {
            background-color: white !important;
            border-radius: 8px !important;
            border: 1px solid #00C9FF !important;
        }

        div[data-baseweb="select"] * {
            color: black !important;
            background-color: white !important;
        }

        .stButton button {
            background: linear-gradient(
                to right,
                #00C9FF,
                #92FE9D
            ) !important;

            color: black !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            border: none !important;
        }

        .stButton button p {
            color: black !important;
        }

        [data-testid="stSidebar"] {
            background-color: #e6ecf5 !important;
        }

        </style>
        """, unsafe_allow_html=True)

# ==========================================
# THEME TOGGLE
# ==========================================
def toggle_theme():

    if st.session_state.theme_mode == "dark":
        st.session_state.theme_mode = "light"

    else:
        st.session_state.theme_mode = "dark"

    st.rerun()

# ==========================================
# SCORE PREDICTION
# ==========================================
def calculate_score(
    hours,
    attendance,
    previous,
    sleep,
    motivation,
    teacher,
    school,
    internet,
    income,
    parent_involvement,
    parent_education,
    peer,
    resources,
    activities
):

    score = 0

    score += min(hours * 3.5, 25)

    score += attendance * 0.2

    score += previous * 0.15

    score += min(sleep * 1.2, 10)

    motivation_map = {
        "Low": 2,
        "Medium": 5,
        "High": 8
    }

    teacher_map = {
        "Poor": 2,
        "Average": 5,
        "Good": 8
    }

    income_map = {
        "Low": 2,
        "Medium": 4,
        "High": 7
    }

    parent_map = {
        "Low": 2,
        "Medium": 5,
        "High": 8
    }

    peer_map = {
        "Negative": 1,
        "Neutral": 3,
        "Positive": 6
    }

    resource_map = {
        "Low": 2,
        "Medium": 4,
        "High": 7
    }

    score += motivation_map[motivation]

    score += teacher_map[teacher]

    score += 5 if school == "Private" else 0

    score += 5 if internet == "Yes" else 0

    score += income_map[income]

    score += parent_map[parent_involvement]

    score += 5 if parent_education == "College" else 0

    score += peer_map[peer]

    score += resource_map[resources]

    score += 4 if activities == "Yes" else 0

    return max(0, min(100, int(round(score))))

# ==========================================
# LOGIN FUNCTIONS
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
# LOGOUT
# ==========================================
def logout_user():

    theme = st.session_state.theme_mode

    st.session_state.clear()

    st.session_state.theme_mode = theme

    st.session_state.logged_in = False

    st.rerun()

# ==========================================
# LOGIN PAGE
# ==========================================
def show_login_page():

    apply_theme()

    top1, top2 = st.columns([5, 1])

    with top2:

        if st.session_state.theme_mode == "dark":

            if st.button("☀️ Light"):

                toggle_theme()

        else:

            if st.button("🌙 Dark"):

                toggle_theme()

    st.markdown("""
    <h1 style='text-align:center;'>
        🎓 Student Score Predictor
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("---")

    role = st.selectbox(
        "Select Role",
        ["student", "teacher", "parent", "admin"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

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

                    st.error(
                        f"This account is for "
                        f"{users_db[username]['role']}"
                    )

            else:

                st.error("Wrong Password")

        else:

            st.error("Username Not Found")

    st.markdown("---")

    if st.button(
        "📝 Create New Account",
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

    st.markdown("---")

    username = st.text_input("Username")

    full_name = st.text_input("Full Name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

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
            "✅ Register",
            use_container_width=True
        ):

            if not username or not password:

                st.warning("Fill all fields")

            elif password != confirm:

                st.error("Passwords do not match")

            elif username in users_db:

                st.error("Username already exists")

            else:

                users_db[username] = {
                    "password": password,
                    "name": full_name,
                    "role": role,
                    "email": email
                }

                if role == "parent":

                    users_db[username]["child_name"] = child_name

                save_users(users_db)

                st.success("Account Created")

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
# MAIN APP
# ==========================================
def main_app():

    apply_theme()

    # ======================================
    # TOP BAR
    # ======================================
    top1, top2, top3 = st.columns([6, 1, 1])

    with top2:

        if st.session_state.theme_mode == "dark":

            if st.button("☀️"):

                toggle_theme()

        else:

            if st.button("🌙"):

                toggle_theme()

    with top3:

        if st.button("🚪"):

            logout_user()

    # ======================================
    # SIDEBAR
    # ======================================
    with st.sidebar:

        st.title("👤 Profile")

        st.write(
            f"Name: {st.session_state.user_name}"
        )

        st.write(
            f"Role: {st.session_state.user_role}"
        )

        if st.session_state.user_role == "parent":

            st.write(
                f"Child: {st.session_state.child_name}"
            )

        st.markdown("---")

        st.markdown("### 📌 Features")

        st.markdown("- Score Prediction")

        st.markdown("- Report Download")

        st.markdown("- Charts")

        st.markdown("- Theme Switcher")

    # ======================================
    # TITLE
    # ======================================
    st.title("🎓 Student Score Predictor")

    st.info(
        f"Welcome {st.session_state.user_name}"
    )

    st.markdown("---")

    # ======================================
    # INPUTS
    # ======================================
    col1, col2 = st.columns(2)

    with col1:

        hours = st.number_input(
            "Hours Studied",
            0.0,
            24.0,
            5.0
        )

        attendance = st.number_input(
            "Attendance %",
            0.0,
            100.0,
            75.0
        )

        previous = st.number_input(
            "Previous Score",
            0.0,
            100.0,
            65.0
        )

        sleep = st.number_input(
            "Sleep Hours",
            0.0,
            12.0,
            7.0
        )

    with col2:

        motivation = st.selectbox(
            "Motivation Level",
            ["Low", "Medium", "High"]
        )

        teacher = st.selectbox(
            "Teacher Quality",
            ["Poor", "Average", "Good"]
        )

        school = st.selectbox(
            "School Type",
            ["Public", "Private"]
        )

        internet = st.selectbox(
            "Internet Access",
            ["No", "Yes"]
        )

    col3, col4 = st.columns(2)

    with col3:

        income = st.selectbox(
            "Family Income",
            ["Low", "Medium", "High"]
        )

        parent_involvement = st.selectbox(
            "Parental Involvement",
            ["Low", "Medium", "High"]
        )

        parent_education = st.selectbox(
            "Parent Education",
            ["School", "College"]
        )

    with col4:

        peer = st.selectbox(
            "Peer Influence",
            ["Negative", "Neutral", "Positive"]
        )

        resources = st.selectbox(
            "Learning Resources",
            ["Low", "Medium", "High"]
        )

        activities = st.selectbox(
            "Extracurricular Activities",
            ["No", "Yes"]
        )

    st.markdown("---")

    # ======================================
    # PREDICT BUTTON
    # ======================================
    if st.button(
        "🔮 Predict Score",
        use_container_width=True
    ):

        score = calculate_score(
            hours,
            attendance,
            previous,
            sleep,
            motivation,
            teacher,
            school,
            internet,
            income,
            parent_involvement,
            parent_education,
            peer,
            resources,
            activities
        )

        # ==================================
        # GRADE
        # ==================================
        if score >= 90:

            grade = "A+"

            color = "#FFD700"

            message = "🏆 Outstanding!"

            st.balloons()

        elif score >= 80:

            grade = "A"

            color = "#92FE9D"

            message = "🎉 Excellent Work!"

        elif score >= 70:

            grade = "B"

            color = "#64E986"

            message = "👍 Good Job!"

        elif score >= 60:

            grade = "C"

            color = "#FFD700"

            message = "📚 Average Performance"

        elif score >= 50:

            grade = "D"

            color = "#FFA500"

            message = "⚠️ Needs Improvement"

        else:

            grade = "F"

            color = "#FF6B6B"

            message = "❌ Failing Grade"

        # ==================================
        # RESULT CARD
        # ==================================
        st.markdown(f"""
        <div style="
            background: linear-gradient(
                135deg,
                #1a1a2e,
                #16213e
            );

            padding: 30px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid #00FFD1;
        ">

            <h2 style="color:#00FFD1;">
                📊 PREDICTED SCORE
            </h2>

            <h1 style="
                font-size:72px;
                color:white;
            ">
                {score}
                <span style="font-size:24px;">
                    /100
                </span>
            </h1>

            <div style="
                background:{color};
                display:inline-block;
                padding:10px 30px;
                border-radius:50px;
            ">
                <h3 style="color:black;">
                    Grade : {grade}
                </h3>
            </div>

            <p style="
                color:white;
                margin-top:20px;
            ">
                {message}
            </p>

        </div>
        """, unsafe_allow_html=True)

        st.progress(score / 100)

        # ==================================
        # CHARTS
        # ==================================
        chart1, chart2 = st.columns(2)

        with chart1:

            fig, ax = plt.subplots(
                figsize=(5, 5)
            )

            if st.session_state.theme_mode == "dark":

                fig.patch.set_facecolor("#0F2027")

                ax.set_facecolor("#0F2027")

            values = [
                score,
                100 - score
            ]

            labels = [
                "Your Score",
                "Remaining"
            ]

            colors = [
                "#00FFD1",
                "#2C5364"
            ]

            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                colors=colors
            )

            for text in ax.texts:

                text.set_color("white")

            st.pyplot(fig)

        with chart2:

            fig2, ax2 = plt.subplots(
                figsize=(5, 5)
            )

            if st.session_state.theme_mode == "dark":

                fig2.patch.set_facecolor("#0F2027")

                ax2.set_facecolor("#0F2027")

                ax2.tick_params(colors="white")

                ax2.yaxis.label.set_color("white")

                ax2.title.set_color("white")

            categories = [
                "Your Score",
                "Class Avg",
                "Target"
            ]

            values2 = [
                score,
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

            ax2.set_ylabel("Score")

            ax2.set_title(
                "Performance Comparison"
            )

            st.pyplot(fig2)

        # ==================================
        # INSIGHTS
        # ==================================
        st.subheader("💡 Insights")

        if hours >= 6:

            st.success(
                "Excellent study hours!"
            )

        else:

            st.warning(
                "Increase study hours"
            )

        if attendance >= 85:

            st.success(
                "Excellent attendance!"
            )

        else:

            st.warning(
                "Improve attendance"
            )

        if sleep >= 7:

            st.success(
                "Perfect sleep schedule!"
            )

        else:

            st.warning(
                "Take proper sleep"
            )

        # ==================================
        # DOWNLOAD REPORT
        # ==================================
        report = f"""
STUDENT SCORE REPORT
========================

Name:
{st.session_state.user_name}

Role:
{st.session_state.user_role}

Date:
{datetime.now()}

Predicted Score:
{score}/100

Grade:
{grade}

Hours Studied:
{hours}

Attendance:
{attendance}

Previous Score:
{previous}

Sleep Hours:
{sleep}

Motivation:
{motivation}

Teacher Quality:
{teacher}

School Type:
{school}

Internet Access:
{internet}

Family Income:
{income}

Parental Involvement:
{parent_involvement}

Parent Education:
{parent_education}

Peer Influence:
{peer}

Learning Resources:
{resources}

Activities:
{activities}

Message:
{message}
"""

        st.download_button(
            "📥 Download Report",
            report,
            file_name=f"report_{score}.txt"
        )

    st.markdown("---")

    st.markdown("""
    <center>
        © 2026 Student Score Predictor
    </center>
    """, unsafe_allow_html=True)

# ==========================================
# ROUTING
# ==========================================
if not st.session_state.logged_in:

    if st.session_state.show_register:

        show_register_page()

    else:

        show_login_page()

else:

    main_app()
