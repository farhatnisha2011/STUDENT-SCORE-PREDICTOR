import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="wide"
)

# =========================
# USER DATABASE
# =========================
users_db = {
    "admin": {
        "password": "admin123",
        "name": "System Administrator",
        "role": "admin",
        "email": "admin@scorepredictor.com"
    },
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

# =========================
# HELPER FUNCTIONS
# =========================
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

# =========================
# PREDICTION FUNCTION (Simple Formula)
# =========================
def predict_score(hours, attendance, previous, sleep, motivation, teacher, school, internet, income, parent, education, peer, resources, activities):
    # Simple prediction formula (0-100 scale)
    score = 0
    
    # Hours studied (max 30 points)
    score += min(hours * 4, 30)
    
    # Attendance (max 25 points)
    score += attendance * 0.25
    
    # Previous score (max 20 points)
    score += previous * 0.2
    
    # Sleep hours (max 10 points)
    score += min(sleep * 1.5, 10)
    
    # Motivation Level
    motivation_scores = {"Low": 0, "Medium": 5, "High": 10}
    score += motivation_scores[motivation]
    
    # Teacher Quality
    teacher_scores = {"Poor": 0, "Average": 5, "Good": 10}
    score += teacher_scores[teacher]
    
    # School Type
    score += 5 if school == "Private" else 0
    
    # Internet Access
    score += 5 if internet == "Yes" else 0
    
    # Family Income
    income_scores = {"Low": 0, "Medium": 5, "High": 10}
    score += income_scores[income]
    
    # Parental Involvement
    parent_scores = {"Low": 0, "Medium": 5, "High": 10}
    score += parent_scores[parent]
    
    # Parent Education
    score += 5 if education == "College" else 0
    
    # Peer Influence
    peer_scores = {"Negative": 0, "Neutral": 5, "Positive": 10}
    score += peer_scores[peer]
    
    # Learning Resources
    resources_scores = {"Low": 0, "Medium": 5, "High": 10}
    score += resources_scores[resources]
    
    # Extracurricular Activities
    score += 5 if activities == "Yes" else 0
    
    # Ensure score is between 0 and 100
    return min(max(score, 0), 100)

# =========================
# ADMIN PAGE
# =========================
def show_admin_page():
    st.markdown("""
    <style>
    .admin-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stat-card {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='admin-header'><h1 style='color: white;'>🛡️ Admin Dashboard</h1><p style='color: white;'>System Management Panel</p></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👥 User Management", "⚙️ System Settings"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        total_users = len([u for u in users_db if u != "admin"])
        total_students = len([u for u in users_db if users_db[u]["role"] == "student"])
        total_parents = len([u for u in users_db if users_db[u]["role"] == "parent"])
        
        with col1:
            st.metric("Total Users", total_users)
        with col2:
            st.metric("Total Students", total_students)
        with col3:
            st.metric("Total Parents", total_parents)
    
    with tab2:
        st.subheader("User Management")
        
        for username, user_data in users_db.items():
            if username != "admin":
                with st.expander(f"{username} - {user_data['role']}"):
                    st.write(f"Name: {user_data['name']}")
                    st.write(f"Email: {user_data['email']}")
                    if user_data['role'] == 'parent':
                        st.write(f"Child: {user_data.get('child_name', 'N/A')}")
                    if st.button(f"Delete {username}", key=f"del_{username}"):
                        del users_db[username]
                        st.rerun()
    
    with tab3:
        st.subheader("System Settings")
        st.info("Admin settings panel")
        if st.button("Clear All Data"):
            st.warning("This would clear all data in production")

# =========================
# LOGIN PAGE
# =========================
def show_login_page():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
    }
    .stMarkdown, p, div, span, label, h1, h2, h3 {
        color: white !important;
    }
    .stTextInput input {
        background-color: #1a1a2e !important;
        color: white !important;
        border: 1px solid #00FFD1 !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #00C9FF, #92FE9D) !important;
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #00FFD1;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Role selection
    st.markdown("<h3 style='text-align: center;'>Select Your Role</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button("🎓 Student", use_container_width=True):
        st.session_state.selected_role = "student"
        st.rerun()
    if col2.button("👨‍🏫 Teacher", use_container_width=True):
        st.session_state.selected_role = "teacher"
        st.rerun()
    if col3.button("👨‍👩‍👧 Parent", use_container_width=True):
        st.session_state.selected_role = "parent"
        st.rerun()
    if col4.button("🛡️ Admin", use_container_width=True):
        st.session_state.selected_role = "admin"
        st.rerun()
    
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = "student"
    
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <span style="background: #00FFD1; color: black; padding: 8px 25px; border-radius: 20px;">
            ✓ SELECTED: {st.session_state.selected_role.upper()}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.container():
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border-radius: 20px; padding: 30px; max-width: 400px; margin: 0 auto;">
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("🔐 Login", use_container_width=True):
            if username in users_db and users_db[username]["password"] == password:
                if users_db[username]["role"] == st.session_state.selected_role:
                    login_user(username, users_db[username])
                    st.rerun()
                else:
                    st.error(f"This account is for {users_db[username]['role']} only!")
            else:
                st.error("Invalid credentials!")
        
        st.markdown("---")
        
        if st.button("👤 Guest Mode", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.username = "guest"
            st.session_state.user_name = "Guest User"
            st.session_state.user_role = "guest"
            st.rerun()
        
        if st.button("📝 Create New Account", use_container_width=True):
            st.session_state.show_register = True
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# REGISTRATION PAGE
# =========================
def show_register_page():
    st.markdown("<h1 style='text-align: center; color: #00FFD1;'>📝 Create Account</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border-radius: 20px; padding: 30px; max-width: 500px; margin: 0 auto;">
        """, unsafe_allow_html=True)
        
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["student", "teacher", "parent"])
        
        child_name = None
        if role == "parent":
            child_name = st.text_input("Child's Name")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Register", use_container_width=True):
                if new_username and new_password and full_name:
                    if new_password == confirm_password:
                        if new_username not in users_db:
                            users_db[new_username] = {
                                "password": new_password,
                                "name": full_name,
                                "role": role,
                                "email": email
                            }
                            if child_name:
                                users_db[new_username]["child_name"] = child_name
                            st.success("Account created! Please login.")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error("Username exists!")
                    else:
                        st.error("Passwords don't match!")
                else:
                    st.warning("Fill all fields!")
        
        with col2:
            if st.button("🔙 Back", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# MAIN APP
# =========================
def main_app():
    # Show admin page if admin
    if st.session_state.user_role == "admin":
        show_admin_page()
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        st.markdown(f"**Username:** {st.session_state.username}")
        if st.session_state.user_role == "parent" and "child_name" in st.session_state:
            st.markdown(f"**Child:** {st.session_state.child_name}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Features")
        st.markdown("""
        ✅ Predict Exam Score  
        ✅ Get Performance Insights  
        ✅ Track Progress  
        ✅ Download Reports  
        """)
    
    # Welcome
    st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
    
    if st.session_state.user_role == "parent":
        st.info(f"💡 Tracking performance for **{st.session_state.child_name}**")
    else:
        st.info("📚 Fill in the details below to predict your exam score")
    
    # Input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            hours = st.slider("📚 Hours Studied", 0.0, 24.0, 5.0, 0.5)
            attendance = st.slider("📋 Attendance (%)", 0.0, 100.0, 75.0, 1.0)
            previous = st.slider("📈 Previous Score", 0.0, 100.0, 65.0, 1.0)
            sleep = st.slider("😴 Sleep Hours", 0.0, 12.0, 7.0, 0.5)
        
        with col2:
            motivation = st.selectbox("💪 Motivation", ["Low", "Medium", "High"])
            teacher = st.selectbox("👨‍🏫 Teacher Quality", ["Poor", "Average", "Good"])
            school = st.selectbox("🏫 School Type", ["Public", "Private"])
            internet = st.selectbox("🌐 Internet Access", ["No", "Yes"])
        
        col3, col4 = st.columns(2)
        
        with col3:
            income = st.selectbox("💰 Family Income", ["Low", "Medium", "High"])
            parent = st.selectbox("👪 Parent Involvement", ["Low", "Medium", "High"])
            education = st.selectbox("🎓 Parent Education", ["School", "College"])
        
        with col4:
            peer = st.selectbox("👥 Peer Influence", ["Negative", "Neutral", "Positive"])
            resources = st.selectbox("📚 Learning Resources", ["Low", "Medium", "High"])
            activities = st.selectbox("⚽ Activities", ["No", "Yes"])
        
        submitted = st.form_submit_button("🔮 Predict Score", use_container_width=True)
        
        if submitted:
            # Calculate prediction
            score = predict_score(
                hours, attendance, previous, sleep,
                motivation, teacher, school, internet,
                income, parent, education, peer, resources, activities
            )
            
            # Grade
            if score >= 90:
                grade = "A+"
                message = "🏆 Outstanding performance!"
            elif score >= 80:
                grade = "A"
                message = "🎉 Excellent work!"
            elif score >= 70:
                grade = "B"
                message = "👍 Good job!"
            elif score >= 60:
                grade = "C"
                message = "📚 Keep improving!"
            elif score >= 50:
                grade = "D"
                message = "⚠️ Need more effort!"
            else:
                grade = "F"
                message = "❌ Needs significant improvement!"
            
            # Display result
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); 
                        padding: 30px; border-radius: 20px; text-align: center; 
                        margin: 20px 0; border: 2px solid #00FFD1;">
                <h2 style="color: #00FFD1;">PREDICTED SCORE</h2>
                <h1 style="font-size: 72px; color: white;">{int(score)}<span style="font-size: 24px;">/100</span></h1>
                <div style="background: #FFD700; display: inline-block; padding: 10px 30px; border-radius: 50px;">
                    <h3 style="color: black;">Grade: {grade}</h3>
                </div>
                <p style="color: white; margin-top: 20px;">{message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            st.progress(score/100)
            
            # Insights
            st.subheader("💡 Insights")
            st.info(f"📊 Study Time: {hours} hours - {'Good! 👍' if hours >= 6 else 'Try to study more 📚'}")
            st.info(f"📋 Attendance: {attendance}% - {'Excellent! 👏' if attendance >= 85 else 'Work on attendance 🎯'}")
            st.info(f"😴 Sleep: {sleep} hours - {'Perfect! 🧠' if sleep >= 7 else 'Get more rest 😴'}")
            
            # Tips
            if score < 60:
                st.warning("📌 **Tips to improve:**")
                if hours < 6:
                    st.write("- Increase study hours to 6+ daily")
                if attendance < 85:
                    st.write("- Improve class attendance")
                if motivation != "High":
                    st.write("- Set clear academic goals")
            
            # Download report
            report = f"""
            STUDENT SCORE REPORT
            ===================
            Name: {st.session_state.user_name}
            Role: {st.session_state.user_role}
            Predicted Score: {int(score)}/100
            Grade: {grade}
            
            Key Metrics:
            - Hours Studied: {hours}
            - Attendance: {attendance}%
            - Previous Score: {previous}
            - Sleep Hours: {sleep}
            """
            
            st.download_button("📥 Download Report", report, file_name=f"score_report_{int(score)}.txt")

# =========================
# APP ROUTING
# =========================
if "show_register" not in st.session_state:
    st.session_state.show_register = False

if not check_login_status():
    if st.session_state.get("show_register", False):
        show_register_page()
    else:
        show_login_page()
else:
    main_app()
