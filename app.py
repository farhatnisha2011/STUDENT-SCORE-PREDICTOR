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
    page_title="AI Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# DATABASE
# ==========================================
USER_DB_FILE = "users.json"

default_users = {
    "student1": {
        "password": "pass123",
        "name": "John Student",
        "role": "student",
        "email": "john@school.com"
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
# SESSION
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_register" not in st.session_state:
    st.session_state.show_register = False

# ==========================================
# PREMIUM CSS
# ==========================================
st.markdown("""
<style>

/* Background */

.stApp{
    background:
    linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
}

/* Hide Menu */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* Text */

h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

/* Inputs */

.stTextInput input,
.stNumberInput input{

    background:#111827 !important;
    color:white !important;

    border:1px solid #00FFD1 !important;

    border-radius:12px !important;
}

/* Selectbox */

div[data-baseweb="select"]{

    background:#111827 !important;

    border-radius:12px !important;

    border:1px solid #00FFD1 !important;
}

div[data-baseweb="select"] *{
    color:white !important;
    background:#111827 !important;
}

/* Button */

.stButton button{

    width:100%;

    background:linear-gradient(
        135deg,
        #00C9FF,
        #92FE9D
    ) !important;

    color:black !important;

    font-weight:bold !important;

    border:none !important;

    border-radius:14px !important;

    padding:14px !important;

    transition:0.3s;
}

.stButton button:hover{

    transform:scale(1.03);

    box-shadow:0 0 20px #00FFD1;
}

/* Sidebar */

[data-testid="stSidebar"]{
    background:#0f172a !important;
}

/* Glass */

.glass{

    background:rgba(255,255,255,0.08);

    backdrop-filter: blur(12px);

    border-radius:20px;

    padding:25px;

    border:1px solid rgba(255,255,255,0.15);

    box-shadow:0 8px 32px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SCORE FUNCTION
# ==========================================
def calculate_score(
    hours,
    attendance,
    previous,
    sleep,
    motivation,
    internet
):

    score = 0

    score += min(hours * 5, 30)
    score += attendance * 0.3
    score += previous * 0.2
    score += sleep * 1.5

    motivation_map = {
        "Low": 3,
        "Medium": 6,
        "High": 10
    }

    score += motivation_map[motivation]

    if internet == "Yes":
        score += 5

    return max(0, min(100, int(score)))

# ==========================================
# LOGIN FUNCTION
# ==========================================
def login_user(username):

    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.user_name = users_db[username]["name"]

# ==========================================
# LOGOUT
# ==========================================
def logout_user():

    st.session_state.logged_in = False
    st.rerun()

# ==========================================
# LOGIN PAGE
# ==========================================
def show_login():

    st.markdown("""
    <h1 style='text-align:center;'>
    🎓 AI Student Performance Predictor
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<div class='glass'>", unsafe_allow_html=True)

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("🔐 Login"):

            if username in users_db:

                if users_db[username]["password"] == password:

                    login_user(username)

                    st.success("Login Successful")

                    st.rerun()

                else:

                    st.error("Wrong Password")

            else:

                st.error("Username Not Found")

        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MAIN APP
# ==========================================
def main_app():

    # ======================================
    # SIDEBAR
    # ======================================

    with st.sidebar:

        st.markdown(f"""
        <div class="glass">

        <h2>👤 Profile</h2>

        <p><b>Name:</b>
        {st.session_state.user_name}</p>

        <p><b>Status:</b>
        Active User</p>

        <p><b>Login Time:</b>
        {datetime.now().strftime("%H:%M")}</p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("## 📌 Features")

        st.markdown("""
        - AI Score Prediction
        - Analytics Dashboard
        - Performance Charts
        - Download Report
        - Premium UI
        """)

        if st.button("🚪 Logout"):

            logout_user()

    # ======================================
    # TITLE
    # ======================================

    st.markdown("""
    <h1 style='text-align:center;'>
    🎓 AI Student Performance Predictor
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ======================================
    # TABS
    # ======================================

    tab1, tab2, tab3 = st.tabs([
        "📊 Prediction",
        "📈 Analytics",
        "👤 Profile"
    ])

    # ======================================
    # TAB 1
    # ======================================

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            hours = st.number_input(
                "Study Hours",
                0.0,
                24.0,
                5.0
            )

            attendance = st.number_input(
                "Attendance %",
                0.0,
                100.0,
                80.0
            )

            previous = st.number_input(
                "Previous Score",
                0.0,
                100.0,
                70.0
            )

        with col2:

            sleep = st.number_input(
                "Sleep Hours",
                0.0,
                12.0,
                7.0
            )

            motivation = st.selectbox(
                "Motivation Level",
                ["Low", "Medium", "High"]
            )

            internet = st.selectbox(
                "Internet Access",
                ["No", "Yes"]
            )

        st.markdown("---")

        if st.button(
            "🔮 Predict Performance"
        ):

            score = calculate_score(
                hours,
                attendance,
                previous,
                sleep,
                motivation,
                internet
            )

            # ==================================
            # GRADE
            # ==================================

            if score >= 90:
                grade = "A+"
                color = "#00FFD1"

            elif score >= 80:
                grade = "A"
                color = "#92FE9D"

            elif score >= 70:
                grade = "B"
                color = "#FFD700"

            elif score >= 60:
                grade = "C"
                color = "#FFA500"

            else:
                grade = "F"
                color = "#FF6B6B"

            # ==================================
            # RESULT CARD
            # ==================================

            st.markdown(f"""
            <div class="glass">

            <h2 style="
            text-align:center;
            color:#00FFD1;
            ">
            🎯 Predicted Performance
            </h2>

            <h1 style="
            text-align:center;
            font-size:90px;
            font-weight:bold;
            color:white;
            ">
            {score}
            </h1>

            <h3 style="
            text-align:center;
            color:{color};
            ">
            Grade : {grade}
            </h3>

            <hr>

            <p style="text-align:center;">
            AI Analysis:
            Your academic performance shows
            strong improvement potential.
            Stay consistent and focused.
            </p>

            </div>
            """, unsafe_allow_html=True)

            st.progress(score / 100)

            # ==================================
            # CHARTS
            # ==================================

            chart1, chart2 = st.columns(2)

            # DONUT CHART

            with chart1:

                fig, ax = plt.subplots(figsize=(5,5))

                ax.pie(
                    [score, 100-score],
                    labels=["Score", "Remaining"],
                    startangle=90,
                    wedgeprops=dict(width=0.4),
                    autopct="%1.1f%%"
                )

                centre_circle = plt.Circle(
                    (0,0),
                    0.70,
                    fc='black'
                )

                fig.gca().add_artist(
                    centre_circle
                )

                st.pyplot(fig)

            # BAR CHART

            with chart2:

                fig2, ax2 = plt.subplots(figsize=(5,5))

                categories = [
                    "Your Score",
                    "Average",
                    "Target"
                ]

                values = [
                    score,
                    65,
                    90
                ]

                colors = [
                    "#00FFD1",
                    "#FFA500",
                    "#FF6B6B"
                ]

                ax2.bar(
                    categories,
                    values,
                    color=colors
                )

                ax2.set_ylim(0,100)

                st.pyplot(fig2)

            # ==================================
            # INSIGHTS
            # ==================================

            st.markdown("## 📌 Performance Insights")

            if score >= 85:

                st.success(
                    "Excellent performance. Keep it up!"
                )

            elif score >= 70:

                st.info(
                    "Good performance. Improve consistency."
                )

            elif score >= 50:

                st.warning(
                    "Average performance. Focus more."
                )

            else:

                st.error(
                    "Needs serious improvement."
                )

            # ==================================
            # DOWNLOAD REPORT
            # ==================================

            report = f"""
AI STUDENT REPORT

Name:
{st.session_state.user_name}

Predicted Score:
{score}

Grade:
{grade}

Generated On:
{datetime.now()}
"""

            st.download_button(
                "📥 Download Report",
                report,
                file_name="student_report.txt"
            )

    # ======================================
    # TAB 2
    # ======================================

    with tab2:

        st.markdown("""
        <div class='glass'>
        <h2>📈 Analytics Dashboard</h2>

        <p>
        This dashboard helps students
        analyze their academic growth.
        </p>

        </div>
        """, unsafe_allow_html=True)

        data = pd.DataFrame({

            "Subjects": [
                "Math",
                "Science",
                "English",
                "Computer"
            ],

            "Marks": [
                78,
                85,
                72,
                90
            ]
        })

        st.dataframe(data)

        fig3, ax3 = plt.subplots(figsize=(8,4))

        ax3.plot(
            data["Subjects"],
            data["Marks"],
            marker="o"
        )

        ax3.set_ylim(0,100)

        st.pyplot(fig3)

    # ======================================
    # TAB 3
    # ======================================

    with tab3:

        st.markdown(f"""
        <div class='glass'>

        <h2>👤 User Profile</h2>

        <p><b>Name:</b>
        {st.session_state.user_name}</p>

        <p><b>Username:</b>
        {st.session_state.username}</p>

        <p><b>Status:</b>
        Premium Dashboard User</p>

        <p><b>System:</b>
        AI Powered Prediction</p>

        </div>
        """, unsafe_allow_html=True)

    # ======================================
    # FOOTER
    # ======================================

    st.markdown("""
    <hr>

    <center>

    Made with ❤️ using Streamlit

    </center>
    """, unsafe_allow_html=True)

# ==========================================
# ROUTING
# ==========================================
if st.session_state.logged_in:

    main_app()

else:

    show_login()
