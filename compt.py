
import streamlit as st
import pandas as pd
import numpy as np

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
        height: 120px; /* For consistent height */
        display: flex; /* For vertical alignment */
        flex-direction: column; /* For vertical alignment */
        justify-content: center; /* For vertical alignment */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="big-title">💼 Smart Job Portal</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Connecting Students & Companies through AI-powered matching</p>', unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION (CENTRALIZED) ---
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


def go_back():
    """Resets all relevant session state variables to return to the main page."""
    st.session_state.role = None
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.details_submitted = False
    st.rerun()

# ---------------------- ROLE SELECTION ----------------------
if st.session_state.role is None:
    if st.session_state.announcement:
        st.info(f"📢 Announcement: {st.session_state.announcement}")

    st.subheader("Choose Your Role to Continue")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="highlight-box">🎓 <br> I am a Student</div>', unsafe_allow_html=True)
        if st.button("Login as Student"):
            st.session_state.role = "student"
            st.rerun()
    with col2:
        st.markdown('<div class="highlight-box">🏢 <br> I am a Company</div>', unsafe_allow_html=True)
        if st.button("Login as Company"):
            st.session_state.role = "company"
            st.rerun()
    with col3:
        st.markdown('<div class="highlight-box">👤 <br> I am an Admin</div>', unsafe_allow_html=True)
        if st.button("Login as Admin"):
            st.session_state.role = "admin"
            st.rerun()

    st.markdown("---")
    colA, colB, colC = st.columns(3)
    with colA:
        st.metric("Students Registered", "2,340")
    with colB:
        st.metric("Companies Onboarded", "120")
    with colC:
        st.metric("Jobs Posted", "450+")

