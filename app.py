import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os
import numpy as np

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="centered"
)

# ==========================================
# USER DATABASE FILE
# ==========================================
USER_DB_FILE = "users.json"

default_users = {
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


def load_users():
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "w") as f:
            json.dump(default_users, f, indent=4)
    
    with open(USER_DB_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=4)


users_db = load_users()

# ==========================================
# SESSION STATE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_register" not in st.session_state:
    st.session_state.show_register = False
    
if "show_admin" not in st.session_state:
    st.session_state.show_admin = False

# ==========================================
# PREDICTION FUNCTION (No model needed)
# ==========================================
def predict_score(hours, attendance, previous, sleep, motivation, teacher, 
                  school, internet, income, parent, education, peer, resources, activities):
    """Calculate predicted score without ML model"""
    
    score = 0
    
    # Hours studied (max 25 points)
    score += min(hours * 4, 25)
    
    # Attendance (max 20 points)
    score += attendance * 0.2
    
    # Previous score (max 15 points)
    score += previous * 0.15
    
    # Sleep hours (max 10 points)
    score += min(sleep * 1.5, 10)
    
    # Motivation Level (0-8 points)
    motivation_scores = {"Low": 2, "Medium": 5, "High": 8}
    score += motivation_scores[motivation]
    
    # Teacher Quality (0-8 points)
    teacher_scores = {"Poor": 2, "Average": 5, "Good": 8}
    score += teacher_scores[teacher]
    
    # School Type (0-5 points)
    score += 5 if school == "Private" else 2
    
    # Internet Access (0-5 points)
    score += 5 if internet == "Yes" else 1
    
    # Family Income (0-6 points)
    income_scores = {"Low": 2, "Medium": 4, "High": 6}
    score += income_scores[income]
    
    # Parental Involvement (0-8 points)
    parent_scores = {"Low": 2, "Medium": 5, "High": 8}
    score += parent_scores[parent]
    
    # Parent Education (0-5 points)
    score += 5 if education == "College" else 2
    
    # Peer Influence (0-6 points)
    peer_scores = {"Negative": 1, "Neutral": 3, "Positive": 6}
    score += peer_scores[peer]
    
    # Learning Resources (0-6 points)
    resources_scores = {"Low": 2, "Medium": 4, "High": 6}
    score += resources_scores[resources]
    
    # Extracurricular Activities (0-4 points)
    score += 4 if activities == "Yes" else 0
    
    # Ensure score between 0-100
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
        st.session_state.child_name = user_data.get("child_name", "Child")


def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_name = None
    st.session_state.user_role = None
    st.session_state.user_email = None
    st.session_state.login_time = None
    st.rerun()

