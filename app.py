
import streamlit as st

# ---------------------- MAIN APP ----------------------
st.set_page_config(page_title="Smart Job Portal", page_icon="💼", layout="wide")

# ---------------------- HEADER ----------------------
st.markdown(
    """
    <style>
    .big-title {
        font-size:42px !important;
        color:#2E86C1;
        text-align:center;
        font-weight:bold;
    }
    .subtitle {
        font-size:20px !important;
        text-align:center;
        color:#5D6D7E;
    }
    .highlight-box {
        padding:15px;
        border-radius:10px;
        background-color:#EAF2F8;
        text-align:center;
        margin:10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="big-title">💼 Smart Job Portal</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Connecting Students & Companies through AI-powered matching</p>', unsafe_allow_html=True)

if "role" not in st.session_state:
    st.session_state.role = None

# ---------------------- ROLE SELECTION ----------------------
if st.session_state.role is None:
    st.subheader("Choose Your Role to Continue")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="highlight-box">🎓 <br> I am a Student</div>', unsafe_allow_html=True)
        if st.button("Login as Student"):
            st.session_state.role = "student"

    with col2:
        st.markdown('<div class="highlight-box">🏢 <br> I am a Company</div>', unsafe_allow_html=True)
        if st.button("Login as Company"):
            st.session_state.role = "company"

    st.markdown("---")
    colA, colB, colC = st.columns(3)
    with colA:
        st.metric("Students Registered", "2,340")
    with colB:
        st.metric("Companies Onboarded", "120")
    with colC:
        st.metric("Jobs Posted", "450+")

# ---------------------- STUDENT LOGIN ----------------------
elif st.session_state.role == "student":
    st.header("🎓 Student Login")
    with st.form("student_form"):
        student_id = st.text_input("Enter Student ID (University Roll No.)")
        student_password = st.text_input("Password", type="password")
        submit_student = st.form_submit_button("Login")

    if submit_student:
        if student_id == "STU1001" and student_password == "stu@1234":
            st.success(f"✅ Welcome Student {student_id}! Please continue to upload your details.")
            
            with st.form("student_details"):
                student_name = st.text_input("Full Name")
                student_email = st.text_input("Email")
                student_phone = st.text_input("Phone Number")
                student_college = st.text_input("College Name")
                student_degree = st.text_input("Degree / Major")
                resume_file = st.file_uploader("Upload Resume (PDF/Doc)", type=["pdf", "docx"])
                
                save_details = st.form_submit_button("Submit Details")
            
            if save_details:
                if student_name and resume_file:
                    st.success("🎉 Your profile has been saved! Resume uploaded successfully.")
                    st.info("Next: Your resume will be analyzed for skills.")
                else:
                    st.error("⚠️ Please complete all fields and upload your resume.")
        else:
            st.error("❌ Invalid Student ID or Password")

    if st.button("⬅️ Back"):
        st.session_state.role = None

# ---------------------- COMPANY LOGIN ----------------------
elif st.session_state.role == "company":
    st.header("🏢 Company Login")
    with st.form("company_form"):
        company_id = st.text_input("Enter Company ID")
        company_password = st.text_input("Password", type="password")
        submit_company = st.form_submit_button("Login")

    if submit_company:
        if company_id == "COMP001" and company_password == "comp@123":
            st.success(f"✅ Welcome Company {company_id}! Please add job details.")

            with st.form("job_details"):
                company_name = st.text_input("Company Name")
                num_openings = st.number_input("Number of Openings", min_value=1, step=1)
                job_role = st.text_input("Job Role / Position")
                job_description = st.text_area("Job Description")
                
                save_job = st.form_submit_button("Submit Job Details")
            
            if save_job:
                if company_name and job_role and job_description:
                    st.success(f"🎯 Job '{job_role}' added successfully!")
                    st.info("Students will be recommended based on their skills.")
                else:
                    st.error("⚠️ Please fill all job details.")
        else:
            st.error("❌ Invalid Company ID or Password")

    if st.button("⬅️ Back"):
        st.session_state.role = None
