import streamlit as st
import pandas as pd
from pathlib import Path

# Import custom modules
try:
    import student_module as student
    import company_module as company
    import admin_module as admin
except ImportError as e:
    st.error(f"Error importing modules: {e}. Please ensure all module files are present and correctly named.")
    st.error("Required modules: student_module.py, company_module.py, admin_module.py")
    st.stop()

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Smart Job Portal", page_icon="💼", layout="wide")

# --- DEFINE IMAGE FILE NAME ---
LOGO_IMAGE_FILE = "1m1b.jpg"

# ---------------------- CUSTOM CSS ----------------------
st.markdown(
    """
    <style>
    /* Overall App Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #FFF5E1 0%, #F8F9FA 100%);
        background-attachment: fixed;
    }

    /* Remove Streamlit's default header/padding */
    .stApp > header {
        background-color: transparent;
    }
    
    /* Add padding to the main content area */
    [data-testid="stAppViewContainer"] > .main > div:first-child > [data-testid="stVerticalBlock"] {
        padding: 1rem;
    }

    /* Custom Header Container */
    .custom-header {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin: 1rem 0 2rem 0;
    }

    /* Title with Gradient Text */
    .title-text {
        font-size: 3.8rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #FF4500, #FFB800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 1px 1px 5px rgba(255, 255, 255, 0.5);
    }
    .subtitle-text {
        font-size: 1.2rem;
        color: #2C3E50;
        padding-top: 5px;
        font-weight: 500;
    }
    
    /* Fix general text colors */
    .stApp {
        color: #2C3E50;
    }
    
    /* Ensure all text elements have proper contrast */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #2C3E50 !important;
    }
    
    /* Fix metric text */
    [data-testid="metric-container"] {
        color: #2C3E50 !important;
    }
    
    /* Fix button text */
    .stButton > button {
        color: #2C3E50 !important;
    }

    /* Role Selection Cards */
    .role-card {
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
    }
    .role-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 16px 30px rgba(0, 0, 0, 0.15);
        border-color: #FFA500;
    }
    .role-icon { font-size: 45px; margin-bottom: 10px; color: #0D47A1; }
    .role-title { font-size: 20px; font-weight: bold; color: #343A40; }

    /* Button Styling */
    div.stButton > button:not([kind="secondary"]) {
        margin-top: 25px;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        border: none;
        background: linear-gradient(45deg, #FFA500, #FF8C00);
        box-shadow: 0 4px 14px 0 rgba(255, 165, 0, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:not([kind="secondary"]):hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 20px 0 rgba(255, 165, 0, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- SESSION STATE ----------------------
def initialize_session_state():
    """Initialize session state variables and shared DataFrames."""
    if "role" not in st.session_state:
        st.session_state.role = None
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "details_submitted" not in st.session_state:
        st.session_state.details_submitted = False
    if "announcement" not in st.session_state:
        st.session_state.announcement = "Welcome! Job fair next week. All companies will be present."
    
    # Initialize shared DataFrames if not present
    if 'students' not in st.session_state:
        st.session_state.students = pd.DataFrame(columns=[
            'StudentID', 'Name', 'Email', 'College', 'Degree', 'Year', 'CGPA', 
            'Resume Score', 'Test Score', 'Skills', 'Skills_Count', 
            'Test_Completed', 'Resume_Uploaded', 'Status', 'Registration_Date', 
            'Applications_Count'
        ])
    if 'companies' not in st.session_state:
        st.session_state.companies = pd.DataFrame(columns=[
            'CompanyID', 'Name', 'Industry', 'Company_Size', 'Jobs_Posted', 
            'Total_Applications', 'Approval_Status', 'Registration_Date'
        ])
    if 'jobs' not in st.session_state:
        st.session_state.jobs = pd.DataFrame(columns=[
            'JobID', 'Company', 'Role', 'Location', 'Salary', 'Experience', 
            'Description', 'Openings', 'Status', 'Posted_Date', 'Applications', 
            'Min Resume Score', 'Min Test Score', 'Required Skills'
        ])
    if 'applications' not in st.session_state:
        st.session_state.applications = pd.DataFrame(columns=['JobID', 'StudentID', 'ApplicationDate', 'Status'])
    if 'student_credentials' not in st.session_state:
        st.session_state.student_credentials = {}
    if 'company_credentials' not in st.session_state:
        st.session_state.company_credentials = {}
    if 'admin_credentials' not in st.session_state:
        st.session_state.admin_credentials = {'ADMIN001': 'admin@123'}

def go_back():
    """Reset session state to return to main page."""
    st.session_state.role = None
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.details_submitted = False
    st.rerun()

# ---------------------- HEADER LAYOUT ----------------------
def display_header():
    st.markdown('<div class="custom-header">', unsafe_allow_html=True)
    col_logo_left, col_title_text, col_logo_right = st.columns([1, 4, 1])
    with col_logo_left:
        if Path(LOGO_IMAGE_FILE).is_file():
            st.image(LOGO_IMAGE_FILE, width=200)
        else:
            st.warning(f"Logo image '{LOGO_IMAGE_FILE}' not found. Displaying default icon.")
            st.markdown('<div style="font-size: 80px;">💼</div>', unsafe_allow_html=True)
    with col_title_text:
        st.markdown('<p class="title-text" style="margin: 0; padding: 0;">Smart Job Portal</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle-text" style="margin: 0; padding: 0;">Connecting Talent with Opportunity through AI</p>', unsafe_allow_html=True)
    with col_logo_right:
        if Path("E:\programming\Job Matching App\logo.jpeg").is_file():  # Use the uploaded logo file name
            st.image("logo.jpeg", width=200)  # Adjust width as needed
        else:
            st.warning("Naukri Milaao logo not found. Please ensure the file 'naukri_milaao_logo.jpg' is in the directory.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- ROLE SELECTION PAGE ----------------------
def display_role_selection():
    if st.session_state.announcement:
        st.info(f"📢 Announcement: {st.session_state.announcement}")
    
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
    # Dynamically calculate metrics
    candidates_registered = len(st.session_state.students)
    companies_onboarded = len(st.session_state.companies)
    jobs_posted = len(st.session_state.jobs)
    colA.metric("👥 Candidates Registered", f"{candidates_registered:,}")
    colB.metric("🏢 Companies Onboarded", f"{companies_onboarded:,}")
    colC.metric("📝 Jobs Posted", f"{jobs_posted:,}")

# ---------------------- MAIN APPLICATION ----------------------
def main():
    initialize_session_state()
    display_header()
    
    if st.session_state.role is None:
        display_role_selection()
    else:
        # Show back button
        st.button("⬅️ Back to Home", on_click=go_back, type="secondary")
        
        # Route to appropriate module dashboard
        try:
            if st.session_state.role == "student":
                student.display_student_dashboard()
            elif st.session_state.role == "company":
                company.display_company_dashboard()
            elif st.session_state.role == "admin":
                admin.display_admin_dashboard()
        except Exception as e:
            st.error(f"Error in {st.session_state.role} module: {e}")
            st.error("Please check the module implementation or contact support.")
            st.button("Try Again", on_click=go_back)

if __name__ == "__main__":
    main()