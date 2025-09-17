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
    # Display announcement if it exists
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
    # This button is now universal for all roles
    st.button("⬅️ Back to Home", on_click=go_back)

    # ---------------------- STUDENT WORKFLOW ----------------------
    if st.session_state.role == "student":
        st.header("🎓 Student Portal")
        # Step 1: Login Form
        if not st.session_state.logged_in:
            with st.form("student_login_form"):
                student_id = st.text_input("Enter Student ID (e.g., STU1001)")
                student_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if student_id == "STU1001" and student_password == "stu@1234":
                        st.session_state.logged_in = True
                        st.session_state.user_id = student_id
                        st.rerun()
                    else:
                        st.error("❌ Invalid Student ID or Password")
        # Step 2: Details Form (after login)
        elif not st.session_state.details_submitted:
            st.success(f"✅ Welcome {st.session_state.user_id}! Please complete your profile.")
            with st.form("student_details_form"):
                student_name = st.text_input("Full Name")
                student_email = st.text_input("Email")
                student_phone = st.text_input("Phone Number")
                student_college = st.text_input("College Name")
                student_degree = st.text_input("Degree / Major")
                if st.form_submit_button("Continue ➡️"):
                    if student_name and student_email and student_phone:
                        st.session_state.details_submitted = True
                        st.rerun()
                    else:
                        st.error("⚠️ Please complete all required fields.")
        # Step 3: Final confirmation
        else:
            st.success("🎉 Your profile has been saved successfully.")
            st.info("Next Section: Resume analysis and job recommendations.")

    # ---------------------- COMPANY WORKFLOW ----------------------
    elif st.session_state.role == "company":
        st.header("🏢 Company Portal")
        # Step 1: Login Form
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
        # Step 2: Job Details Form (after login)
        elif not st.session_state.details_submitted:
            st.success(f"✅ Welcome {st.session_state.user_id}! Please add job details.")
            with st.form("job_details_form"):
                company_name = st.text_input("Company Name")
                num_openings = st.number_input("Number of Openings", min_value=1, step=1)
                job_role = st.text_input("Job Role / Position")
                job_description = st.text_area("Job Description")
                if st.form_submit_button("Submit Job Details"):
                    if company_name and job_role and job_description:
                        st.session_state.details_submitted = True
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill all job details.")
        # Step 3: Final confirmation
        else:
            st.success("🎯 Job has been posted successfully!")
            st.info("Students will be recommended based on their skills.")

    # ---------------------- ADMIN WORKFLOW (ENHANCED) ----------------------
    elif st.session_state.role == "admin":
        st.header("👤 Admin Panel")
        # Step 1: Admin Login Form
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
        # Step 2: Admin Dashboard (after login)
        else:
            st.sidebar.title(f"Welcome, {st.session_state.user_id}!")
            admin_option = st.sidebar.radio(
                "Admin Menu",
                ["Dashboard", "Manage Students", "Manage Companies", "View Job Postings", "Portal Settings"]
            )
            
            # --- MOCK DATA CREATION ---
            # In a real app, this data would come from a database.
            @st.cache_data
            def get_mock_data():
                students = pd.DataFrame({
                    'StudentID': [f'STU{1000+i}' for i in range(1, 21)],
                    'Name': ['Liam Smith', 'Olivia Johnson', 'Noah Williams', 'Emma Brown', 'Oliver Jones', 'Ava Garcia', 'Elijah Miller', 'Sophia Davis', 'William Rodriguez', 'Isabella Martinez', 'James Hernandez', 'Charlotte Lopez', 'Benjamin Gonzalez', 'Amelia Wilson', 'Lucas Anderson', 'Mia Taylor', 'Henry Thomas', 'Evelyn Moore', 'Alexander Jackson', 'Harper Martin'],
                    'College': np.random.choice(['Tech University', 'Global Institute', 'City College', 'State University'], 20),
                    'Degree': np.random.choice(['Computer Science', 'Data Science', 'Mechanical Engg.', 'Electronics Engg.'], 20),
                    'Verified': np.random.choice([True, False], 20, p=[0.8, 0.2])
                })
                companies = pd.DataFrame({
                    'CompanyID': [f'COMP{100+i}' for i in range(1, 11)],
                    'Name': ['Innovatech', 'DataSolutions', 'QuantumLeap', 'Nexus Inc.', 'FutureSoft', 'CodeGenius', 'Alpha Systems', 'BluePeak', 'SynthoCorp', 'Visionary AI'],
                    'Industry': np.random.choice(['SaaS', 'FinTech', 'AI/ML', 'Hardware', 'Consulting'], 10),
                    'Approval_Status': np.random.choice(['Verified', 'Pending', 'Rejected'], 10, p=[0.7, 0.2, 0.1])
                })
                jobs = pd.DataFrame({
                    'JobID': [f'JOB{500+i}' for i in range(1, 16)],
                    'Company': np.random.choice(companies['Name'], 15),
                    'Role': np.random.choice(['Software Engineer', 'Data Analyst', 'Product Manager', 'UX Designer', 'DevOps Engineer'], 15),
                    'Status': np.random.choice(['Open', 'Closed'], 15, p=[0.75, 0.25]),
                    'Openings': np.random.randint(1, 10, 15)
                })
                return students, companies, jobs
            
            students_df, companies_df, jobs_df = get_mock_data()

            # --- DISPLAY SELECTED OPTION ---
            st.success("✅ You are now logged into the admin dashboard.")
            
            if admin_option == "Dashboard":
                st.subheader("📊 Dashboard Analytics")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Students", len(students_df))
                col2.metric("Verified Companies", companies_df[companies_df['Approval_Status'] == 'Verified'].shape[0])
                col3.metric("Open Jobs", jobs_df[jobs_df['Status'] == 'Open'].shape[0])
                col4.metric("Pending Approvals", companies_df[companies_df['Approval_Status'] == 'Pending'].shape[0])

                st.markdown("---")
                
                c1, c2 = st.columns((6, 4))
                with c1:
                    st.subheader("Jobs by Role")
                    job_counts = jobs_df['Role'].value_counts()
                    st.bar_chart(job_counts)
                with c2:
                    st.subheader("Company Status")
                    status_counts = companies_df['Approval_Status'].value_counts()
                    st.dataframe(status_counts)

            elif admin_option == "Manage Students":
                st.subheader("🎓 Manage Students")
                st.write("Review, search, and manage student profiles. You can edit their verification status directly.")
                
                # Search and Filter
                search_query = st.text_input("Search by Name or Student ID", key="student_search")
                filtered_df = students_df[students_df['Name'].str.contains(search_query, case=False) | students_df['StudentID'].str.contains(search_query, case=False)]

                # Display editable dataframe
                st.info("Click on a cell to edit. Check/uncheck the 'Verified' box and your changes will be saved.")
                edited_students = st.data_editor(filtered_df, num_rows="dynamic")
                
                # In a real app, you would have a button here to save changes to the database.
                # For this demo, the changes are just kept in the session.

            elif admin_option == "Manage Companies":
                st.subheader("🏢 Manage Companies")
                st.write("Approve, reject, or review company profiles. Use the filters to narrow down the list.")

                # Filter by status
                status_filter = st.selectbox("Filter by Approval Status", ['All'] + list(companies_df['Approval_Status'].unique()))

                if status_filter == 'All':
                    filtered_df = companies_df
                else:
                    filtered_df = companies_df[companies_df['Approval_Status'] == status_filter]

                st.info("You can directly edit the 'Approval_Status' field. Changes are reflected instantly for this demo.")
                edited_companies = st.data_editor(
                    filtered_df,
                    column_config={
                        "Approval_Status": st.column_config.SelectboxColumn(
                            "Approval Status",
                            options=['Verified', 'Pending', 'Rejected'],
                            required=True,
                        )
                    },
                    hide_index=True,
                    num_rows="dynamic"
                )
            
            elif admin_option == "View Job Postings":
                st.subheader("📝 View All Job Postings")
                st.write("Oversee all job postings from various companies.")

                # Filters
                col_filter1, col_filter2 = st.columns(2)
                with col_filter1:
                    company_filter = st.selectbox("Filter by Company", ['All'] + list(jobs_df['Company'].unique()))
                with col_filter2:
                    status_filter = st.selectbox("Filter by Status", ['All', 'Open', 'Closed'])
                
                # Apply filters
                filtered_jobs = jobs_df.copy()
                if company_filter != 'All':
                    filtered_jobs = filtered_jobs[filtered_jobs['Company'] == company_filter]
                if status_filter != 'All':
                    filtered_jobs = filtered_jobs[filtered_jobs['Status'] == status_filter]
                
                st.dataframe(filtered_jobs, use_container_width=True)


            elif admin_option == "Portal Settings":
                st.subheader("⚙️ Portal Settings")
                st.write("Manage global settings for the portal.")

                st.markdown("#### Announcement Banner")
                new_announcement = st.text_area(
                    "Enter a site-wide announcement", 
                    value=st.session_state.announcement,
                    help="This message will be displayed at the top of the home page for all users."
                )
                if st.button("Update Announcement"):
                    st.session_state.announcement = new_announcement
                    st.success("Announcement updated successfully!")

                st.markdown("---")
                st.markdown("#### User Management")
                st.write("Add or remove admin users, or change user permissions.")
                st.warning("🔒 Feature not implemented in this demo.")