# ---------------------- LOGGED IN VIEWS ----------------------
else:
    st.button("⬅️ Back to Home", on_click=go_back)

    # --- MOCK DATA & MATCHING LOGIC (Centralized for reuse) ---
    @st.cache_data
    def get_matching_data():
        students = pd.DataFrame({
            'StudentID': ['STU1001', 'STU1002', 'STU1003', 'STU1004', 'STU1005'],
            'Name': ['Liam Smith', 'Olivia Johnson', 'Noah Williams', 'Emma Brown', 'Oliver Jones'],
            'Degree': ['Computer Science', 'Data Science', 'Computer Science', 'Mechanical Engg.', 'Data Science'],
            'Resume Score': [88, 92, 85, 78, 95],
            'Test Score': [90, 95, 82, 75, 98],
            'Skills': [
                ['Python', 'Java', 'SQL', 'Git'],
                ['Python', 'R', 'TensorFlow', 'SQL', 'Tableau'],
                ['Python', 'JavaScript', 'React', 'Node.js'],
                ['AutoCAD', 'SolidWorks', 'MATLAB'],
                ['Python', 'PyTorch', 'Scikit-learn', 'AWS']
            ]
        })
        jobs = pd.DataFrame({
            'JobID': ['JOB501', 'JOB502', 'JOB503', 'JOB504'],
            'Company': ['Innovatech', 'DataSolutions', 'FutureSoft', 'Innovatech'],
            'Role': ['Software Engineer', 'Data Scientist', 'Frontend Developer', 'AI/ML Engineer'],
            'Min Resume Score': [80, 85, 80, 90],
            'Min Test Score': [85, 90, 75, 90],
            'Required Skills': [
                ['Python', 'Java', 'SQL', 'Algorithms'],
                ['Python', 'TensorFlow', 'SQL', 'Statistics'],
                ['JavaScript', 'React', 'HTML', 'CSS'],
                ['Python', 'PyTorch', 'AWS', 'NLP']
            ]
        })
        return students, jobs

    students_df, jobs_df = get_matching_data()

    def calculate_match(student_skills, required_skills, student_resume, min_resume, student_test, min_test):
        if student_resume < min_resume or student_test < min_test:
            return 0
        common_skills = set(student_skills) & set(required_skills)
        skill_match_score = len(common_skills) / len(required_skills) if len(required_skills) > 0 else 0
        resume_score_ratio = (student_resume - min_resume) / (100 - min_resume) if (100 - min_resume) > 0 else 0
        test_score_ratio = (student_test - min_test) / (100 - min_test) if (100 - min_test) > 0 else 0
        final_score = (0.6 * skill_match_score) + (0.2 * resume_score_ratio) + (0.2 * test_score_ratio)
        return round(final_score * 100, 2)

    # ---------------------- STUDENT WORKFLOW ----------------------
    if st.session_state.role == "student":
        st.header("🎓 Student Portal")
        if not st.session_state.logged_in:
            with st.form("student_login_form"):
                student_id = st.text_input("Enter Student ID (e.g., STU1001)")
                student_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if student_id in students_df['StudentID'].values and student_password == "stu@1234":
                        st.session_state.logged_in = True
                        st.session_state.user_id = student_id
                        st.rerun()
                    else:
                        st.error("❌ Invalid Student ID or Password")
        elif not st.session_state.details_submitted:
            st.success(f"✅ Welcome {st.session_state.user_id}! Please complete your profile.")
            with st.form("student_details_form"):
                student_name = st.text_input("Full Name")
                student_email = st.text_input("Email")
                if st.form_submit_button("Continue ➡️"):
                    if student_name and student_email:
                        st.session_state.details_submitted = True
                        st.rerun()
                    else:
                        st.error("⚠️ Please complete all required fields.")
        else:
            st.success("🎉 Your profile is active! Here are your recommended jobs.")
            student_data = students_df[students_df['StudentID'] == st.session_state.user_id].iloc[0]
            st.subheader(f"Recommended Jobs for {student_data['Name']}")
            
            matches = []
            for index, job in jobs_df.iterrows():
                match_score = calculate_match(
                    student_data['Skills'], job['Required Skills'],
                    student_data['Resume Score'], job['Min Resume Score'],
                    student_data['Test Score'], job['Min Test Score']
                )
                if match_score > 0:
                    job_info = job.to_dict()
                    job_info['Match Score'] = match_score
                    matches.append(job_info)
            
            sorted_matches = sorted(matches, key=lambda x: x['Match Score'], reverse=True)

            if not sorted_matches:
                st.warning("No suitable job matches found at the moment. Please check back later!")
            else:
                for match in sorted_matches:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader(f"{match['Role']} at {match['Company']}")
                            st.caption(f"Required Skills: {', '.join(match['Required Skills'])}")
                        with col2:
                            st.metric("Your Match", f"{match['Match Score']}%")
                            if st.button("Apply Now", key=match['JobID']):
                                st.toast(f"✅ Successfully applied for {match['Role']}!")

    # ---------------------- COMPANY WORKFLOW (REVISED) ----------------------
    elif st.session_state.role == "company":
        st.header("🏢 Company Portal")
        # Step 1: Login Form (remains the same)
        if not st.session_state.logged_in:
            with st.form("company_login_form"):
                company_id = st.text_input("Enter Company ID (e.g., COMP001)")
                company_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if company_id == "COMP001" and company_password == "comp@123":
                        st.session_state.logged_in = True
                        st.session_state.user_id = company_id
                        st.rerun()
                    else:
                        st.error("❌ Invalid Company ID or Password")

        # Step 2: Display Job Dashboard (This part is new)
        else:
            # 1. Get the company name from the logged-in user ID for our demo
            company_name_map = {"COMP001": "Innovatech"}
            company_name = company_name_map.get(st.session_state.user_id, "Unknown Company")
            
            st.success(f"✅ Welcome {company_name}! Here is a summary of your active job postings.")

            # 2. Filter the main jobs DataFrame to get only the jobs for this company
            company_jobs = jobs_df[jobs_df['Company'] == company_name]

            if company_jobs.empty:
                st.warning("You have not posted any jobs yet.")
            else:
                # 3. Loop through each of the company's job postings
                for index, job_data in company_jobs.iterrows():
                    role = job_data['Role']
                    job_id = job_data['JobID']
                    
                    # Find all matching students for this specific job
                    matches = []
                    for s_index, student in students_df.iterrows():
                        match_score = calculate_match(
                            student['Skills'], job_data['Required Skills'],
                            student['Resume Score'], job_data['Min Resume Score'],
                            student['Test Score'], job_data['Min Test Score']
                        )
                        if match_score > 0:
                            student_info = student.to_dict()
                            student_info['Match Score'] = match_score
                            matches.append(student_info)
                    
                    sorted_matches = sorted(matches, key=lambda x: x['Match Score'], reverse=True)
                    
                    # 4. Display each job as an expander with the candidates inside
                    with st.expander(f"**{role}** ({job_id}) - `{len(sorted_matches)}` matching candidates found"):
                        if not sorted_matches:
                            st.info("No suitable student matches found for this role at the moment.")
                        else:
                            for match in sorted_matches:
                                st.markdown("---")
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.subheader(f"{match['Name']}")
                                    st.write(f"**Degree:** {match['Degree']}")
                                    st.caption(f"Skills: {', '.join(match['Skills'])}")
                                with col2:
                                    st.metric("Match Score", f"{match['Match Score']}%")
                                    if st.button("Shortlist", key=f"shortlist_{job_id}_{match['StudentID']}"):
                                        st.toast(f"✅ {match['Name']} shortlisted for {role}!")

    # ---------------------- ADMIN WORKFLOW (ENHANCED) ----------------------
    elif st.session_state.role == "admin":
        st.header("👤 Admin Panel")
        if not st.session_state.logged_in:
            with st.form("admin_login_form"):
                admin_id = st.text_input("Admin ID (e.g., ADMIN001)")
                admin_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if admin_id == "ADMIN001" and admin_password == "admin@123":
                        st.session_state.logged_in = True
                        st.session_state.user_id = admin_id
                        st.rerun()
                    else:
                        st.error("❌ Invalid Admin ID or Password")
        else:
            st.sidebar.title(f"Welcome, {st.session_state.user_id}!")
            admin_option = st.sidebar.radio(
                "Admin Menu",
                ["Dashboard", "Manage Students", "Manage Companies", "View Job Postings", "Portal Settings"]
            )
            
            # --- MOCK DATA FOR ADMIN PANEL ---
            @st.cache_data
            def get_admin_mock_data():
                admin_students = pd.DataFrame({
                    'StudentID': [f'STU{1000+i}' for i in range(1, 21)],
                    'Name': ['Liam Smith', 'Olivia Johnson', 'Noah Williams', 'Emma Brown', 'Oliver Jones', 'Ava Garcia', 'Elijah Miller', 'Sophia Davis', 'William Rodriguez', 'Isabella Martinez', 'James Hernandez', 'Charlotte Lopez', 'Benjamin Gonzalez', 'Amelia Wilson', 'Lucas Anderson', 'Mia Taylor', 'Henry Thomas', 'Evelyn Moore', 'Alexander Jackson', 'Harper Martin'],
                    'College': np.random.choice(['Tech University', 'Global Institute', 'City College', 'State University'], 20),
                    'Degree': np.random.choice(['Computer Science', 'Data Science', 'Mechanical Engg.', 'Electronics Engg.'], 20),
                    'Verified': np.random.choice([True, False], 20, p=[0.8, 0.2])
                })
                admin_companies = pd.DataFrame({
                    'CompanyID': [f'COMP{100+i}' for i in range(1, 11)],
                    'Name': ['Innovatech', 'DataSolutions', 'QuantumLeap', 'Nexus Inc.', 'FutureSoft', 'CodeGenius', 'Alpha Systems', 'BluePeak', 'SynthoCorp', 'Visionary AI'],
                    'Industry': np.random.choice(['SaaS', 'FinTech', 'AI/ML', 'Hardware', 'Consulting'], 10),
                    'Approval_Status': np.random.choice(['Verified', 'Pending', 'Rejected'], 10, p=[0.7, 0.2, 0.1])
                })
                admin_jobs = pd.DataFrame({
                    'JobID': [f'JOB{500+i}' for i in range(1, 16)],
                    'Company': np.random.choice(admin_companies['Name'], 15),
                    'Role': np.random.choice(['Software Engineer', 'Data Analyst', 'Product Manager', 'UX Designer', 'DevOps Engineer'], 15),
                    'Status': np.random.choice(['Open', 'Closed'], 15, p=[0.75, 0.25]),
                    'Openings': np.random.randint(1, 10, 15)
                })
                return admin_students, admin_companies, admin_jobs
            
            admin_students_df, admin_companies_df, admin_jobs_df = get_admin_mock_data()

            st.success("✅ You are now logged into the admin dashboard.")
            
            if admin_option == "Dashboard":
                st.subheader("📊 Dashboard Analytics")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Students", len(admin_students_df))
                col2.metric("Verified Companies", admin_companies_df[admin_companies_df['Approval_Status'] == 'Verified'].shape[0])
                col3.metric("Open Jobs", admin_jobs_df[admin_jobs_df['Status'] == 'Open'].shape[0])
                col4.metric("Pending Approvals", admin_companies_df[admin_companies_df['Approval_Status'] == 'Pending'].shape[0])
                st.bar_chart(admin_jobs_df['Role'].value_counts())

            elif admin_option == "Manage Students":
                st.subheader("🎓 Manage Students")
                st.data_editor(admin_students_df, num_rows="dynamic")

            elif admin_option == "Manage Companies":
                st.subheader("🏢 Manage Companies")
                st.data_editor(admin_companies_df, num_rows="dynamic")
            
            elif admin_option == "View Job Postings":
                st.subheader("📝 View All Job Postings")
                st.dataframe(admin_jobs_df)

            elif admin_option == "Portal Settings":
                st.subheader("⚙️ Portal Settings")
                new_announcement = st.text_area("Site-wide announcement", value=st.session_state.announcement)
                if st.button("Update Announcement"):
                    st.session_state.announcement = new_announcement
                    st.success("Announcement updated!")