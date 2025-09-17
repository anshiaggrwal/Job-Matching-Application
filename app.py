import streamlit as st
import pandas as pd
from pathlib import Path

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Smart Job Portal", page_icon="💼", layout="wide")

# --- DEFINE IMAGE FILE NAME ---
LOGO_IMAGE_FILE = "1m1b.jpg"

# ---------------------- CUSTOM CSS (FINAL VERSION) ----------------------
st.markdown(
    f"""
    <style>
    /* Overall App Background with Gradient */
    .stApp {{
        background: linear-gradient(135deg, #FFF5E1 0%, #F8F9FA 100%);
        background-attachment: fixed;
    }}

    /* Remove Streamlit's default header/padding */
    .stApp > header {{
        background-color: transparent;
    }}
    
    /* Add padding to the main content area */
    [data-testid="stAppViewContainer"] > .main > div:first-child > [data-testid="stVerticalBlock"] {{
        padding: 1rem;
    }}

    /* Custom Header Container (for alignment only, no background) */
    .custom-header {{
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin: 1rem 0 2rem 0; /* Adds space above and below */
    }}

    /* Title with Attractive Gradient Text */
    .title-text {{
        font-size: 3.8rem; /* Made the font even larger */
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #FF4500, #FFB800); /* Brighter gradient */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 1px 1px 5px rgba(255, 255, 255, 0.5); /* Adds a subtle glow */
    }}
    .subtitle-text {{
        font-size: 1.2rem;
        color: #5D6D7E;
        padding-top: 5px;
    }}

    /* Role Selection Cards */
    .role-card {{
        padding: 2rem 1rem;
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.9);
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        height: 190px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 2px solid #FFFFFF;
    }}
    .role-card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 16px 30px rgba(0, 0, 0, 0.15);
        border-color: #FFA500;
    }}
    .role-icon {{ font-size: 45px; margin-bottom: 10px; color: #0D47A1; }}
    .role-title {{ font-size: 20px; font-weight: bold; color: #343A40; }}

    /* Primary Button Styling with Gradient and Hover Effect */
    div.stButton > button:not([kind="secondary"]) {{
        margin-top: 25px; /* Increased the space */
        color: white;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        border: none;
        background: linear-gradient(45deg, #FFA500, #FF8C00);
        box-shadow: 0 4px 14px 0 rgba(255, 165, 0, 0.3);
        transition: all 0.3s ease;
    }}
    div.stButton > button:not([kind="secondary"]):hover {{
        transform: translateY(-3px);
        box-shadow: 0 7px 20px 0 rgba(255, 165, 0, 0.4);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- SESSION STATE ----------------------
if "role" not in st.session_state:
    st.session_state.role = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def go_back():
    st.session_state.role = None
    st.session_state.logged_in = False

# ---------------------- HEADER LAYOUT ----------------------
st.markdown('<div class="custom-header">', unsafe_allow_html=True)
col_logo, col_title_text = st.columns([1, 4])
with col_logo:
    if Path(LOGO_IMAGE_FILE).is_file():
        st.image(LOGO_IMAGE_FILE, width=120)
with col_title_text:
    st.markdown('<p class="title-text" style="margin: 0; padding: 0;">Smart Job Portal</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text" style="margin: 0; padding: 0;">Connecting Talent with Opportunity through AI</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- MAIN CONTENT AREA ----------------------
if st.session_state.role is None:
    st.subheader("Welcome! Choose your role to begin.")
    st.write("")
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown('<div class="role-card"><div class="role-icon">🎓</div><div class="role-title">Student / Job Seeker</div></div>', unsafe_allow_html=True)
        if st.button("Login as Student / Job Seeker →", key="student_btn"):
            st.session_state.role = "student"
            st.rerun()
    with col2:
        st.markdown('<div class="role-card"><div class="role-icon">🏢</div><div class="role-title">Company / Job Provider</div></div>', unsafe_allow_html=True)
        if st.button("Login as Company / Job Provider →", key="company_btn"):
            st.session_state.role = "company"
            st.rerun()
    with col3:
        st.markdown('<div class="role-card"><div class="role-icon">👤</div><div class="role-title">Admin</div></div>', unsafe_allow_html=True)
        if st.button("Login as Admin →", key="admin_btn"):
            st.session_state.role = "admin"
            st.rerun()

    st.markdown("---")
    st.subheader("Portal at a Glance")
    colA, colB, colC = st.columns(3)
    colA.metric("👥 Candidates Registered", "2,340")
    colB.metric("🏢 Companies Onboarded", "120")
    colC.metric("📝 Jobs Posted", "450+")
else:
    # This section no longer has the st.container(border=True)
    st.button("⬅️ Back to Home", on_click=go_back, type="secondary")
    
    if st.session_state.role == "student":
        if not st.session_state.logged_in:
            st.header("🎓 Student / Job Seeker Login")
            with st.form("student_login_form"):
                student_id = st.text_input("Student ID (e.g., STU1001)")
                student_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if student_id == "STU1001" and student_password == "stu@1234":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("❌ Invalid Student ID or Password")
        else:
            st.success("✅ Welcome STU1001! You are logged in.")

    elif st.session_state.role == "company":
        if not st.session_state.logged_in:
            st.header("🏢 Company / Job Provider Login")
            with st.form("company_login_form"):
                company_id = st.text_input("Company ID (e.g., COMP001)")
                company_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if company_id == "COMP001" and company_password == "comp@123":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("❌ Invalid Company ID or Password")
        else:
            st.success("✅ Welcome COMP001! You are logged in.")

    elif st.session_state.role == "admin":
        if not st.session_state.logged_in:
            st.header("👤 Admin Login")
            with st.form("admin_login_form"):
                admin_id = st.text_input("Admin ID (e.g., ADMIN001)")
                admin_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if admin_id == "ADMIN001" and admin_password == "admin@123":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("❌ Invalid Admin ID or Password")
        else:
            st.success("✅ Welcome Admin! You are now logged into the dashboard.")
            st.sidebar.radio("Admin Menu", ["Dashboard", "Manage Data"])