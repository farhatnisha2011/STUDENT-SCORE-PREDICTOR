import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
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
# DATABASE FILE
# ==========================================
USER_DB_FILE = "users.json"

# ==========================================
# DEFAULT USERS
# ==========================================
default_users = {
    "student1": {
        "password": "pass123",
        "name": "John Student",
        "email": "john@example.com"
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
# PREMIUM CSS
# ==========================================
st.markdown("""
<style>

/* BACKGROUND */
.stApp{
    background:
    linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
}

/* HIDE DEFAULT */
#MainMenu{ visibility:hidden; }
footer{ visibility:hidden; }

/* TEXT */
h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

/* INPUTS */
.stTextInput input,
.stNumberInput input{
    background:#111827 !important;
    color:white !important;
    border:1px solid #00FFD1 !important;
    border-radius:12px !important;
}

/* SELECTBOX */
div[data-baseweb="select"]{
    background:#111827 !important;
    border-radius:12px !important;
    border:1px solid #00FFD1 !important;
}
div[data-baseweb="select"] *{
    color:white !important;
    background:#111827 !important;
}

/* BUTTONS */
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

/* SIDEBAR */
[data-testid="stSidebar"]{
    background:#0f172a !important;
}

/* GLASS EFFECT */
.glass{
    background:rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius:20px;
    padding:25px;
    border:1px solid rgba(255,255,255,0.15);
    box-shadow:0 8px 32px rgba(0,0,0,0.3);
}

/* CUSTOM TABLE */
.custom-table{
    width:100%;
    border-collapse:collapse;
    border-radius:12px;
    overflow:hidden;
    margin-top:16px;
}
.custom-table th{
    background:rgba(0,255,209,0.2) !important;
    color:#00FFD1 !important;
    padding:12px 20px;
    text-align:left;
    font-size:15px;
    font-weight:700;
    border-bottom:2px solid #00FFD1;
}
.custom-table td{
    background:rgba(255,255,255,0.04) !important;
    color:white !important;
    padding:11px 20px;
    border-bottom:1px solid rgba(255,255,255,0.08);
    font-size:14px;
}
.custom-table tr:hover td{
    background:rgba(0,255,209,0.07) !important;
}
.badge{
    display:inline-block;
    padding:3px 10px;
    border-radius:20px;
    font-size:13px;
    font-weight:bold;
}

/* FIX: matplotlib chart white bg override */
.stImage img, .element-container img {
    border-radius: 16px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SCORE CALCULATION
# ==========================================
def calculate_score(hours, attendance, previous, sleep, motivation, internet):
    score = 0
    score += min(hours * 5, 30)
    score += attendance * 0.3
    score += previous * 0.2
    score += sleep * 1.5
    motivation_map = {"Low": 3, "Medium": 6, "High": 10}
    score += motivation_map[motivation]
    if internet == "Yes":
        score += 5
    return max(0, min(100, int(score)))

# ==========================================
# DARK CHART HELPER
# ==========================================
def apply_dark_style(fig, ax):
    """Apply dark theme to any matplotlib figure"""
    BG = "#111827"
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.tick_params(colors='white', labelsize=11)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('rgba(255,255,255,0.1)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return fig, ax

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
        password = st.text_input("Password", type="password")
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
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📝 Create New Account"):
            st.session_state.show_register = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# REGISTER PAGE
# ==========================================
def show_register():
    st.markdown("""
    <h1 style='text-align:center;'>
    📝 Create Account
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        full_name = st.text_input("Full Name")
        username = st.text_input("Create Username")
        email = st.text_input("Email")
        password = st.text_input("Create Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        if st.button("✅ Register"):
            if username in users_db:
                st.error("Username already exists")
            elif password != confirm:
                st.error("Passwords do not match")
            else:
                users_db[username] = {
                    "password": password,
                    "name": full_name,
                    "email": email
                }
                save_users(users_db)
                st.success("Account Created Successfully")
                st.session_state.show_register = False
                st.rerun()
        if st.button("🔙 Back to Login"):
            st.session_state.show_register = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MAIN APP
# ==========================================
def main_app():

    # SIDEBAR
    with st.sidebar:
        st.markdown(f"""
        <div class="glass">
        <h2>👤 Profile</h2>
        <p><b>Name:</b> {st.session_state.user_name}</p>
        <p><b>Status:</b> Active User</p>
        <p><b>Login Time:</b> {datetime.now().strftime("%H:%M")}</p>
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

    # TITLE
    st.markdown("""
    <h1 style='text-align:center;'>
    🎓 AI Student Performance Predictor
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # TABS
    tab1, tab2, tab3 = st.tabs([
        "📊 Prediction",
        "📈 Analytics",
        "👤 Profile"
    ])

    # ======================================
    # TAB 1 — Prediction
    # ======================================
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            hours = st.number_input("Study Hours", 0.0, 24.0, 5.0)
            attendance = st.number_input("Attendance %", 0.0, 100.0, 80.0)
            previous = st.number_input("Previous Score", 0.0, 100.0, 70.0)
        with col2:
            sleep = st.number_input("Sleep Hours", 0.0, 12.0, 7.0)
            motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
            internet = st.selectbox("Internet Access", ["No", "Yes"])

        st.markdown("---")

        if st.button("🔮 Predict Performance"):
            score = calculate_score(hours, attendance, previous, sleep, motivation, internet)

            if score >= 90:
                grade = "A+"; color = "#00FFD1"
            elif score >= 80:
                grade = "A"; color = "#92FE9D"
            elif score >= 70:
                grade = "B"; color = "#FFD700"
            elif score >= 60:
                grade = "C"; color = "#FFA500"
            else:
                grade = "F"; color = "#FF6B6B"

            st.markdown(f"""
            <div class="glass">
            <h2 style="text-align:center;color:#00FFD1;">🎯 Predicted Performance</h2>
            <h1 style="text-align:center;font-size:90px;font-weight:bold;color:white;">{score}</h1>
            <h3 style="text-align:center;color:{color};">Grade : {grade}</h3>
            <hr>
            <p style="text-align:center;">
            AI Analysis: Your academic performance shows strong improvement potential.
            Stay consistent and focused.
            </p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(score / 100)

            chart1, chart2 = st.columns(2)

            # DONUT CHART (dark)
            with chart1:
                BG = "#111827"
                fig, ax = plt.subplots(figsize=(5,5))
                fig.patch.set_facecolor(BG)
                ax.set_facecolor(BG)
                wedges, texts, autotexts = ax.pie(
                    [score, 100-score],
                    labels=["Score", "Remaining"],
                    startangle=90,
                    wedgeprops=dict(width=0.45, edgecolor=BG, linewidth=2),
                    autopct="%1.1f%%",
                    colors=["#00FFD1", "#1e293b"]
                )
                for t in texts:
                    t.set_color("white")
                    t.set_fontsize(12)
                for at in autotexts:
                    at.set_color("white")
                    at.set_fontweight("bold")
                centre_circle = plt.Circle((0,0), 0.70, fc=BG)
                fig.gca().add_artist(centre_circle)
                ax.text(0, 0, f"{score}", ha='center', va='center',
                        fontsize=30, fontweight='bold', color='white')
                st.pyplot(fig)
                plt.close(fig)

            # BAR CHART (dark)
            with chart2:
                BG = "#111827"
                fig2, ax2 = plt.subplots(figsize=(5,5))
                fig2, ax2 = apply_dark_style(fig2, ax2)
                categories = ["Your Score", "Average", "Target"]
                values = [score, 65, 90]
                colors = ["#00FFD1", "#FFA500", "#FF6B6B"]
                bars = ax2.bar(categories, values, color=colors,
                               width=0.5, edgecolor='none')
                for bar, val in zip(bars, values):
                    ax2.text(bar.get_x() + bar.get_width()/2,
                             bar.get_height() + 1.5,
                             str(val), ha='center', va='bottom',
                             color='white', fontweight='bold', fontsize=13)
                ax2.set_ylim(0, 110)
                ax2.grid(axis='y', color='rgba(255,255,255,0.07)', linewidth=0.8)
                ax2.set_axisbelow(True)
                st.pyplot(fig2)
                plt.close(fig2)

            # INSIGHTS
            st.markdown("## 📌 Performance Insights")
            if score >= 85:
                st.success("Excellent performance. Keep it up!")
            elif score >= 70:
                st.info("Good performance. Improve consistency.")
            elif score >= 50:
                st.warning("Average performance. Focus more.")
            else:
                st.error("Needs serious improvement.")

            # DOWNLOAD REPORT
            report = f"""
AI STUDENT REPORT
Name: {st.session_state.user_name}
Predicted Score: {score}
Grade: {grade}
Generated On: {datetime.now()}
"""
            st.download_button("📥 Download Report", report, file_name="student_report.txt")

    # ======================================
    # TAB 2 — Analytics (FIXED)
    # ======================================
    with tab2:

        st.markdown("""
        <div class='glass'>
        <h2>📈 Analytics Dashboard</h2>
        <p>Track your subject-wise academic performance and trends below.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # DATA
        data = pd.DataFrame({
            "Subjects": ["Math", "Science", "English", "Computer"],
            "Marks":    [78, 85, 72, 90]
        })

        # ── STYLED HTML TABLE (replaces plain st.dataframe) ──
        def get_badge(mark):
            if mark >= 85:
                return f"<span class='badge' style='background:rgba(0,255,209,0.2);color:#00FFD1;'>Excellent</span>"
            elif mark >= 70:
                return f"<span class='badge' style='background:rgba(255,215,0,0.2);color:#FFD700;'>Good</span>"
            else:
                return f"<span class='badge' style='background:rgba(255,107,107,0.2);color:#FF6B6B;'>Needs Work</span>"

        rows = ""
        for _, row in data.iterrows():
            badge = get_badge(row["Marks"])
            bar_w = int(row["Marks"])
            rows += f"""
            <tr>
              <td><b>{row['Subjects']}</b></td>
              <td>
                <div style="display:flex;align-items:center;gap:10px;">
                  <div style="
                    width:{bar_w}%;
                    max-width:160px;
                    height:8px;
                    background:linear-gradient(90deg,#00C9FF,#92FE9D);
                    border-radius:4px;
                  "></div>
                  <span style="color:white;font-weight:bold;">{row['Marks']}</span>
                </div>
              </td>
              <td>{badge}</td>
            </tr>
            """

        st.markdown(f"""
        <table class="custom-table">
          <thead>
            <tr>
              <th>📚 Subject</th>
              <th>📊 Marks / 100</th>
              <th>🏅 Status</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CHARTS ROW ──
        c1, c2 = st.columns(2)

        # LINE CHART — Subject trend
        with c1:
            BG = "#111827"
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            fig3, ax3 = apply_dark_style(fig3, ax3)
            subjects = data["Subjects"].tolist()
            marks    = data["Marks"].tolist()
            ax3.plot(subjects, marks, color="#00FFD1",
                     marker="o", linewidth=2.5, markersize=9,
                     markerfacecolor="#92FE9D", markeredgecolor="#00FFD1")
            ax3.fill_between(subjects, marks, alpha=0.12, color="#00FFD1")
            for i, (s, m) in enumerate(zip(subjects, marks)):
                ax3.annotate(str(m), (s, m), textcoords="offset points",
                             xytext=(0, 10), ha='center',
                             color='white', fontsize=11, fontweight='bold')
            ax3.set_ylim(0, 110)
            ax3.set_title("Subject-wise Performance", color='white',
                          fontsize=13, pad=12)
            ax3.grid(axis='y', color='rgba(255,255,255,0.07)', linewidth=0.8)
            ax3.set_axisbelow(True)
            fig3.tight_layout()
            st.pyplot(fig3)
            plt.close(fig3)

        # BAR CHART — Comparison with average
        with c2:
            BG = "#111827"
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            fig4, ax4 = apply_dark_style(fig4, ax4)
            x = np.arange(len(subjects))
            w = 0.35
            avg = [75, 70, 68, 80]   # class average (sample)
            b1 = ax4.bar(x - w/2, marks, w,
                         color="#00FFD1", label="Your Marks",
                         edgecolor='none')
            b2 = ax4.bar(x + w/2, avg, w,
                         color="#FFA500", label="Class Avg",
                         edgecolor='none', alpha=0.8)
            ax4.set_xticks(x)
            ax4.set_xticklabels(subjects, color='white')
            ax4.set_ylim(0, 115)
            ax4.set_title("You vs Class Average", color='white',
                          fontsize=13, pad=12)
            ax4.legend(facecolor="#111827", edgecolor="none",
                       labelcolor="white", fontsize=10)
            ax4.grid(axis='y', color='rgba(255,255,255,0.07)', linewidth=0.8)
            ax4.set_axisbelow(True)
            fig4.tight_layout()
            st.pyplot(fig4)
            plt.close(fig4)

        # SUMMARY METRICS
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        total_avg = int(sum(data["Marks"]) / len(data["Marks"]))
        top_sub   = data.loc[data["Marks"].idxmax(), "Subjects"]
        low_sub   = data.loc[data["Marks"].idxmin(), "Subjects"]
        highest   = data["Marks"].max()

        for col, emoji, label, val, clr in [
            (m1, "📊", "Average Score", f"{total_avg}", "#00FFD1"),
            (m2, "🏆", "Highest Score", f"{highest}", "#92FE9D"),
            (m3, "⭐", "Top Subject",   top_sub,      "#FFD700"),
            (m4, "📌", "Focus Subject", low_sub,      "#FF6B6B"),
        ]:
            col.markdown(f"""
            <div class='glass' style='text-align:center;padding:18px;'>
              <div style='font-size:28px;'>{emoji}</div>
              <div style='color:rgba(255,255,255,0.6);font-size:12px;
                          margin:4px 0;'>{label}</div>
              <div style='color:{clr};font-size:22px;
                          font-weight:bold;'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    # ======================================
    # TAB 3 — Profile
    # ======================================
    with tab3:
        st.markdown(f"""
        <div class='glass'>
        <h2>👤 User Profile</h2>
        <p><b>Name:</b> {st.session_state.user_name}</p>
        <p><b>Username:</b> {st.session_state.username}</p>
        <p><b>Status:</b> Premium Dashboard User</p>
        <p><b>System:</b> AI Powered Prediction</p>
        </div>
        """, unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
    <hr>
    <center>Made with ❤️ using Streamlit</center>
    """, unsafe_allow_html=True)

# ==========================================
# ROUTING
# ==========================================
if st.session_state.logged_in:
    main_app()
else:
    if st.session_state.show_register:
        show_register()
    else:
        show_login()
