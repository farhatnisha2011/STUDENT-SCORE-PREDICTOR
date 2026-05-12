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

def toggle_theme():
    if st.session_state.theme_mode == "dark":
        st.session_state.theme_mode = "light"
    else:
        st.session_state.theme_mode = "dark"
    st.rerun()

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

# ==========================================
# PREDICTION FUNCTION
# ==========================================
def calculate_score(hours, attendance, previous, sleep, motivation, teacher, 
                    school, internet, income, parent_involvement, parent_education, 
                    peer, resources, activities):
    
    score = 0
    score += min(hours * 3.5, 25)
    score += attendance * 0.2
    score += previous * 0.15
    score += min(sleep * 1.2, 10)
    
    mot_map = {"Low": 2, "Medium": 5, "High": 8}
    score += mot_map[motivation]
    
    teacher_map = {"Poor": 2, "Average": 5, "Good": 8}
    score += teacher_map[teacher]
    
    score += 5 if school == "Private" else 0
    score += 5 if internet == "Yes" else 0
    
    income_map = {"Low": 2, "Medium": 4, "High": 7}
    score += income_map[income]
    
    parent_map = {"Low": 2, "Medium": 5, "High": 8}
    score += parent_map[parent_involvement]
    
    score += 5 if parent_education == "College" else 0
    
    peer_map = {"Negative": 1, "Neutral": 3, "Positive": 6}
    score += peer_map[peer]
    
    resource_map = {"Low": 2, "Medium": 4, "High": 7}
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
        st.session_state.child_name = user_data.get("child_name", "Child")

def logout_user():
    st.session_state.logged_in = False
    st.rerun()