# ==========================================
# ADMIN PAGE
# ==========================================
def show_admin_page():
    st.markdown("""
    <style>
    .admin-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='admin-header'><h1 style='color: white;'>🛡️ Admin Dashboard</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👥 Manage Users", "⚙️ Settings"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        total_users = len([u for u in users_db if u != "admin"])
        total_students = len([u for u in users_db if users_db[u]["role"] == "student"])
        total_parents = len([u for u in users_db if users_db[u]["role"] == "parent"])
        
        col1.metric("Total Users", total_users)
        col2.metric("Students", total_students)
        col3.metric("Parents", total_parents)
        
        # Chart
        fig, ax = plt.subplots(figsize=(6, 4))
        roles = ['Students', 'Teachers', 'Parents']
        counts = [
            total_students, 
            len([u for u in users_db if users_db[u]["role"] == "teacher"]), 
            total_parents
        ]
        ax.bar(roles, counts, color=['#00FFD1', '#92FE9D', '#FFD700'])
        ax.set_title('User Distribution', color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)
    
    with tab2:
        st.subheader("User Management")
        for username, user_data in users_db.items():
            if username != "admin":
                with st.expander(f"📌 {username} - {user_data['role']}"):
                    st.write(f"**Name:** {user_data['name']}")
                    st.write(f"**Email:** {user_data['email']}")
                    if user_data['role'] == 'parent':
                        st.write(f"**Child:** {user_data.get('child_name', 'N/A')}")
                    
                    if st.button(f"🗑️ Delete {username}", key=f"del_{username}"):
                        del users_db[username]
                        save_users(users_db)
                        st.rerun()
        
        st.markdown("---")
        st.subheader("Add New User")
        with st.form("add_user"):
            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type="password")
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_role = st.selectbox("Role", ["student", "teacher", "parent"])
            child = ""
            if new_role == "parent":
                child = st.text_input("Child Name")
            
            if st.form_submit_button("➕ Add User"):
                if new_user and new_pass and new_name:
                    if new_user not in users_db:
                        users_db[new_user] = {
                            "password": new_pass,
                            "name": new_name,
                            "role": new_role,
                            "email": new_email
                        }
                        if child:
                            users_db[new_user]["child_name"] = child
                        save_users(users_db)
                        st.success("User added!")
                        st.rerun()
                    else:
                        st.error("Username exists!")
                else:
                    st.warning("Fill required fields!")
    
    with tab3:
        st.subheader("System Settings")
        if st.button("📥 Backup Users Data"):
            st.success("Backup created!")
        if st.button("🔄 Reset to Default Users"):
            # Update the global users_db
            users_db.clear()
            users_db.update(default_users)
            save_users(users_db)
            st.success("Reset successful!")
            st.rerun()

# ==========================================
# LOGIN PAGE
# ==========================================
def show_login_page():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
    }
    h1, h2, h3, h4, p, label, span, div {
        color: white !important;
    }
    .stTextInput input {
        background-color: #111827 !important;
        color: white !important;
        border: 1px solid #00FFD1 !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(to right, #00C9FF, #92FE9D);
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    .stSelectbox div {
        background-color: #111827 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; color: #00FFD1;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        role = st.selectbox("Select Role", ["student", "teacher", "parent", "admin"])
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔐 Login", use_container_width=True):
                if username in users_db:
                    if users_db[username]["password"] == password:
                        if users_db[username]["role"] == role:
                            login_user(username, users_db[username])
                            st.success(f"✅ Welcome {users_db[username]['name']}!")
                            st.rerun()
                        else:
                            st.error(f"❌ This account is for {users_db[username]['role']} only!")
                    else:
                        st.error("❌ Incorrect password!")
                else:
                    st.error("❌ Username not found!")
        
        with col_btn2:
            if st.button("👤 Guest Mode", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "guest"
                st.session_state.user_name = "Guest User"
                st.session_state.user_role = "guest"
                st.session_state.user_email = "guest@temp.com"
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        
        if st.button("📝 Create New Account", use_container_width=True):
            st.session_state.show_register = True
            st.rerun()

# ==========================================
# REGISTER PAGE
# ==========================================
def show_register_page():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
    }
    h1, h2, h3, h4, p, label, span, div {
        color: white !important;
    }
    .stTextInput input {
        background-color: #111827 !important;
        color: white !important;
        border: 1px solid #00FFD1 !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(to right, #00C9FF, #92FE9D);
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; color: #00FFD1;'>📝 Create New Account</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username *", placeholder="Choose a username")
        full_name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input("Email *", placeholder="your@email.com")
        password = st.text_input("Password *", type="password", placeholder="Create a password")
        confirm = st.text_input("Confirm Password *", type="password", placeholder="Confirm password")
        role = st.selectbox("Role", ["student", "teacher", "parent"])
        
        child_name = None
        if role == "parent":
            child_name = st.text_input("Child's Name", placeholder="Enter your child's name")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Register", use_container_width=True):
                if not username or not password or not full_name or not email:
                    st.warning("⚠️ Please fill all required fields!")
                elif password != confirm:
                    st.error("❌ Passwords do not match!")
                elif username in users_db:
                    st.error("❌ Username already exists!")
                else:
                    users_db[username] = {
                        "password": password,
                        "name": full_name,
                        "role": role,
                        "email": email
                    }
                    if child_name:
                        users_db[username]["child_name"] = child_name
                    save_users(users_db)
                    st.success("✅ Account created successfully!")
                    st.balloons()
                    st.session_state.show_register = False
                    st.rerun()
        
        with col_btn2:
            if st.button("🔙 Back to Login", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()

# ==========================================
# MAIN APP
# ==========================================
def main_app():
    # Admin page
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
        if hasattr(st.session_state, 'login_time') and st.session_state.login_time:
            st.markdown(f"**Login Time:** {st.session_state.login_time.strftime('%H:%M:%S')}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
        
        st.markdown("---")
        st.markdown("### 📊 Features")
        st.markdown("""
        ✅ Predict Score  
        ✅ Get Insights  
        ✅ Download Report  
        """)
    
    # Main content
    st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
    
    if st.session_state.user_role == "parent":
        st.info(f"💡 Tracking performance for **{st.session_state.child_name}**")
    else:
        st.info("📚 Fill in the details below to predict your exam score")
    
    st.markdown("---")
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        hours = st.slider("📚 Hours Studied", 0.0, 24.0, 5.0, 0.5)
        attendance = st.slider("📋 Attendance (%)", 0.0, 100.0, 75.0, 1.0)
        previous = st.slider("📈 Previous Score", 0.0, 100.0, 65.0, 1.0)
        sleep = st.slider("😴 Sleep Hours", 0.0, 12.0, 7.0, 0.5)
    
    with col2:
        motivation = st.selectbox("💪 Motivation Level", ["Low", "Medium", "High"])
        teacher = st.selectbox("👨‍🏫 Teacher Quality", ["Poor", "Average", "Good"])
        school = st.selectbox("🏫 School Type", ["Public", "Private"])
        internet = st.selectbox("🌐 Internet Access", ["No", "Yes"])
    
    col3, col4 = st.columns(2)
    
    with col3:
        income = st.selectbox("💰 Family Income", ["Low", "Medium", "High"])
        parent = st.selectbox("👪 Parental Involvement", ["Low", "Medium", "High"])
        education = st.selectbox("🎓 Parent Education", ["School", "College"])
    
    with col4:
        peer = st.selectbox("👥 Peer Influence", ["Negative", "Neutral", "Positive"])
        resources = st.selectbox("📚 Learning Resources", ["Low", "Medium", "High"])
        activities = st.selectbox("⚽ Extracurricular Activities", ["No", "Yes"])
    
    # Predict button
    if st.button("🔮 Predict Score", use_container_width=True):
        
        # Calculate score
        score = predict_score(
            hours, attendance, previous, sleep, motivation, teacher,
            school, internet, income, parent, education, peer, resources, activities
        )
        
        # Grade
        if score >= 90:
            grade = "A+"
            color = "#FFD700"
            message = "🏆 Outstanding performance! Keep it up!"
        elif score >= 80:
            grade = "A"
            color = "#92FE9D"
            message = "🎉 Excellent work! You're doing great!"
        elif score >= 70:
            grade = "B"
            color = "#64E986"
            message = "👍 Good job! A little more effort for an A!"
        elif score >= 60:
            grade = "C"
            color = "#FFD700"
            message = "📚 Not bad! Focus on weaker areas."
        elif score >= 50:
            grade = "D"
            color = "#FFA500"
            message = "⚠️ Needs improvement. Consider studying harder."
        else:
            grade = "F"
            color = "#FF6B6B"
            message = "❌ Failing. Immediate action required!"
        
        # Display result
        st.markdown("---")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); 
                    padding: 30px; border-radius: 20px; text-align: center; 
                    margin: 20px 0; border: 2px solid #00FFD1;">
            <h2 style="color: #00FFD1;">📊 PREDICTED SCORE</h2>
            <h1 style="font-size: 72px; color: white;">{score}<span style="font-size: 24px;">/100</span></h1>
            <div style="background: {color}; display: inline-block; padding: 10px 30px; border-radius: 50px;">
                <h3 style="color: black;">Grade: {grade}</h3>
            </div>
            <p style="color: white; margin-top: 20px;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(score / 100)
        
        # Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            fig, ax = plt.subplots(figsize=(5, 5))
            fig.patch.set_facecolor('#0F2027')
            ax.set_facecolor('#0F2027')
            values = [score, 100 - score]
            labels = ["Your Score", "Remaining"]
            colors = ["#00FFD1", "#2C5364"]
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax.set_title("Score Distribution", color="white", pad=20)
            st.pyplot(fig)
        
        with chart_col2:
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            fig2.patch.set_facecolor('#0F2027')
            ax2.set_facecolor('#0F2027')
            categories = ['Your Score', 'Class Average', 'Target Score']
            values2 = [score, 65, 85]
            ax2.bar(categories, values2, color=['#00FFD1', '#FFA500', '#FF6B6B'])
            ax2.set_ylim(0, 100)
            ax2.set_ylabel('Score', color='white')
            ax2.set_title('Performance Comparison', color='white')
            ax2.tick_params(colors='white')
            st.pyplot(fig2)
        
        # Insights
        st.subheader("💡 Insights")
        
        if hours >= 6:
            st.success(f"✅ Study Time: {hours} hours - Great consistency!")
        else:
            st.warning(f"⚠️ Study Time: {hours} hours - Try to study 6+ hours")
        
        if attendance >= 85:
            st.success(f"✅ Attendance: {attendance}% - Excellent!")
        else:
            st.warning(f"⚠️ Attendance: {attendance}% - Higher attendance = better scores")
        
        if sleep >= 7:
            st.success(f"✅ Sleep: {sleep} hours - Perfect for brain function!")
        else:
            st.warning(f"⚠️ Sleep: {sleep} hours - Aim for 7-8 hours")
        
        # Tips
        if score < 60:
            st.subheader("📌 Improvement Tips")
            if hours < 6:
                st.info("🎯 Increase study hours to 6+ hours daily")
            if attendance < 75:
                st.info("🎯 Improve attendance to 85% or higher")
            if motivation != "High":
                st.info("🎯 Set clear academic goals and stay motivated")
            if sleep < 7:
                st.info("🎯 Get 7-8 hours of sleep for better focus")
        
        # Download report
        report = f"""
STUDENT SCORE REPORT
====================
Name: {st.session_state.user_name}
Role: {st.session_state.user_role}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PREDICTION RESULTS
------------------
Predicted Score: {score}/100
Grade: {grade}

INPUT PARAMETERS
----------------
Hours Studied: {hours}
Attendance: {attendance}%
Previous Score: {previous}
Sleep Hours: {sleep}
Motivation Level: {motivation}
Teacher Quality: {teacher}
School Type: {school}
Internet Access: {internet}
Family Income: {income}
Parental Involvement: {parent}
Parent Education: {education}
Peer Influence: {peer}
Learning Resources: {resources}
Extracurricular Activities: {activities}

ANALYSIS
--------
{message}

Generated by Student Score Predictor
        """
        
        st.download_button(
            "📥 Download Full Report",
            report,
            file_name=f"score_report_{score}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
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
