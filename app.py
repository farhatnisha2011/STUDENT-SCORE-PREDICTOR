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
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 40px;
        background: linear-gradient(135deg, #141E30 0%, #243B55 100%);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-top: 30px;
    }
    .login-title {
        text-align: center;
        color: #00FFD1;
        margin-bottom: 20px;
        font-size: 28px;
    }
    .role-button {
        background: linear-gradient(135deg, #00C9FF, #92FE9D);
        color: black;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Role selection buttons
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: white; margin-bottom: 15px;">🎯 Select Your Role</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_role1, col_role2, col_role3 = st.columns(3)
    
    with col_role1:
        if st.button("🎓 Student", use_container_width=True, key="btn_student"):
            st.session_state.selected_role = "student"
            st.rerun()
    with col_role2:
        if st.button("👨‍🏫 Teacher", use_container_width=True, key="btn_teacher"):
            st.session_state.selected_role = "teacher"
            st.rerun()
    with col_role3:
        if st.button("👨‍👩‍👧 Parent", use_container_width=True, key="btn_parent"):
            st.session_state.selected_role = "parent"
            st.rerun()
    
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = "student"
    
    # Show selected role with colored text
    st.markdown(f"""
    <div style="text-align: center; margin: 15px 0;">
        <p style="color: #00FFD1; font-size: 18px; font-weight: bold;">✓ Selected: {st.session_state.selected_role.upper()} Login</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Role-specific title with emoji
        if st.session_state.selected_role == "student":
            st.markdown('<h2 class="login-title">🎓 Student Login</h2>', unsafe_allow_html=True)
        elif st.session_state.selected_role == "teacher":
            st.markdown('<h2 class="login-title">👨‍🏫 Teacher Login</h2>', unsafe_allow_html=True)
        else:
            st.markdown('<h2 class="login-title">👨‍👩‍👧 Parent Login</h2>', unsafe_allow_html=True)
        
        username = st.text_input("👤 Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            login_clicked = st.button("📝 Login", use_container_width=True)
        with col_btn2:
            guest_clicked = st.button("👤 Guest Mode", use_container_width=True)
        
        if login_clicked:
            if username and password:
                if username in users_db and users_db[username]["password"] == password:
                    if users_db[username]["role"] == st.session_state.selected_role:
                        login_user(username, users_db[username])
                        st.success(f"✅ Welcome {users_db[username]['name']}!")
                        st.rerun()
                    else:
                        st.error(f"❌ This account is for {users_db[username]['role']} only!")
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please enter both username and password!")
        
        if guest_clicked:
            st.session_state.logged_in = True
            st.session_state.username = "guest"
            st.session_state.user_name = "Guest User"
            st.session_state.user_role = "guest"
            st.session_state.user_email = "guest@temp.com"
            st.session_state.login_time = datetime.now()
            st.success("✅ Logged in as Guest!")
            st.rerun()
        
        # Demo credentials with better visibility
        st.markdown("---")
        st.markdown('<p style="text-align: center; color: #00FFD1; font-weight: bold;">📝 Demo Credentials</p>', unsafe_allow_html=True)
        
        if st.session_state.selected_role == "student":
            st.markdown('<p style="text-align: center; color: #cccccc;">student1 / pass123</p>', unsafe_allow_html=True)
        elif st.session_state.selected_role == "teacher":
            st.markdown('<p style="text-align: center; color: #cccccc;">teacher1 / teach123</p>', unsafe_allow_html=True)
        elif st.session_state.selected_role == "parent":
            st.markdown('<p style="text-align: center; color: #cccccc;">parent1 / parent123 (Emma\'s Parent)<br>parent2 / mom123 (Michael\'s Parent)</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DARK/LIGHT MODE STATE
# =========================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# =========================
# MAIN APP
# =========================
def main_app():
    
    # =========================
    # SIDEBAR STYLING
    # =========================
    if st.session_state.theme_mode == "dark":
        sidebar_css = """
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F2027 0%, #203A43 100%);
        }
        [data-testid="stSidebar"] .stMarkdown, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] label {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(to right, #00C9FF, #92FE9D);
            color: black !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: #00FFD1 !important;
        }
        </style>
        """
    else:
        sidebar_css = """
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f0f2f6 100%);
        }
        [data-testid="stSidebar"] .stMarkdown, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] label {
            color: #1a1a2e !important;
        }
        [data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(to right, #0f3460, #16213e);
            color: white !important;
        }
        </style>
        """
    st.markdown(sidebar_css, unsafe_allow_html=True)
    
    # =========================
    # SIDEBAR CONTENT
    # =========================
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
        
        if st.session_state.user_role == "parent":
            st.markdown("---")
            st.markdown("### 👨‍👩‍👧 Parent Corner")
            st.markdown("""
            - Monitor progress
            - Get parenting tips
            - Track improvement
            """)
        
        st.markdown("---")
        st.markdown("### 📞 Support")
        st.markdown("Email: support@scorepredictor.com")
    
    # =========================
    # THEME TOGGLE BUTTONS
    # =========================
    col_theme1, col_theme2, col_theme3 = st.columns([1, 1, 3])
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
    
    # =========================
    # MAIN CSS
    # =========================
    if st.session_state.theme_mode == "dark":
        theme_css = """
        <style>
        .stApp {
            background: linear-gradient(to right, #0F2027, #203A43, #2C5364);
        }
        html, body, [class*="css"] {
            color: white !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        .stMarkdown, p, div, span {
            color: white !important;
        }
        label, .stSelectbox label, .stNumberInput label {
            color: white !important;
        }
        .stNumberInput input {
            background-color: #111111 !important;
            color: white !important;
            border-radius: 10px;
            border: 1px solid #555;
        }
        div[data-baseweb="select"] > div {
            background-color: #111111 !important;
            color: white !important;
            border-radius: 10px !important;
            border: 1px solid #555 !important;
        }
        div[data-baseweb="select"] span, div[data-baseweb="select"] div {
            color: white !important;
        }
        ul, li {
            background-color: #111111 !important;
            color: white !important;
        }
        li:hover {
            background-color: #333333 !important;
            color: #00FFD1 !important;
        }
        .stButton > button {
            background: linear-gradient(to right, #00C9FF, #92FE9D);
            color: black !important;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            transform: scale(1.03);
            box-shadow: 0px 0px 18px rgba(0,255,200,0.5);
        }
        .stDownloadButton > button {
            background-color: #111111 !important;
            color: white !important;
            border-radius: 10px;
            border: 1px solid #00FFD1;
            font-weight: bold;
        }
        .stProgress > div > div > div > div {
            background-color: #00FFD1;
        }
        .insight-card {
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #00FFD1;
            color: white !important;
        }
        .insight-card strong {
            color: #00FFD1 !important;
        }
        </style>
        """
    else:
        theme_css = """
        <style>
        .stApp {
            background: linear-gradient(to right, #f5f7fa, #c3cfe2);
        }
        html, body, [class*="css"] {
            color: #1a1a2e !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #0f3460 !important;
        }
        label {
            color: #1a1a2e !important;
            font-weight: 600;
        }
        .stNumberInput input {
            background-color: white !important;
            color: #1a1a2e !important;
            border-radius: 10px;
            border: 1px solid #0f3460;
        }
        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: #1a1a2e !important;
            border-radius: 10px !important;
            border: 1px solid #0f3460 !important;
        }
        .stButton > button {
            background: linear-gradient(to right, #0f3460, #16213e);
            color: white !important;
        }
        .insight-card {
            background: rgba(15,52,96,0.1);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #0f3460;
            color: #1a1a2e !important;
        }
        .insight-card strong {
            color: #0f3460 !important;
        }
        </style>
        """
    
    st.markdown(theme_css, unsafe_allow_html=True)
    
    # =========================
    # LOAD MODEL
    # =========================
    try:
        model = joblib.load("student_model.pkl")
        columns = joblib.load("model_columns.pkl")
    except FileNotFoundError:
        st.error("❌ Model files not found!")
        st.stop()
    
    # =========================
    # INPUT FIELDS
    # =========================
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
    
    # =========================
    # PREDICT BUTTON
    # =========================
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
        
        # Result Card
        result_html = f"""
        <div style='background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 40px 30px; border-radius: 25px; text-align: center; box-shadow: 0px 10px 30px rgba(0,200,255,0.2); margin-top: 30px; margin-bottom: 30px; border: 1px solid #00FFD1;'>
            <h3 style='color: #00FFD1; margin-bottom: 15px; letter-spacing: 2px; font-size: 20px;'>📊 PREDICTED EXAM SCORE</h3>
            <h1 style='color: white; font-size: 70px; margin: 10px 0; font-weight: bold;'>{final_score}<span style='font-size: 28px; color: #bbbbbb;'>/100</span></h1>
            <div style='background: {grade_color}; display: inline-block; padding: 10px 25px; border-radius: 50px; margin-top: 10px;'>
                <h3 style='color: black; margin: 0; font-weight: bold;'>📘 Predicted Grade : {grade}</h3>
            </div>
            <p style='color: #cccccc; margin-top: 20px; font-size: 14px;'>{grade_message}</p>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
        # Progress Bar
        st.subheader("📈 Score Progress")
        st.progress(final_score / 100)
        
        # Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("🍩 Score Breakdown")
            fig, ax = plt.subplots(figsize=(5, 5))
            values = [final_score, 100 - final_score]
            labels = ["Your Score", "Remaining"]
            colors = ["#00FFD1", "#2C5364"]
            explode = (0.05, 0)
            text_color = 'white' if st.session_state.theme_mode == "dark" else '#1a1a2e'
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, explode=explode, 
                   wedgeprops=dict(width=0.4, edgecolor=text_color), textprops={'fontsize': 10, 'fontweight': 'bold', 'color': text_color})
            ax.set_title("Score Distribution", color=text_color, fontsize=12, pad=20)
            ax.axis('equal')
            st.pyplot(fig)
        
        with chart_col2:
            st.subheader("📊 Performance Meter")
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            categories = ['Your Score', 'Class Average', 'Target Score']
            values2 = [final_score, 65, 85]
            colors2 = ['#00FFD1' if st.session_state.theme_mode == "dark" else '#0f3460', '#FFA500', '#FF6B6B']
            bars = ax2.bar(categories, values2, color=colors2, alpha=0.7)
            ax2.set_ylim(0, 100)
            ax2.set_ylabel('Score')
            ax2.set_title('Performance Comparison', fontsize=12)
            
            if st.session_state.theme_mode == "dark":
                ax2.tick_params(colors='white')
                ax2.spines['bottom'].set_color('white')
                ax2.spines['left'].set_color('white')
                ax2.yaxis.label.set_color('white')
                ax2.title.set_color('white')
                for label in ax2.get_xticklabels():
                    label.set_color('white')
            else:
                ax2.tick_params(colors='#1a1a2e')
                ax2.spines['bottom'].set_color('#1a1a2e')
                ax2.spines['left'].set_color('#1a1a2e')
                ax2.yaxis.label.set_color('#1a1a2e')
                ax2.title.set_color('#1a1a2e')
                for label in ax2.get_xticklabels():
                    label.set_color('#1a1a2e')
            
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            
            for bar, value in zip(bars, values2):
                height = bar.get_height()
                text_color = 'white' if st.session_state.theme_mode == "dark" else '#1a1a2e'
                ax2.text(bar.get_x() + bar.get_width()/2., height + 2, f'{value}', 
                        ha='center', va='bottom', color=text_color, fontweight='bold')
            st.pyplot(fig2)
        
        # Insights
        st.subheader("💡 Personalized Insights")
        
        insight_html = f"""
        <div class="insight-card">
            <strong>📊 Score Analysis:</strong> {grade_message}
        </div>
        <div class="insight-card">
            <strong>⏰ Study Pattern:</strong> You studied {hours} hours. 
            {"Great consistency! 🌟" if hours >= 6 else "Try to increase study time to 6+ hours 📚"}
        </div>
        <div class="insight-card">
            <strong>📋 Attendance Impact:</strong> Your attendance is {attendance}%. 
            {"Excellent! Keep it up! 👏" if attendance >= 85 else "Higher attendance leads to better scores 🎯"}
        </div>
        <div class="insight-card">
            <strong>😴 Sleep & Performance:</strong> You sleep {sleep} hours.
            {"Perfect for learning! 🧠" if sleep >= 7 else "Try to get 7-8 hours of sleep 😊"}
        </div>
        """
        st.markdown(insight_html, unsafe_allow_html=True)
        
        # Key Factors
        st.subheader("🔍 Key Factors Affecting Your Score")
        
        factors_html = f"""
        <div class="insight-card">
            <strong>💪 Motivation Level:</strong> {motivation}
            {" - Great! Boosts performance! 🚀" if motivation == "High" else " - Set small daily goals to stay motivated 🎯"}
        </div>
        <div class="insight-card">
            <strong>👪 Parental Involvement:</strong> {parent}
            {" - Strong support system! 🤝" if parent == "High" else " - More support could improve scores 💕"}
        </div>
        <div class="insight-card">
            <strong>📚 Learning Resources:</strong> {resources}
            {" - Excellent resources! 📖" if resources == "High" else " - Explore free online resources 💻"}
        </div>
        <div class="insight-card">
            <strong>👥 Peer Influence:</strong> {peer}
            {" - Positive influence helps! 🌟" if peer == "Positive" else " - Surround yourself with motivated peers 👨‍🎓"}
        </div>
        """
        st.markdown(factors_html, unsafe_allow_html=True)
        
        # Tips
        st.subheader("📌 Improvement Tips")
        
        tips = []
        if final_score < 60:
            tips.append("🎯 Increase study hours to at least 6 hours daily")
        if attendance < 75:
            tips.append("🎯 Improve attendance to 85% or higher")
        if motivation != "High":
            tips.append("🎯 Set clear academic goals to boost motivation")
        if resources != "High":
            tips.append("🎯 Use Khan Academy, Coursera, or YouTube for free learning")
        if sleep < 7:
            tips.append("🎯 Maintain 7-8 hours of sleep for better concentration")
        if parent != "High":
            tips.append("🎯 Discuss progress regularly with parents/guardians")
        
        if tips:
            for tip in tips:
                st.info(tip)
        else:
            st.success("🎉 You're doing everything right! Keep up the great work!")
        
        # Report
        report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              STUDENT SCORE PREDICTION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 USER: {st.session_state.user_name}
👔 ROLE: {st.session_state.user_role.title()}
"""
        if st.session_state.user_role == "parent" and "child_name" in st.session_state:
            report += f"👶 CHILD: {st.session_state.child_name}\n"
        
        report += f"""📅 DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 PREDICTED SCORE: {final_score}/100
🎓 PREDICTED GRADE: {grade}
💬 ASSESSMENT: {grade_message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 RECOMMENDATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        for tip in tips:
            report += f"  ✓ {tip}\n"

        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         GENERATED BY STUDENT SCORE PREDICTOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        # Download Button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            st.download_button(
                label="📥 Download Report (TXT)",
                data=report,
                file_name=f"report_{st.session_state.username}_{final_score}_{grade}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # Celebration
        if final_score >= 80:
            st.balloons()
            st.snow()
            st.success("🏆 EXCELLENT WORK! Keep shining! 🌟")
        elif final_score >= 60:
            st.balloons()
            st.success("🎉 Good job! You're making progress!")
        else:
            st.info("💪 Keep working hard! Every expert was once a beginner.")
        
        st.markdown("---")
        st.caption("🎓 Student Score Predictor")

# =========================
# REGISTRATION PAGE
# =========================
def show_register_page():
    st.markdown("""
    <style>
    .register-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 40px;
        background: linear-gradient(135deg, #141E30 0%, #243B55 100%);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="register-container">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #00FFD1;">📝 Create Account</h2>', unsafe_allow_html=True)
        
        new_username = st.text_input("👤 Username", key="reg_username")
        new_password = st.text_input("🔒 Password", type="password", key="reg_password")
        confirm_password = st.text_input("✅ Confirm Password", type="password", key="reg_confirm")
        full_name = st.text_input("📝 Full Name", key="reg_name")
        email = st.text_input("📧 Email", key="reg_email")
        role = st.selectbox("👔 Role", ["student", "teacher", "parent"], key="reg_role")
        
        child_name = None
        if role == "parent":
            child_name = st.text_input("👶 Child's Name", key="reg_child_name")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Register", use_container_width=True):
                if new_username and new_password and full_name:
                    if new_password == confirm_password:
                        if new_username not in users_db:
                            user_data = {
                                "password": new_password,
                                "name": full_name,
                                "role": role,
                                "email": email
                            }
                            if role == "parent" and child_name:
                                user_data["child_name"] = child_name
                            users_db[new_username] = user_data
                            st.success("✅ Registration successful! Please login.")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error("❌ Username already exists!")
                    else:
                        st.error("❌ Passwords do not match!")
                else:
                    st.warning("⚠️ Please fill all fields!")
        
        with col_btn2:
            if st.button("🔙 Back", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

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
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📝 Create New Account", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
else:
    main_app()
