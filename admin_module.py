import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

def display_admin_dashboard():
    """Main admin dashboard function"""
    # CSS for consistent styling
    st.markdown(
        """
        <style>
        .stApp {
            color: #2C3E50 !important;
        }
        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: #2C3E50 !important;
        }
        [data-testid="metric-container"] * {
            color: #2C3E50 !important;
        }
        .stButton > button {
            color: white !important;
            background-color: #FF6B35 !important;
        }
        .stSelectbox > div > div > div {
            color: #2C3E50 !important;
        }
        .stTextInput > div > div > input {
            color: #2C3E50 !important;
        }
        .stTextArea > div > div > textarea {
            color: #2C3E50 !important;
        }
        .streamlit-expanderHeader {
            color: #2C3E50 !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #2C3E50 !important;
        }
        .css-1d391kg {
            color: #2C3E50 !important;
        }
        .stDataFrame {
            color: #2C3E50 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.header("👤 Admin Panel")
    
    # Initialize shared session state with empty DataFrames (no dummy data)
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
    if 'shortlists' not in st.session_state:
        st.session_state.shortlists = pd.DataFrame(columns=['JobID', 'StudentID', 'ShortlistDate', 'Status'])
    if 'admin_credentials' not in st.session_state:
        st.session_state.admin_credentials = {'ADMIN001': 'admin@123'}

    # Ensure correct data types for jobs DataFrame
    jobs_df = st.session_state.jobs.copy()
    students_df = st.session_state.students.copy()
    companies_df = st.session_state.companies
    applications_df = st.session_state.applications
    shortlists_df = st.session_state.shortlists

    # Convert numeric columns in jobs_df
    numeric_columns_jobs = ['Openings', 'Applications', 'Min Resume Score', 'Min Test Score']
    for col in numeric_columns_jobs:
        if col in jobs_df.columns:
            jobs_df[col] = pd.to_numeric(jobs_df[col], errors='coerce').fillna(0).astype(int)

    # Convert string columns in jobs_df
    string_columns_jobs = ['JobID', 'Company', 'Role', 'Location', 'Salary', 'Experience', 'Description', 'Status']
    for col in string_columns_jobs:
        if col in jobs_df.columns:
            jobs_df[col] = jobs_df[col].astype(str)

    # Ensure list and datetime columns in jobs_df
    if 'Required Skills' in jobs_df.columns:
        jobs_df['Required Skills'] = jobs_df['Required Skills'].apply(lambda x: x if isinstance(x, list) else [])
    if 'Posted_Date' in jobs_df.columns:
        jobs_df['Posted_Date'] = pd.to_datetime(jobs_df['Posted_Date'], errors='coerce').fillna(pd.to_datetime(datetime.now()))

    # Convert numeric columns in students_df
    numeric_columns_students = ['CGPA', 'Resume Score', 'Test Score', 'Skills_Count', 'Applications_Count']
    for col in numeric_columns_students:
        if col in students_df.columns:
            if col == 'CGPA':
                students_df[col] = pd.to_numeric(students_df[col], errors='coerce').fillna(0.0).astype(float)
            else:
                students_df[col] = pd.to_numeric(students_df[col], errors='coerce').fillna(0).astype(int)

    # Convert string columns in students_df
    string_columns_students = ['StudentID', 'Name', 'Email', 'College', 'Degree', 'Year', 'Status']
    for col in string_columns_students:
        if col in students_df.columns:
            students_df[col] = students_df[col].astype(str)

    # Ensure list and boolean columns in students_df
    if 'Skills' in students_df.columns:
        students_df['Skills'] = students_df['Skills'].apply(lambda x: x if isinstance(x, list) else [])
    if 'Test_Completed' in students_df.columns:
        students_df['Test_Completed'] = students_df['Test_Completed'].astype(bool)
    if 'Resume_Uploaded' in students_df.columns:
        students_df['Resume_Uploaded'] = students_df['Resume_Uploaded'].astype(bool)
    if 'Registration_Date' in students_df.columns:
        students_df['Registration_Date'] = pd.to_datetime(students_df['Registration_Date'], errors='coerce').fillna(pd.to_datetime(datetime.now()))

    # Update session state
    st.session_state.jobs = jobs_df
    st.session_state.students = students_df

    # Ensure all required columns exist
    required_student_cols = [
        'StudentID', 'Name', 'Email', 'College', 'Degree', 'Year', 'CGPA', 
        'Resume Score', 'Test Score', 'Skills', 'Skills_Count', 
        'Test_Completed', 'Resume_Uploaded', 'Status', 'Registration_Date', 
        'Applications_Count'
    ]
    for col in required_student_cols:
        if col not in students_df.columns:
            if col == 'Skills':
                students_df[col] = [[] for _ in range(len(students_df))]
            elif col == 'Email':
                students_df[col] = ''
            elif '_Count' in col or 'Score' in col:
                students_df[col] = 0 if col != 'CGPA' else 0.0
            elif 'Completed' in col or 'Uploaded' in col:
                students_df[col] = False
            elif col == 'Status':
                students_df[col] = 'Active'
            elif col == 'Registration_Date':
                students_df[col] = pd.to_datetime(datetime.now())
            else:
                students_df[col] = ''

    required_job_cols = [
        'JobID', 'Company', 'Role', 'Location', 'Salary', 'Experience', 
        'Description', 'Openings', 'Status', 'Posted_Date', 'Applications', 
        'Min Resume Score', 'Min Test Score', 'Required Skills'
    ]
    for col in required_job_cols:
        if col not in jobs_df.columns:
            jobs_df[col] = 0 if col in ['Applications', 'Openings', 'Min Resume Score', 'Min Test Score'] else 'Open' if col == 'Status' else pd.to_datetime(datetime.now()) if col == 'Posted_Date' else [] if col == 'Required Skills' else ''

    # Update derived metrics
    if not applications_df.empty:
        app_counts_jobs = applications_df.groupby('JobID').size()
        jobs_df['Applications'] = jobs_df['JobID'].map(app_counts_jobs).fillna(0).astype(int)
        app_counts_students = applications_df.groupby('StudentID').size()
        students_df['Applications_Count'] = students_df['StudentID'].map(app_counts_students).fillna(0).astype(int)
        company_apps = applications_df.merge(jobs_df[['JobID', 'Company']], on='JobID').groupby('Company').size()
        companies_df['Total_Applications'] = companies_df['Name'].map(company_apps).fillna(0).astype(int)

    st.session_state.jobs = jobs_df
    st.session_state.students = students_df
    st.session_state.companies = companies_df

    if not st.session_state.logged_in:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔑 Login")
            with st.form("admin_login_form"):
                admin_id = st.text_input("Admin ID (e.g., ADMIN001)")
                admin_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if admin_id in st.session_state.admin_credentials and admin_password == st.session_state.admin_credentials[admin_id]:
                        st.session_state.logged_in = True
                        st.session_state.user_id = admin_id
                        st.rerun()
                    else:
                        st.error("❌ Invalid Admin ID or Password")
        with col2:
            st.subheader("📝 Signup")
            with st.form("admin_signup_form"):
                new_admin_name = st.text_input("Admin Name")
                new_admin_email = st.text_input("Email")
                new_admin_password = st.text_input("Password", type="password")
                if st.form_submit_button("Signup"):
                    if new_admin_name and new_admin_email and new_admin_password:
                        new_id = f"ADMIN{len(st.session_state.admin_credentials) + 1:03d}"
                        st.session_state.admin_credentials[new_id] = new_admin_password
                        st.success(f"✅ Signup successful! Your Admin ID is {new_id}. Please login.")
                    else:
                        st.error("⚠️ Please complete all fields.")
    else:
        st.success(f"✅ Welcome Admin {st.session_state.user_id}!")
        
        st.sidebar.title(f"Admin Menu")
        admin_option = st.sidebar.radio(
            "Select Section",
            ["📊 Dashboard Overview", "🎓 Manage Students", "🏢 Manage Companies", "📝 Manage Jobs", "⚙️ Portal Settings", "📈 Analytics"]
        )
        
        if admin_option == "📊 Dashboard Overview":
            st.subheader("📊 Dashboard Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_students = len(students_df)
                active_students = len(students_df[students_df['Status'] == 'Active'])
                st.metric("Total Students", total_students, f"+{active_students} Active")
            with col2:
                total_companies = len(companies_df)
                verified_companies = len(companies_df[companies_df['Approval_Status'] == 'Verified'])
                st.metric("Total Companies", total_companies, f"{verified_companies} Verified")
            with col3:
                total_jobs = len(jobs_df)
                open_jobs = len(jobs_df[jobs_df['Status'] == 'Open'])
                st.metric("Total Jobs", total_jobs, f"{open_jobs} Open")
            with col4:
                total_applications = len(applications_df)
                avg_applications = round(total_applications / total_jobs if total_jobs > 0 else 0, 1)
                st.metric("Total Applications", total_applications, f"Avg: {avg_applications}")

            st.markdown("---")
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.subheader("Student Registration Trends")
                if not students_df.empty:
                    reg_trend = students_df.groupby(students_df['Registration_Date'].dt.date).size().reset_index()
                    reg_trend.columns = ['Date', 'Registrations']
                    fig = px.line(reg_trend, x='Date', y='Registrations', title="Daily Student Registrations")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No student registrations yet.")
            with col_chart2:
                st.subheader("Jobs by Industry")
                if not jobs_df.empty and not companies_df.empty:
                    jobs_industry = jobs_df.merge(companies_df[['Name', 'Industry']], left_on='Company', right_on='Name', how='left')
                    industry_counts = jobs_industry['Industry'].value_counts()
                    fig = px.pie(values=industry_counts.values, names=industry_counts.index, title="Job Distribution by Industry")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No jobs or companies yet.")

            st.subheader("Recent Activity")
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                st.write("**Recent Student Registrations**")
                if not students_df.empty:
                    recent_students = students_df.sort_values('Registration_Date', ascending=False).head(5)[['Name', 'College', 'Registration_Date']]
                    st.dataframe(recent_students, use_container_width=True)
                else:
                    st.info("No students registered.")
            with col_act2:
                st.write("**Recent Job Postings**")
                if not jobs_df.empty:
                    recent_jobs = jobs_df.sort_values('Posted_Date', ascending=False).head(5)[['Role', 'Company', 'Posted_Date']]
                    st.dataframe(recent_jobs, use_container_width=True)
                else:
                    st.info("No jobs posted.")

        elif admin_option == "🎓 Manage Students":
            st.subheader("🎓 Student Management")
            
            # Debug: Display students DataFrame and data types
            with st.expander("Debug: Students DataFrame"):
                st.write("Students DataFrame:")
                st.write(students_df)
                st.write("Data Types:")
                st.write(students_df.dtypes)
            
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            with col_filter1:
                colleges = [str(x) for x in students_df['College'].unique() if pd.notna(x)]
                college_filter = st.selectbox("Filter by College", ["All"] + sorted(colleges))
            with col_filter2:
                degrees = [str(x) for x in students_df['Degree'].unique() if pd.notna(x)]
                degree_filter = st.selectbox("Filter by Degree", ["All"] + sorted(degrees))
            with col_filter3:
                statuses = [str(x) for x in students_df['Status'].unique() if pd.notna(x)]
                status_filter = st.selectbox("Filter by Status", ["All"] + sorted(statuses))
            
            filtered_students = students_df.copy()
            try:
                if college_filter != "All":
                    filtered_students = filtered_students[filtered_students['College'] == college_filter]
                if degree_filter != "All":
                    filtered_students = filtered_students[filtered_students['Degree'] == degree_filter]
                if status_filter != "All":
                    filtered_students = filtered_students[filtered_students['Status'] == status_filter]
            except Exception as e:
                st.error(f"Error applying filters: {e}. Please check data types.")
                filtered_students = students_df.copy()
            
            st.write(f"Showing {len(filtered_students)} students")
            
            edited_students = st.data_editor(
                filtered_students,
                column_config={
                    "Status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["Active", "Inactive", "Pending"]
                    ),
                    "CGPA": st.column_config.NumberColumn("CGPA", min_value=0.0, max_value=10.0, format="%.2f"),
                    "Registration_Date": st.column_config.DateColumn("Registration Date"),
                    "Resume Score": st.column_config.NumberColumn("Resume Score", min_value=0, max_value=100),
                    "Test Score": st.column_config.NumberColumn("Test Score", min_value=0, max_value=100),
                    "Skills_Count": st.column_config.NumberColumn("Skills Count", min_value=0),
                    "Test_Completed": st.column_config.CheckboxColumn("Test Completed"),
                    "Resume_Uploaded": st.column_config.CheckboxColumn("Resume Uploaded"),
                    "Applications_Count": st.column_config.NumberColumn("Applications Count", min_value=0)
                },
                num_rows="dynamic",
                use_container_width=True
            )
            
            if st.button("Save Changes"):
                for col in ['Resume Score', 'Test Score', 'Skills_Count', 'Applications_Count']:
                    edited_students[col] = pd.to_numeric(edited_students[col], errors='coerce').fillna(0).astype(int)
                edited_students['CGPA'] = pd.to_numeric(edited_students['CGPA'], errors='coerce').fillna(0.0).astype(float)
                st.session_state.students.update(edited_students)
                st.session_state.students['Skills_Count'] = st.session_state.students['Skills'].apply(len)
                st.success("Changes saved!")

            st.subheader("Bulk Actions")
            col_bulk1, col_bulk2, col_bulk3 = st.columns(3)
            with col_bulk1:
                if st.button("Export Student Data"):
                    csv = filtered_students.to_csv(index=False)
                    st.download_button("Download CSV", csv, "students.csv", "text/csv")
            with col_bulk2:
                if st.button("Send Notification"):
                    st.info("Notification feature would send messages to selected students")
            with col_bulk3:
                if st.button("Generate Report"):
                    st.info("Report generation feature would create detailed student analytics")

        elif admin_option == "🏢 Manage Companies":
            st.subheader("🏢 Company Management")
            pending_companies = companies_df[companies_df['Approval_Status'] == 'Pending']
            if not pending_companies.empty:
                st.warning(f"⚠️ {len(pending_companies)} companies pending approval")
                for idx, company in pending_companies.iterrows():
                    with st.expander(f"Review: {company['Name']} ({company['CompanyID']})"):
                        col_info, col_action = st.columns([3, 1])
                        with col_info:
                            st.write(f"**Industry:** {company['Industry']}")
                            st.write(f"**Size:** {company['Company_Size']}")
                            st.write(f"**Jobs Posted:** {company['Jobs_Posted']}")
                            st.write(f"**Registration Date:** {company['Registration_Date'].strftime('%Y-%m-%d')}")
                        with col_action:
                            col_approve, col_reject = st.columns(2)
                            with col_approve:
                                if st.button("Approve", key=f"approve_{company['CompanyID']}"):
                                    index = companies_df[companies_df['CompanyID'] == company['CompanyID']].index[0]
                                    st.session_state.companies.loc[index, 'Approval_Status'] = 'Verified'
                                    st.success(f"✅ {company['Name']} approved!")
                                    st.rerun()
                            with col_reject:
                                if st.button("Reject", key=f"reject_{company['CompanyID']}"):
                                    index = companies_df[companies_df['CompanyID'] == company['CompanyID']].index[0]
                                    st.session_state.companies.loc[index, 'Approval_Status'] = 'Rejected'
                                    st.error(f"❌ {company['Name']} rejected!")
                                    st.rerun()
            
            st.markdown("---")
            st.subheader("All Companies")
            col_comp_filter1, col_comp_filter2 = st.columns(2)
            with col_comp_filter1:
                industries = [str(x) for x in companies_df['Industry'].unique() if pd.notna(x)]
                industry_filter = st.selectbox("Filter by Industry", ["All"] + sorted(industries))
            with col_comp_filter2:
                statuses = [str(x) for x in companies_df['Approval_Status'].unique() if pd.notna(x)]
                approval_filter = st.selectbox("Filter by Status", ["All"] + sorted(statuses))
            
            filtered_companies = companies_df.copy()
            if industry_filter != "All":
                filtered_companies = filtered_companies[filtered_companies['Industry'] == industry_filter]
            if approval_filter != "All":
                filtered_companies = filtered_companies[filtered_companies['Approval_Status'] == approval_filter]
            
            edited_companies = st.data_editor(
                filtered_companies,
                column_config={
                    "Approval_Status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["Verified", "Pending", "Rejected"]
                    ),
                    "Jobs_Posted": st.column_config.NumberColumn("Jobs Posted", min_value=0),
                    "Total_Applications": st.column_config.NumberColumn("Total Applications", min_value=0),
                    "Registration_Date": st.column_config.DateColumn("Registration Date")
                },
                use_container_width=True
            )
            
            if st.button("Save Company Changes"):
                for col in ['Jobs_Posted', 'Total_Applications']:
                    edited_companies[col] = pd.to_numeric(edited_companies[col], errors='coerce').fillna(0).astype(int)
                st.session_state.companies.update(edited_companies)
                st.success("Changes saved!")

        elif admin_option == "📝 Manage Jobs":
            st.subheader("📝 Job Management")
            
            # Debug: Display jobs DataFrame and data types
            with st.expander("Debug: Jobs DataFrame"):
                st.write("Jobs DataFrame:")
                st.write(jobs_df)
                st.write("Data Types:")
                st.write(jobs_df.dtypes)
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Total Jobs", len(jobs_df))
            with col_stat2:
                st.metric("Open Positions", len(jobs_df[jobs_df['Status'] == 'Open']))
            with col_stat3:
                st.metric("Total Openings", int(jobs_df['Openings'].sum()))
            
            col_job_filter1, col_job_filter2, col_job_filter3 = st.columns(3)
            with col_job_filter1:
                roles = [str(x) for x in jobs_df['Role'].unique() if pd.notna(x)]
                role_filter = st.selectbox("Filter by Role", ["All"] + sorted(roles))
            with col_job_filter2:
                locations = [str(x) for x in jobs_df['Location'].unique() if pd.notna(x)]
                location_filter = st.selectbox("Filter by Location", ["All"] + sorted(locations))
            with col_job_filter3:
                statuses = [str(x) for x in jobs_df['Status'].unique() if pd.notna(x)]
                status_job_filter = st.selectbox("Filter by Job Status", ["All"] + sorted(statuses))
            
            filtered_jobs = jobs_df.copy()
            try:
                if role_filter != "All":
                    filtered_jobs = filtered_jobs[filtered_jobs['Role'] == role_filter]
                if location_filter != "All":
                    filtered_jobs = filtered_jobs[filtered_jobs['Location'] == location_filter]
                if status_job_filter != "All":
                    filtered_jobs = filtered_jobs[filtered_jobs['Status'] == status_job_filter]
            except Exception as e:
                st.error(f"Error applying filters: {e}. Please ensure all job data is correctly formatted.")
                filtered_jobs = jobs_df.copy()
            
            st.write(f"Showing {len(filtered_jobs)} jobs")
            
            edited_jobs = st.data_editor(
                filtered_jobs,
                column_config={
                    "Status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["Open", "Closed", "On Hold"]
                    ),
                    "Applications": st.column_config.NumberColumn("Applications", min_value=0, format="%d"),
                    "Openings": st.column_config.NumberColumn("Openings", min_value=1, format="%d"),
                    "Min Resume Score": st.column_config.NumberColumn("Min Resume Score", min_value=0, max_value=100, format="%d"),
                    "Min Test Score": st.column_config.NumberColumn("Min Test Score", min_value=0, max_value=100, format="%d")
                },
                use_container_width=True
            )
            
            if st.button("Save Job Changes"):
                for col in numeric_columns_jobs:
                    edited_jobs[col] = pd.to_numeric(edited_jobs[col], errors='coerce').fillna(0).astype(int)
                st.session_state.jobs.update(edited_jobs)
                st.success("Changes saved!")
            
            # Shortlist Management
            st.markdown("---")
            st.subheader("Shortlist Management")
            if not filtered_jobs.empty and not applications_df.empty:
                for _, job in filtered_jobs.iterrows():
                    with st.expander(f"Shortlist Candidates for {job['Role']} at {job['Company']} (JobID: {job['JobID']})"):
                        job_applications = applications_df[applications_df['JobID'] == job['JobID']]
                        if not job_applications.empty:
                            applicants = job_applications.merge(students_df[['StudentID', 'Name', 'Email', 'Skills', 'Resume Score', 'Test Score']], on='StudentID')
                            selected_applicants = st.multiselect(
                                "Select Students to Shortlist",
                                options=applicants['StudentID'].tolist(),
                                format_func=lambda x: f"{applicants[applicants['StudentID'] == x]['Name'].iloc[0]} ({x})",
                                key=f"shortlist_{job['JobID']}"
                            )
                            if st.button("Shortlist Selected", key=f"shortlist_btn_{job['JobID']}"):
                                for student_id in selected_applicants:
                                    new_shortlist = {
                                        'JobID': job['JobID'],
                                        'StudentID': student_id,
                                        'ShortlistDate': pd.to_datetime(datetime.now()),
                                        'Status': 'Shortlisted'
                                    }
                                    if not ((st.session_state.shortlists['JobID'] == job['JobID']) & 
                                            (st.session_state.shortlists['StudentID'] == student_id)).any():
                                        st.session_state.shortlists = pd.concat([st.session_state.shortlists, pd.DataFrame([new_shortlist])], ignore_index=True)
                                st.success(f"✅ {len(selected_applicants)} students shortlisted for {job['Role']}!")
                            
                            if st.button("Share Shortlisted Details", key=f"share_{job['JobID']}"):
                                shortlisted = st.session_state.shortlists[
                                    (st.session_state.shortlists['JobID'] == job['JobID']) & 
                                    (st.session_state.shortlists['Status'] == 'Shortlisted')
                                ]
                                if not shortlisted.empty:
                                    shortlisted_details = shortlisted.merge(
                                        students_df[['StudentID', 'Name', 'Email', 'Skills', 'Resume Score', 'Test Score']],
                                        on='StudentID'
                                    )
                                    csv = shortlisted_details[['Name', 'Email', 'Skills', 'Resume Score', 'Test Score']].to_csv(index=False)
                                    st.download_button(
                                        label="Download Shortlisted Candidates",
                                        data=csv,
                                        file_name=f"shortlisted_{job['JobID']}.csv",
                                        mime="text/csv",
                                        key=f"download_{job['JobID']}"
                                    )
                                    st.info("Mock: Details sent to company via email.")
                                else:
                                    st.warning("No students shortlisted for this job.")
                        else:
                            st.info("No applications for this job.")
            else:
                st.info("No jobs or applications available.")

            st.subheader("Job Insights")
            col_insight1, col_insight2 = st.columns(2)
            with col_insight1:
                if not jobs_df.empty:
                    role_counts = jobs_df['Role'].value_counts().head(10)
                    fig = px.bar(x=role_counts.values, y=role_counts.index, orientation='h', 
                               title="Most Posted Job Roles", labels={'x': 'Number of Jobs', 'y': 'Role'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No jobs available.")
            with col_insight2:
                if not jobs_df.empty:
                    location_apps = jobs_df.groupby('Location')['Applications'].sum().sort_values(ascending=False)
                    fig = px.bar(x=location_apps.index, y=location_apps.values,
                               title="Applications by Location", labels={'x': 'Location', 'y': 'Applications'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No applications available.")

        elif admin_option == "⚙️ Portal Settings":
            st.subheader("⚙️ Portal Settings")
            st.subheader("System Announcements")
            current_announcement = st.session_state.get('announcement', 'Welcome! Job fair next week. All companies will be present.')
            new_announcement = st.text_area("Global Announcement", value=current_announcement)
            if st.button("Update Announcement"):
                st.session_state.announcement = new_announcement
                st.success("✅ Announcement updated successfully!")
            
            st.markdown("---")
            st.subheader("Portal Configuration")
            col_config1, col_config2 = st.columns(2)
            with col_config1:
                st.checkbox("Enable Student Registration", value=True)
                st.checkbox("Enable Company Registration", value=True)
                st.checkbox("Allow Resume Upload", value=True)
                st.checkbox("Enable Skill Testing", value=True)
            with col_config2:
                st.number_input("Max Resume Size (MB)", min_value=1, max_value=10, value=5)
                st.number_input("Max Applications per Student", min_value=1, max_value=50, value=20)
                st.selectbox("Default Theme", ["Light", "Dark", "Auto"])
                st.selectbox("Email Notifications", ["Enabled", "Disabled", "Weekly Summary"])
            
            st.markdown("---")
            st.subheader("Database Maintenance")
            col_maint1, col_maint2, col_maint3 = st.columns(3)
            with col_maint1:
                if st.button("Backup Database"):
                    st.info("Database backup initiated...")
            with col_maint2:
                if st.button("Clean Temp Files"):
                    st.info("Temporary files cleaned...")
            with col_maint3:
                if st.button("System Health Check"):
                    st.success("System is running normally ✅")

        elif admin_option == "📈 Analytics":
            st.subheader("📈 Advanced Analytics")
            time_period = st.selectbox("Select Time Period", ["Last 7 Days", "Last 30 Days", "Last 3 Months", "Last Year"])
            today = datetime.now()
            if time_period == "Last 7 Days":
                start_date = today - timedelta(days=7)
            elif time_period == "Last 30 Days":
                start_date = today - timedelta(days=30)
            elif time_period == "Last 3 Months":
                start_date = today - timedelta(days=90)
            elif time_period == "Last Year":
                start_date = today - timedelta(days=365)
            
            filtered_students = students_df[students_df['Registration_Date'] >= start_date]
            filtered_jobs = jobs_df[jobs_df['Posted_Date'] >= start_date]
            filtered_applications = applications_df[applications_df['ApplicationDate'] >= start_date]
            
            st.subheader("Key Performance Indicators")
            col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
            with col_kpi1:
                conversion_rate = round(len(filtered_applications) / len(filtered_students) * 100 if len(filtered_students) > 0 else 0, 1)
                st.metric("Application Conversion Rate", f"{conversion_rate}%")
            with col_kpi2:
                avg_time_to_hire = np.random.randint(10, 15)  # Mock
                st.metric("Avg. Time to Hire (days)", avg_time_to_hire)
            with col_kpi3:
                student_engagement = round(len(filtered_students[filtered_students['Applications_Count'] > 0]) / len(filtered_students) * 100 if len(filtered_students) > 0 else 0, 1)
                st.metric("Student Engagement Rate", f"{student_engagement}%")
            with col_kpi4:
                company_satisfaction = round(np.random.uniform(4.0, 4.5), 1)  # Mock
                st.metric("Company Satisfaction", f"{company_satisfaction}/5")
            
            st.markdown("---")
            st.subheader("User Activity Trends")
            if not filtered_students.empty or not filtered_jobs.empty:
                dates = pd.date_range(start=start_date.date(), end=today.date())
                student_activity = filtered_students.groupby(filtered_students['Registration_Date'].dt.date).size().reindex(dates, fill_value=0)
                company_activity = filtered_jobs.groupby(filtered_jobs['Posted_Date'].dt.date).size().reindex(dates, fill_value=0)
                activity_df = pd.DataFrame({
                    'Date': dates,
                    'Student Activity': student_activity,
                    'Company Activity': company_activity
                })
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=activity_df['Date'], y=activity_df['Student Activity'], name='Students', line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=activity_df['Date'], y=activity_df['Company Activity'], name='Companies', line=dict(color='red')))
                fig.update_layout(title='Daily User Activity', xaxis_title='Date', yaxis_title='Active Users')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No activity in the selected period.")
            
            col_skill1, col_skill2 = st.columns(2)
            with col_skill1:
                st.subheader("Most In-Demand Skills")
                all_required_skills = []
                for _, job in filtered_jobs.iterrows():
                    if isinstance(job['Required Skills'], list):
                        all_required_skills.extend(job['Required Skills'])
                if all_required_skills:
                    skill_counts = Counter(all_required_skills)
                    skills_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Demand']).sort_values('Demand', ascending=False).head(10)
                    fig = px.bar(skills_df, x='Skill', y='Demand', title='Skills Demand Analysis')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No skills data available.")
            
            with col_skill2:
                st.subheader("Skill Gap Analysis")
                if all_required_skills:
                    unique_skills = list(set(all_required_skills))
                    demand = [skill_counts.get(s, 0) for s in unique_skills]
                    student_skills = []
                    for skills in students_df['Skills']:
                        if isinstance(skills, list):
                            student_skills.extend(skills)
                    supply_counts = Counter(student_skills)
                    supply = [supply_counts.get(s, 0) for s in unique_skills]
                    gap_df = pd.DataFrame({
                        'Skill': unique_skills,
                        'Demand': demand,
                        'Supply': supply,
                        'Gap': [d - s for d, s in zip(demand, supply)]
                    })
                    gap_df['Abs Gap'] = gap_df['Gap'].abs()
                    # Debug: Display gap_df
                    with st.expander("Debug: Skill Gap Data"):
                        st.write(gap_df)
                    fig = px.scatter(gap_df, x='Supply', y='Demand', size='Abs Gap', hover_name='Skill',
                                   title='Skill Gap Analysis (Size = |Demand - Supply|)')
                    fig.update_layout(xaxis_title='Supply (from Students)', yaxis_title='Demand (from Jobs)')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No skills data available.")
            
            st.markdown("---")
            if st.button("Generate Analytics Report"):
                st.info("📊 Comprehensive analytics report would be generated and downloaded here")

if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    display_admin_dashboard()