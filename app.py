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
        "email": "admin@scorepredictor.com",
        "created_at": datetime.now()
    },
    "student1": {
        "password": "pass123",
        "name": "John Doe",
        "role": "student",
        "email": "john@example.com",
        "created_at": datetime.now(),
        "scores": [65, 70, 75]
    },
    "teacher1": {
        "password": "teach123",
        "name": "Ms. Smith",
        "role": "teacher",
        "email": "smith@school.com",
        "created_at": datetime.now()
    },
    "parent1": {
        "password": "parent123",
        "name": "Robert Johnson",
        "role": "parent",
        "email": "parent@family.com",
        "child_name": "Emma Johnson",
        "created_at": datetime.now()
    },
    "parent2": {
        "password": "mom123",
        "name": "Sarah Williams",
        "role": "parent",
        "email": "sarah@family.com",
        "child_name": "Michael Williams",
        "created_at": datetime.now()
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
    if user_data["role"] == "admin":
        st.session_state.is_admin = True

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_name = None
    st.session_state.user_role = None
    st.session_state.user_email = None
    st.session_state.login_time = None
    st.session_state.is_admin = False
    if "child_name" in st.session_state:
        st.session_state.child_name = None

def get_all_users():
    return {k: v for k, v in users_db.items() if k != "admin"}

def delete_user(username):
    if username in users_db and username != "admin":
        del users_db[username]
        return True
    return False

def update_user(username, updated_data):
    if username in users_db:
        users_db[username].update(updated_data)
        return True
    return False

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
    
    # Admin tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "👥 User Management", "📈 Analytics", "⚙️ System Settings", "📝 Activity Logs"])
    
    # Tab 1: Dashboard
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        total_users = len([u for u in users_db if u != "admin"])
        total_students = len([u for u in users_db if users_db[u]["role"] == "student"])
        total_teachers = len([u for u in users_db if users_db[u]["role"] == "teacher"])
        total_parents = len([u for u in users_db if users_db[u]["role"] == "parent"])
        
        with col1:
            st.markdown(f"""
            <div class='stat-card'>
                <h2 style='color: #00FFD1;'>{total_users}</h2>
                <p>Total Users</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='stat-card'>
                <h2 style='color: #00FFD1;'>{total_students}</h2>
                <p>Students</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='stat-card'>
                <h2 style='color: #00FFD1;'>{total_teachers}</h2>
                <p>Teachers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='stat-card'>
                <h2 style='color: #00FFD1;'>{total_parents}</h2>
                <p>Parents</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📊 User Distribution")
        
        # Pie chart for user distribution using matplotlib
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        labels = ['Students', 'Teachers', 'Parents']
        sizes = [total_students, total_teachers, total_parents]
        colors = ['#00FFD1', '#92FE9D', '#FFD700']
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('User Distribution by Role', color='white', pad=20)
        ax1.set_facecolor('none')
        fig1.patch.set_alpha(0)
        st.pyplot(fig1)
        
        # User growth chart
        st.markdown("### User Growth Over Time")
        dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        growth_data = [5, 8, 12, 15, 18, 22, 25, 28, 30, 32, 35, 38]
        
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(dates, growth_data, marker='o', color='#00FFD1', linewidth=2, markersize=8)
        ax2.set_title('Monthly User Registrations', color='white', fontsize=14)
        ax2.set_xlabel('Month', color='white')
        ax2.set_ylabel('New Users', color='white')
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('none')
        fig2.patch.set_alpha(0)
        st.pyplot(fig2)
    
    # Tab 2: User Management
    with tab2:
        st.subheader("👥 Manage Users")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### All Users")
            users_list = get_all_users()
            
            if users_list:
                for username, user_data in users_list.items():
                    with st.expander(f"📌 {username} - {user_data['role'].title()}"):
                        st.write(f"**Name:** {user_data['name']}")
                        st.write(f"**Email:** {user_data['email']}")
                        st.write(f"**Role:** {user_data['role']}")
                        if user_data['role'] == 'parent':
                            st.write(f"**Child Name:** {user_data.get('child_name', 'N/A')}")
                        st.write(f"**Created:** {user_data.get('created_at', 'Unknown')}")
                        
                        col_actions1, col_actions2 = st.columns(2)
                        with col_actions1:
                            if st.button(f"✏️ Edit", key=f"edit_{username}"):
                                st.session_state.edit_user = username
                                st.rerun()
                        with col_actions2:
                            if st.button(f"🗑️ Delete", key=f"delete_{username}"):
                                if delete_user(username):
                                    st.success(f"User {username} deleted successfully!")
                                    st.rerun()
            else:
                st.info("No users found")
        
        with col2:
            st.markdown("### Add New User")
            with st.form("add_user_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email")
                new_role = st.selectbox("Role", ["student", "teacher", "parent"])
                child_name = ""
                if new_role == "parent":
                    child_name = st.text_input("Child's Name")
                
                if st.form_submit_button("➕ Add User"):
                    if new_username and new_password and new_name:
                        if new_username not in users_db:
                            users_db[new_username] = {
                                "password": new_password,
                                "name": new_name,
                                "role": new_role,
                                "email": new_email,
                                "created_at": datetime.now()
                            }
                            if child_name:
                                users_db[new_username]["child_name"] = child_name
                            st.success(f"User {new_username} added successfully!")
                            st.rerun()
                        else:
                            st.error("Username already exists!")
                    else:
                        st.warning("Please fill required fields!")
        
        # Edit user modal
        if hasattr(st.session_state, 'edit_user'):
            st.markdown("---")
            st.subheader(f"✏️ Editing User: {st.session_state.edit_user}")
            user_to_edit = users_db[st.session_state.edit_user]
            
            col_edit1, col_edit2 = st.columns(2)
            with col_edit1:
                edit_name = st.text_input("Name", user_to_edit['name'])
                edit_email = st.text_input("Email", user_to_edit['email'])
            with col_edit2:
                edit_role = st.selectbox("Role", ["student", "teacher", "parent"], 
                                       index=["student", "teacher", "parent"].index(user_to_edit['role']))
                if user_to_edit['role'] == 'parent':
                    edit_child = st.text_input("Child's Name", user_to_edit.get('child_name', ''))
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("💾 Save Changes"):
                    updated_data = {
                        "name": edit_name,
                        "email": edit_email,
                        "role": edit_role
                    }
                    if edit_role == 'parent' and edit_child:
                        updated_data["child_name"] = edit_child
                    if update_user(st.session_state.edit_user, updated_data):
                        st.success("User updated successfully!")
                        del st.session_state.edit_user
                        st.rerun()
            with col_btn2:
                if st.button("❌ Cancel"):
                    del st.session_state.edit_user
                    st.rerun()
    
    # Tab 3: Analytics
    with tab3:
        st.subheader("📈 System Analytics")
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model Accuracy", "87.5%", "+2.3%")
        with col2:
            st.metric("Total Predictions", "1,234", "+156")
        with col3:
            st.metric("Avg Score Improvement", "15.6%", "+3.2%")
        
        st.markdown("---")
        
        # Activity chart
        st.markdown("### User Activity by Role")
        roles = ['Students', 'Teachers', 'Parents']
        activities = [234, 156, 89]
        
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        bars = ax3.bar(roles, activities, color=['#00FFD1', '#92FE9D', '#FFD700'])
        ax3.set_title('Activity by Role', color='white', fontsize=14)
        ax3.set_ylabel('Number of Activities', color='white')
        ax3.tick_params(colors='white')
        ax3.set_facecolor('none')
        fig3.patch.set_alpha(0)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', 
                    ha='center', va='bottom', color='white')
        
        st.pyplot(fig3)
    
    # Tab 4: System Settings
    with tab4:
        st.subheader("⚙️ System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### General Settings")
            maintenance_mode = st.toggle("🔧 Maintenance Mode", False)
            allow_registration = st.toggle("📝 Allow New Registrations", True)
            email_notifications = st.toggle("📧 Email Notifications", True)
            
            if st.button("💾 Save General Settings"):
                st.success("Settings saved successfully!")
        
        with col2:
            st.markdown("### Admin Account")
            st.info("⚠️ Security Settings")
            
            current_admin_pass = st.text_input("Current Password", type="password")
            new_admin_pass = st.text_input("New Password", type="password")
            confirm_admin_pass = st.text_input("Confirm New Password", type="password")
            
            if st.button("🔑 Change Admin Password"):
                if current_admin_pass == users_db["admin"]["password"]:
                    if new_admin_pass == confirm_admin_pass and new_admin_pass:
                        users_db["admin"]["password"] = new_admin_pass
                        st.success("Password changed successfully!")
                    else:
                        st.error("New passwords don't match!")
                else:
                    st.error("Current password is incorrect!")
    
    # Tab 5: Activity Logs
    with tab5:
        st.subheader("📝 Recent Activity Logs")
        
        # Sample activity logs
        logs_data = {
            "Timestamp": [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ],
            "User": ["admin", "student1", "teacher1", "parent1"],
            "Action": ["Logged in", "Predicted score", "Viewed analytics", "Checked child progress"],
            "Status": ["Success", "Success", "Success", "Success"]
        }
        
        log_df = pd.DataFrame(logs_data)
        st.dataframe(log_df, use_container_width=True)
        
        if st.button("📥 Export Logs"):
            st.success("Logs exported successfully!")

# =========================
# SIGNUP PAGE
# =========================
def show_signup_page():
    st.markdown("""
    <style>
    .signup-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        background: rgba(0,0,0,0.3);
        border-radius: 20px;
        border: 1px solid #00FFD1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #00FFD1;'>📝 Create New Account</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='signup-container'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Username *", placeholder="Choose a username")
            email = st.text_input("📧 Email *", placeholder="your@email.com")
            full_name = st.text_input("👨‍🎓 Full Name *", placeholder="Enter your full name")
            password = st.text_input("🔒 Password *", type="password", placeholder="Create a password")
            confirm_password = st.text_input("✓ Confirm Password *", type="password", placeholder="Confirm your password")
            role = st.selectbox("🎯 Select Role", ["student", "teacher", "parent"])
            
            child_name = None
            if role == "parent":
                child_name = st.text_input("👶 Child's Name", placeholder="Enter your child's name")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("✅ CREATE ACCOUNT", use_container_width=True):
                    if username and password and full_name and email:
                        if password == confirm_password:
                            if username not in users_db:
                                users_db[username] = {
                                    "password": password,
                                    "name": full_name,
                                    "role": role,
                                    "email": email,
                                    "created_at": datetime.now()
                                }
                                if child_name:
                                    users_db[username]["child_name"] = child_name
                                st.success("🎉 Account created successfully! Please login.")
                                st.balloons()
                                st.session_state.show_signup = False
                                st.rerun()
                            else:
                                st.error("❌ Username already exists! Please choose another.")
                        else:
                            st.error("❌ Passwords do not match!")
                    else:
                        st.warning("⚠️ Please fill all required fields (*)")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("🔙 Back to Login", use_container_width=True):
                    st.session_state.show_signup = False
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# LOGIN PAGE
# =========================
def show_login_page():
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = "student"
    
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%) !important;
    }
    .stMarkdown, p, div, span, label, h1, h2, h3, h4 {
        color: white !important;
    }
    .stTextInput input {
        background-color: #1a1a2e !important;
        color: white !important;
        border: 1px solid #00FFD1 !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #00C9FF, #92FE9D) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #00FFD1;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Role selection
    st.markdown("<h3 style='text-align: center;'>Select Your Role</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
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
    
    with col4:
        if st.button("🛡️ Admin", key="role_admin", use_container_width=True):
            st.session_state.selected_role = "admin"
            st.rerun()
    
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
        
        if st.session_state.selected_role == "student":
            st.markdown("<h2 style='text-align: center; color: #00FFD1;'>🎓 Student Login</h2>", unsafe_allow_html=True)
        elif st.session_state.selected_role == "teacher":
            st.markdown("<h2 style='text-align: center; color: #00FFD1;'>👨‍🏫 Teacher Login</h2>", unsafe_allow_html=True)
        elif st.session_state.selected_role == "parent":
            st.markdown("<h2 style='text-align: center; color: #00FFD1;'>👨‍👩‍👧 Parent Login</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center; color: #00FFD1;'>🛡️ Admin Login</h2>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔐 LOGIN", use_container_width=True, key="login_btn"):
                if username and password:
                    if username in users_db:
                        if users_db[username]["password"] == password:
                            if users_db[username]["role"] == st.session_state.selected_role:
                                login_user(username, users_db[username])
                                st.success(f"✅ Welcome {users_db[username]['name']}!")
                                st.rerun()
                            else:
                                st.error(f"❌ This account is for {users_db[username]['role']} only!")
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("📝 CREATE NEW ACCOUNT", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()

# =========================
# MAIN APP (Student/Teacher/Parent View)
# =========================
def main_app():
    # If admin, show admin page
    if st.session_state.user_role == "admin":
        show_admin_page()
        return
    
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
    
    # Welcome message
    if st.session_state.user_role == "parent":
        st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
        st.markdown(f"Track and predict **{st.session_state.child_name}'s** exam performance.")
        st.info("💡 **Parent Tip:** Regular parental involvement can improve academic performance by up to 30%!")
    else:
        st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
        st.markdown("Fill the details below to predict exam performance.")
    
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
       