# ==========================================
# LOGIN PAGE
# ==========================================
def show_login_page():
    # Theme Toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.session_state.theme_mode == "dark":
            if st.button("☀️ Light Mode"):
                toggle_theme()
        else:
            if st.button("🌙 Dark Mode"):
                toggle_theme()
    
    # Title
    st.markdown("<h1 style='text-align: center;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Login Form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>Login</h3>", unsafe_allow_html=True)
        
        role = st.selectbox("Select Role", ["student", "teacher", "parent", "admin"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("🔐 Login", use_container_width=True):
            if username in users_db and users_db[username]["password"] == password:
                if users_db[username]["role"] == role:
                    login_user(username, users_db[username])
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(f"This account is for {users_db[username]['role']} only!")
            else:
                st.error("Invalid username or password!")
        
        st.markdown("---")
        
        if st.button("👤 Continue as Guest", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.username = "guest"
            st.session_state.user_name = "Guest User"
            st.session_state.user_role = "guest"
            st.rerun()
        
        if st.button("📝 Create New Account", use_container_width=True):
            st.session_state.show_register = True
            st.rerun()

# ==========================================
# REGISTER PAGE
# ==========================================
def show_register_page():
    st.markdown("<h1 style='text-align: center;'>📝 Create Account</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["student", "teacher", "parent"])
        
        child_name = None
        if role == "parent":
            child_name = st.text_input("Child's Name")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Register", use_container_width=True):
                if not username or not password or not full_name:
                    st.warning("Please fill all fields!")
                elif password != confirm:
                    st.error("Passwords don't match!")
                elif username in users_db:
                    st.error("Username already exists!")
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
                    st.success("Account created! Please login.")
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
    # Admin Panel
    if st.session_state.user_role == "admin":
        st.markdown("<h1 style='text-align: center;'>🛡️ Admin Panel</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["📊 Dashboard", "👥 Manage Users"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            total_users = len([u for u in users_db if u != "admin"])
            students = len([u for u in users_db if users_db[u]["role"] == "student"])
            parents = len([u for u in users_db if users_db[u]["role"] == "parent"])
            
            col1.metric("Total Users", total_users)
            col2.metric("Students", students)
            col3.metric("Parents", parents)
        
        with tab2:
            for username, user_data in users_db.items():
                if username != "admin":
                    with st.expander(f"{username} ({user_data['role']})"):
                        st.write(f"Name: {user_data['name']}")
                        st.write(f"Email: {user_data['email']}")
                        if st.button(f"Delete {username}", key=f"del_{username}"):
                            del users_db[username]
                            save_users(users_db)
                            st.rerun()
        return
    
    # Regular User Interface
    # Theme Toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.session_state.theme_mode == "dark":
            if st.button("☀️ Light Mode"):
                toggle_theme()
        else:
            if st.button("🌙 Dark Mode"):
                toggle_theme()
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        if st.session_state.user_role == "parent":
            st.markdown(f"**Child:** {st.session_state.child_name}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
        
        st.markdown("---")
        st.markdown("### 📌 Quick Info")
        st.markdown("- Predict exam scores")
        st.markdown("- Get performance insights")
        st.markdown("- Download reports")
    
    # Welcome
    st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
    if st.session_state.user_role == "parent":
        st.info(f"📊 Tracking performance for **{st.session_state.child_name}**")
    else:
        st.info("📝 Fill the form below to predict your exam score")
    
    st.markdown("---")
    
    # Input Form
    with st.form("prediction_form"):
        st.markdown("### 📚 Academic Information")
        
        col1, col2 = st.columns(2)
        with col1:
            hours = st.number_input("Hours Studied (per day)", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
            attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
            previous = st.number_input("Previous Score (%)", min_value=0.0, max_value=100.0, value=65.0, step=1.0)
        
        with col2:
            sleep = st.number_input("Sleep Hours (per day)", min_value=0.0, max_value=12.0, value=7.0, step=0.5)
            motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
            teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
        
        st.markdown("---")
        st.markdown("### 🏫 School & Family Background")
        
        col3, col4 = st.columns(2)
        with col3:
            school = st.selectbox("School Type", ["Public", "Private"])
            internet = st.selectbox("Internet Access", ["No", "Yes"])
            income = st.selectbox("Family Income", ["Low", "Medium", "High"])
        
        with col4:
            parent_involvement = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
            parent_education = st.selectbox("Parent Education", ["School", "College"])
            peer = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
        
        st.markdown("---")
        st.markdown("### 🎯 Additional Resources")
        
        col5, col6 = st.columns(2)
        with col5:
            resources = st.selectbox("Learning Resources", ["Low", "Medium", "High"])
        
        with col6:
            activities = st.selectbox("Extracurricular Activities", ["No", "Yes"])
        
        st.markdown("---")
        
        # Submit button
        submitted = st.form_submit_button("🔮 Predict Score", use_container_width=True)
        
        if submitted:
            # Calculate score
            score = calculate_score(
                hours, attendance, previous, sleep, motivation, teacher,
                school, internet, income, parent_involvement, parent_education,
                peer, resources, activities
            )
            
            # Determine grade
            if score >= 90:
                grade = "A+"
                color = "#FFD700"
                message = "🏆 Outstanding! Keep up the excellent work!"
            elif score >= 80:
                grade = "A"
                color = "#92FE9D"
                message = "🎉 Excellent! You're doing great!"
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
                message = "⚠️ Needs improvement. Study harder!"
            else:
                grade = "F"
                color = "#FF6B6B"
                message = "❌ Failing. Immediate action required!"
            
            # Display results
            st.markdown("---")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); 
                        padding: 30px; border-radius: 20px; text-align: center; 
                        border: 2px solid #00FFD1;">
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
                values = [score, 100 - score]
                labels = ["Your Score", "Remaining"]
                colors = ["#00FFD1", "#2C5364"]
                ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
                ax.set_title("Score Distribution")
                st.pyplot(fig)
            
            with chart_col2:
                fig2, ax2 = plt.subplots(figsize=(5, 5))
                categories = ['Your Score', 'Class Average', 'Target']
                values2 = [score, 65, 85]
                ax2.bar(categories, values2, color=['#00FFD1', '#FFA500', '#FF6B6B'])
                ax2.set_ylim(0, 100)
                ax2.set_ylabel('Score')
                ax2.set_title('Performance Comparison')
                st.pyplot(fig2)
            
            # Insights
            st.subheader("💡 Insights")
            
            if hours >= 6:
                st.success(f"✅ Study Time: {hours} hours - Great!")
            else:
                st.warning(f"⚠️ Study Time: {hours} hours - Try to study 6+ hours")
            
            if attendance >= 85:
                st.success(f"✅ Attendance: {attendance}% - Excellent!")
            else:
                st.warning(f"⚠️ Attendance: {attendance}% - Higher attendance = better scores")
            
            if sleep >= 7:
                st.success(f"✅ Sleep: {sleep} hours - Perfect!")
            else:
                st.warning(f"⚠️ Sleep: {sleep} hours - Aim for 7-8 hours")
            
            # Download report
            report = f"""
STUDENT SCORE REPORT
====================
Name: {st.session_state.user_name}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RESULTS
-------
Predicted Score: {score}/100
Grade: {grade}

INPUTS
------
Hours Studied: {hours}
Attendance: {attendance}%
Previous Score: {previous}
Sleep: {sleep} hours
Motivation: {motivation}
Teacher Quality: {teacher}
School Type: {school}
Internet: {internet}
Family Income: {income}
Parental Involvement: {parent_involvement}
Parent Education: {parent_education}
Peer Influence: {peer}
Learning Resources: {resources}
Activities: {activities}

{message}
"""
            st.download_button("📥 Download Report", report, file_name=f"report_{score}.txt")

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
