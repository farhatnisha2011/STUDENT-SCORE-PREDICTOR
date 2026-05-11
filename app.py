import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="centered"
)

# =========================
# USER DATABASE
# =========================
users_db = {
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
    },
    "parent2": {
        "password": "mom123",
        "name": "Sarah Williams",
        "role": "parent",
        "email": "sarah@family.com",
        "child_name": "Michael Williams"
    }
}

def check_login_status():
    return st.session_state.get("logged_in", False)

def login_user(username, user_data):
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.user_name = user_data["name"]
    st.session_state.user_role = user_data["role"]
    st.session_state.user_email = user_data["email"]
    st.session_state.login_time = datetime.now()
    if user_data["role"] == "parent":
        st.session_state.child_name = user_data.get("child_name", "Child")

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_name = None
    st.session_state.user_role = None
    st.session_state.user_email = None
    st.session_state.login_time = None
    if "child_name" in st.session_state:
        st.session_state.child_name = None

# =========================
# LOGIN PAGE
# =========================
def show_login_page():
    # Clear any existing session
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = "student"
    
    st.markdown("""
    <style>
    /* Full page background */
    .stApp {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%) !important;
    }
    
    /* All text white */
    .stMarkdown, p, div, span, label, h1, h2, h3, h4 {
        color: white !important;
    }
    
    /* Input fields */
    .stTextInput input {
        background-color: #1a1a2e !important;
        color: white !important;
        border: 1px solid #00FFD1 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Placeholder */
    .stTextInput input::placeholder {
        color: #888 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #00C9FF, #92FE9D) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 10px !important;
        border: none !important;
    }
    
    /* Role buttons specific */
    div[data-testid="column"] .stButton button {
        background: #2c3e50 !important;
        color: white !important;
    }
    
    /* Success/Error messages */
    .stAlert {
        background-color: #1a1a2e !important;
        border-left-color: #00FFD1 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("<h1 style='text-align: center; color: #00FFD1;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Role selection
    st.markdown("<h3 style='text-align: center;'>Select Your Role</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎓 Student", key="role_student", use_container_width=True):
            st.session_state.selected_role = "student"
            st.rerun()
    
    with col2:
        if st.button("👨‍🏫 Teacher", key="role_teacher", use_container_width=True):
            st.session_state.selected_role = "teacher"
            st.rerun()
    
    with col3:
        if st.button("👨‍👩‍👧 Parent", key="role_parent", use_container_width=True):
            st.session_state.selected_role = "parent"
            st.rerun()
    
    # Show selected role
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <span style="background: #00FFD1; color: black; padding: 8px 25px; border-radius: 20px; font-weight: bold;">
            ✓ SELECTED: {st.session_state.selected_role.upper()}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form
    with st.container():
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border-radius: 20px; padding: 30px; max-width: 450px; margin: 0 auto; border: 1px solid #00FFD1;">
        """, unsafe_allow_html=True)
        
        # Role specific title
        if st.session_state.selected_role == "student":
            st.markdown("<h2 style='text-align: center; color: #00FFD1;'>🎓 Student Login</h2>", unsafe_allow_html=True)
        elif st.session_state.selected_role == "teacher":
            st.markdown("<h2 style='text-align: center; color: #00FFD1;'>👨‍🏫 Teacher Login</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center; color: #00FFD1;'>👨‍👩‍👧 Parent Login</h2>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Login fields
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Login button
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔐 LOGIN", use_container_width=True, key="login_btn"):
                if username and password:
                    # Check if user exists
                    if username in users_db:
                        # Check password
                        if users_db[username]["password"] == password:
                            # Check role match
                            if users_db[username]["role"] == st.session_state.selected_role:
                                login_user(username, users_db[username])
                                st.success(f"✅ Welcome {users_db[username]['name']}!")
                                st.rerun()
                            else:
                                st.error(f"❌ This account is for {users_db[username]['role']} only! Please select {users_db[username]['role']} role.")
                        else:
                            st.error("❌ Incorrect password!")
                    else:
                        st.error("❌ Username not found!")
                else:
                    st.warning("⚠️ Please enter username and password!")
        
        with col_btn2:
            if st.button("👤 GUEST MODE", use_container_width=True, key="guest_btn"):
                st.session_state.logged_in = True
                st.session_state.username = "guest"
                st.session_state.user_name = "Guest User"
                st.session_state.user_role = "guest"
                st.session_state.user_email = "guest@temp.com"
                st.session_state.login_time = datetime.now()
                st.success("✅ Logged in as Guest!")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Create Account button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 CREATE NEW ACCOUNT", use_container_width=True):
        st.session_state.show_register = True
        st.rerun()

# =========================
# DARK/LIGHT MODE STATE
# =========================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# =========================
# MAIN APP
# =========================
def main_app():
    
    # Sidebar styling
    sidebar_css = """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F2027 0%, #203A43 100%);
    }
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(to right, #00C9FF, #92FE9D);
        color: black !important;
    }
    </style>
    """
    st.markdown(sidebar_css, unsafe_allow_html=True)
    
    # Sidebar content
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"### 👤 User Profile")
        st.markdown(f"**Name:** {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        st.markdown(f"**Username:** {st.session_state.username}")
        
        if st.session_state.user_role == "parent" and "child_name" in st.session_state:
            st.markdown(f"**Child Name:** {st.session_state.child_name}")
        
        if st.session_state.login_time:
            st.markdown(f"**Login Time:** {st.session_state.login_time.strftime('%H:%M:%S')}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.markdown("""
        - Predict exam score
        - Get insights
        - Track progress
        - Download reports
        """)
        
        st.markdown("---")
        st.markdown("### 📞 Support")
        st.markdown("Email: support@scorepredictor.com")
    
    # Theme toggle
    col_theme1, col_theme2 = st.columns(2)
    with col_theme1:
        if st.button("🌙 Dark Mode", use_container_width=True):
            st.session_state.theme_mode = "dark"
            st.rerun()
    with col_theme2:
        if st.button("☀️ Light Mode", use_container_width=True):
            st.session_state.theme_mode = "light"
            st.rerun()
    
    # Welcome message
    if st.session_state.user_role == "parent":
        st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
        st.markdown(f"Track and predict **{st.session_state.child_name}'s** exam performance.")
        st.info("💡 **Parent Tip:** Regular parental involvement can improve academic performance by up to 30%!")
    else:
        st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
        st.markdown("Fill the details below to predict exam performance.")
    
    # Main CSS
    if st.session_state.theme_mode == "dark":
        main_css = """
        <style>
        .stApp {
            background: linear-gradient(to right, #0F2027, #203A43, #2C5364);
        }
        label {
            color: white !important;
        }
        .stNumberInput input {
            background-color: #111111 !important;
            color: white !important;
            border: 1px solid #00FFD1;
        }
        div[data-baseweb="select"] > div {
            background-color: #111111 !important;
            color: white !important;
        }
        .insight-card {
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #00FFD1;
        }
        </style>
        """
    else:
        main_css = """
        <style>
        .stApp {
            background: linear-gradient(to right, #f5f7fa, #c3cfe2);
        }
        .insight-card {
            background: rgba(15,52,96,0.1);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #0f3460;
        }
        </style>
        """
    st.markdown(main_css, unsafe_allow_html=True)
    
    # Load model
    try:
        model = joblib.load("student_model.pkl")
        columns = joblib.load("model_columns.pkl")
    except FileNotFoundError:
        st.error("❌ Model files not found! Please make sure 'student_model.pkl' and 'model_columns.pkl' exist.")
        st.stop()
    
    # Input fields
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
    
    # Predict button
    if st.button("🔮 Predict Score", use_container_width=True):
        
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
        
        input_df = pd.DataFrame([data])
        input_df = pd.get_dummies(input_df)
        input_df = input_df.reindex(columns=columns, fill_value=0)
        
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
        
        # Result
        result_html = f"""
        <div style='background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 40px 30px; border-radius: 25px; text-align: center; margin: 30px 0; border: 1px solid #00FFD1;'>
            <h3 style='color: #00FFD1;'>📊 PREDICTED EXAM SCORE</h3>
            <h1 style='color: white; font-size: 70px;'>{final_score}<span style='font-size: 28px; color: #bbb;'>/100</span></h1>
            <div style='background: {grade_color}; display: inline-block; padding: 10px 25px; border-radius: 50px;'>
                <h3 style='color: black;'>📘 Grade : {grade}</h3>
            </div>
            <p style='color: #ccc; margin-top: 20px;'>{grade_message}</p>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
        st.subheader("📈 Score Progress")
        st.progress(final_score / 100)
        
        # Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            fig, ax = plt.subplots(figsize=(5, 5))
            values = [final_score, 100 - final_score]
            labels = ["Your Score", "Remaining"]
            colors = ["#00FFD1", "#2C5364"]
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, 
                   wedgeprops=dict(width=0.4))
            ax.set_title("Score Distribution", color='white', pad=20)
            st.pyplot(fig)
        
        with chart_col2:
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            categories = ['Your Score', 'Class Average', 'Target Score']
            values2 = [final_score, 65, 85]
            ax2.bar(categories, values2, color=['#00FFD1', '#FFA500', '#FF6B6B'])
            ax2.set_ylim(0, 100)
            ax2.set_ylabel('Score')
            ax2.set_title('Performance Comparison')
            ax2.tick_params(colors='white')
            for spine in ax2.spines.values():
                spine.set_color('white')
            ax2.yaxis.label.set_color('white')
            ax2.title.set_color('white')
            for label in ax2.get_xticklabels():
                label.set_color('white')
            st.pyplot(fig2)
        
        # Insights
        st.subheader("💡 Insights")
        st.info(f"📊 Score Analysis: {grade_message}")
        st.info(f"⏰ Study Pattern: You studied {hours} hours. {'Great consistency! 🌟' if hours >= 6 else 'Try to increase study time to 6+ hours 📚'}")
        st.info(f"📋 Attendance: {attendance}% - {'Excellent! 👏' if attendance >= 85 else 'Higher attendance = better scores 🎯'}")
        st.info(f"😴 Sleep: {sleep} hours - {'Perfect! 🧠' if sleep >= 7 else 'Try 7-8 hours of sleep 😊'}")
        
        # Tips
        st.subheader("📌 Improvement Tips")
        tips = []
        if final_score < 60:
            tips.append("🎯 Increase study hours to at least 6 hours daily")
        if attendance < 75:
            tips.append("🎯 Improve attendance to 85% or higher")
        if motivation != "High":
            tips.append("🎯 Set clear academic goals")
        if sleep < 7:
            tips.append("🎯 Get 7-8 hours of sleep")
        
        if tips:
            for tip in tips:
                st.info(tip)
        else:
            st.success("🎉 Great work! Keep it up!")
        
        # Download report
        report = f"""
STUDENT SCORE REPORT
-------------------
User: {st.session_state.user_name}
Role: {st.session_state.user_role}
Score: {final_score}/100
Grade: {grade}
        """
        st.download_button("📥 Download Report", report, file_name=f"report_{final_score}.txt")

# =========================
# REGISTRATION PAGE
# =========================
def show_register_page():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 100%) !important;
    }
    label, p, div {
        color: white !important;
    }
    .stTextInput input {
        background-color: #1a1a2e !important;
        color: white !important;
        border: 1px solid #00FFD1 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #00FFD1;'>📝 Create Account</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["student", "teacher", "parent"])
        
        child_name = None
        if role == "parent":
            child_name = st.text_input("Child's Name")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Register"):
                if new_username and new_password and full_name:
                    if new_password == confirm:
                        if new_username not in users_db:
                            users_db[new_username] = {
                                "password": new_password,
                                "name": full_name,
                                "role": role,
                                "email": email
                            }
                            if child_name:
                                users_db[new_username]["child_name"] = child_name
                            st.success("✅ Registration successful! Please login.")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error("Username exists!")
                    else:
                        st.error("Passwords don't match!")
                else:
                    st.warning("Fill all fields!")
        
        with col_btn2:
            if st.button("🔙 Back"):
                st.session_state.show_register = False
                st.rerun()

# =========================
# APP ROUTING
# =========================
if "show_register" not in st.session_state:
    st.session_state.show_register = False

if not check_login_status():
    if st.session_state.show_register:
        show_register_page()
    else:
        show_login_page()
else:
    main_app()
