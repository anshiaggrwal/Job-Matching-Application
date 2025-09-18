import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

# Job categories for skill selection (shared with student module)
JOB_CATEGORIES = {
    "Backend Developer": {
        "description": "Develops server-side applications, APIs, databases, and system architecture",
        "keywords": ["python", "java", "nodejs", "django", "flask", "spring", "api", "database", "mongodb", "postgresql", "mysql", "redis", "microservices", "docker", "rest", "graphql"],
        "skills_weight": 1.0
    },
    "Frontend Developer": {
        "description": "Creates user interfaces and client-side applications",
        "keywords": ["react", "angular", "vue", "javascript", "typescript", "html", "css", "sass", "webpack", "bootstrap", "tailwind", "jquery", "nextjs", "nuxtjs", "responsive"],
        "skills_weight": 1.0
    },
    "Full Stack Developer": {
        "description": "Works on both frontend and backend development",
        "keywords": ["react", "nodejs", "python", "javascript", "api", "database", "html", "css", "mongodb", "postgresql", "fullstack", "end-to-end"],
        "skills_weight": 1.2
    },
    "Data Scientist": {
        "description": "Analyzes data to extract insights and build predictive models",
        "keywords": ["python", "r", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "matplotlib", "seaborn", "jupyter", "machine learning", "statistics", "data analysis", "visualization"],
        "skills_weight": 1.0
    },
    "Machine Learning Engineer": {
        "description": "Builds and deploys machine learning models and systems",
        "keywords": ["python", "tensorflow", "pytorch", "scikit-learn", "mlops", "docker", "kubernetes", "aws", "machine learning", "deep learning", "neural networks", "model deployment"],
        "skills_weight": 1.0
    },
    "DevOps Engineer": {
        "description": "Manages infrastructure, deployment pipelines, and system operations",
        "keywords": ["docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible", "jenkins", "gitlab", "ci/cd", "linux", "bash", "monitoring", "infrastructure"],
        "skills_weight": 1.0
    },
    "Mobile Developer": {
        "description": "Develops applications for mobile platforms",
        "keywords": ["react native", "flutter", "swift", "kotlin", "android", "ios", "xamarin", "mobile", "app development"],
        "skills_weight": 1.0
    },
    "Data Engineer": {
        "description": "Builds data pipelines and manages data infrastructure",
        "keywords": ["python", "sql", "spark", "hadoop", "kafka", "airflow", "etl", "data pipeline", "big data", "aws", "snowflake", "databricks"],
        "skills_weight": 1.0
    },
    "UI/UX Designer": {
        "description": "Designs user interfaces and user experiences",
        "keywords": ["figma", "sketch", "adobe xd", "photoshop", "illustrator", "wireframing", "prototyping", "user research", "design thinking", "usability"],
        "skills_weight": 1.0
    },
    "QA Engineer": {
        "description": "Tests software applications and ensures quality",
        "keywords": ["selenium", "cypress", "jest", "junit", "testing", "automation", "manual testing", "api testing", "performance testing", "quality assurance"],
        "skills_weight": 1.0
    }
}

def calculate_match(student_skills, required_skills, student_resume, min_resume, student_test, min_test):
    """Calculate match score between student and job requirements"""
    if student_resume < min_resume or student_test < min_test:
        return 0
    common_skills = set(student_skills) & set(required_skills)
    skill_match_score = len(common_skills) / len(required_skills) if len(required_skills) > 0 else 0
    resume_score_ratio = (student_resume - min_resume) / (100 - min_resume) if (100 - min_resume) > 0 else 0
    test_score_ratio = (student_test - min_test) / (100 - min_test) if (100 - min_test) > 0 else 0
    final_score = (0.6 * skill_match_score) + (0.2 * resume_score_ratio) + (0.2 * test_score_ratio)
    return round(final_score * 100, 2)

def display_company_dashboard():
    """Main company dashboard function"""
    # Add this CSS block at the beginning of each module file's display function
    st.markdown(
        """
        <style>
        /* Fix text visibility issues */
        .stApp {
            color: #2C3E50 !important;
        }
        
        /* Ensure all text elements have proper contrast */
        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: #2C3E50 !important;
        }
        
        /* Fix metric text */
        [data-testid="metric-container"] * {
            color: #2C3E50 !important;
        }
        
        /* Fix button text */
        .stButton > button {
            color: white !important;
            background-color: #FF6B35 !important;
        }
        
        /* Fix form elements */
        .stSelectbox > div > div > div {
            color: #2C3E50 !important;
        }
        
        .stTextInput > div > div > input {
            color: #2C3E50 !important;
        }
        
        .stTextArea > div > div > textarea {
            color: #2C3E50 !important;
        }
        
        /* Fix expander text */
        .streamlit-expanderHeader {
            color: #2C3E50 !important;
        }
        
        /* Fix tab text */
        .stTabs [data-baseweb="tab"] {
            color: #2C3E50 !important;
        }
        
        /* Fix sidebar text */
        .css-1d391kg {
            color: #2C3E50 !important;
        }
        
        /* Fix dataframe text */
        .stDataFrame {
            color: #2C3E50 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.header("🏢 Company Portal")
    
    # Initialize session state
    if 'students' not in st.session_state:
        st.session_state.students = pd.DataFrame({
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
    if 'jobs' not in st.session_state:
        st.session_state.jobs = pd.DataFrame({
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
    if 'companies' not in st.session_state:
        st.session_state.companies = pd.DataFrame({
            'CompanyID': ['COMP001'],
            'Name': ['Innovatech']
        })
    if 'company_credentials' not in st.session_state:
        st.session_state.company_credentials = {'COMP001': 'comp@123'}
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'student_matches' not in st.session_state:
        st.session_state.student_matches = {}
    
    students_df = st.session_state.students
    jobs_df = st.session_state.jobs
    
    if not st.session_state.logged_in:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔑 Login")
            with st.form("company_login_form"):
                company_id = st.text_input("Enter Company ID (e.g., COMP001)")
                company_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if company_id in st.session_state.company_credentials and company_password == st.session_state.company_credentials[company_id]:
                        st.session_state.logged_in = True
                        st.session_state.user_id = company_id
                        st.rerun()
                    else:
                        st.error("❌ Invalid Company ID or Password")
        
        with col2:
            st.subheader("📝 Signup")
            with st.form("company_signup_form"):
                new_company_name = st.text_input("Company Name")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                if st.form_submit_button("Signup"):
                    if new_company_name and new_email and new_password:
                        new_id = f"COMP{len(st.session_state.companies) + 1:03d}"
                        new_company = {
                            'CompanyID': new_id,
                            'Name': new_company_name
                        }
                        st.session_state.companies = pd.concat([st.session_state.companies, pd.DataFrame([new_company])], ignore_index=True)
                        st.session_state.company_credentials[new_id] = new_password
                        st.success(f"✅ Signup successful! Your Company ID is {new_id}. Please login.")
                    else:
                        st.error("⚠️ Please complete all fields.")
    else:
        company_data = st.session_state.companies[st.session_state.companies['CompanyID'] == st.session_state.user_id].iloc[0]
        company_name = company_data['Name']
        
        # Company dashboard with tabs
        tab1, tab2, tab3 = st.tabs(["📋 Job Postings", "🎓 Candidate Matches", "📊 Analytics"])
        
        with tab1:
            st.subheader("📋 Post New Job")
            
            # Job posting form
            with st.form("job_posting_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.text_input("Company Name", value=company_name, disabled=True)
                    job_role = st.text_input("Job Role/Position")
                    num_openings = st.number_input("Number of Openings", min_value=1, value=1)
                
                with col2:
                    job_location = st.selectbox("Job Location", ["Remote", "Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Pune"])
                    experience_level = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Executive"])
                    salary_range = st.selectbox("Salary Range (LPA)", ["3-5", "5-8", "8-12", "12-18", "18+"])
                
                job_description = st.text_area("Job Description", height=120)
                
                # Skills selection
                all_skills = []
                for job_data in JOB_CATEGORIES.values():
                    all_skills.extend(job_data['keywords'])
                all_skills = sorted(list(set(all_skills)))
                
                required_skills = st.multiselect(
                    "Required Skills",
                    all_skills,
                    help="Select the key skills required for this position"
                )
                
                min_resume_score = st.slider("Minimum Resume Score", 0, 100, 75)
                min_test_score = st.slider("Minimum Test Score", 0, 100, 80)
                
                if st.form_submit_button("Post Job", type="primary"):
                    if job_role and job_description and required_skills:
                        new_job = {
                            'JobID': f"JOB{len(st.session_state.jobs) + 501}",
                            'Company': company_name,
                            'Role': job_role,
                            'Min Resume Score': min_resume_score,
                            'Min Test Score': min_test_score,
                            'Required Skills': required_skills,
                            'Location': job_location,
                            'Experience': experience_level,
                            'Salary': salary_range,
                            'Description': job_description,
                            'Openings': int(num_openings),
                            'Status': "Active"
                        }
                        st.session_state.jobs = pd.concat([st.session_state.jobs, pd.DataFrame([new_job])], ignore_index=True)
                        # Update company's Jobs_Posted count
                        company_index = st.session_state.companies[st.session_state.companies['CompanyID'] == st.session_state.user_id].index[0]
                        st.session_state.companies.loc[company_index, 'Jobs_Posted'] += 1
                        st.success(f"✅ Job '{job_role}' posted successfully!")
                        st.balloons()
                    else:
                        st.error("⚠️ Please fill all required fields and select at least one skill.")
            
            # Display existing job postings
            st.markdown("---")
            st.subheader("Your Posted Jobs")
            
            company_jobs = st.session_state.jobs[st.session_state.jobs['Company'] == company_name]
            
            if not company_jobs.empty:
                for index, job in company_jobs.iterrows():
                    with st.expander(f"{job['Role']} - {job.get('Location', 'N/A')} ({job.get('Status', 'Active')})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Company:** {job['Company']}")
                            st.write(f"**Experience:** {job.get('Experience', 'N/A')}")
                            st.write(f"**Salary:** {job.get('Salary', 'N/A')} LPA")
                            st.write(f"**Openings:** {job.get('Openings', 'N/A')}")
                        with col2:
                            st.write(f"**Skills:** {', '.join(job['Required Skills'][:5])}")
                            st.write(f"**Min Resume Score:** {job['Min Resume Score']}%")
                            st.write(f"**Min Test Score:** {job['Min Test Score']}%")
                        
                        st.write(f"**Description:** {job.get('Description', 'N/A')[:200]}...")
                        
                        # Job actions
                        col_edit, col_delete = st.columns(2)
                        with col_edit:
                            if st.button("Edit Job", key=f"edit_{index}"):
                                st.info("Edit functionality would be implemented here")
                        with col_delete:
                            if st.button("Delete Job", key=f"delete_{index}"):
                                st.session_state.jobs = st.session_state.jobs.drop(index)
                                st.rerun()
            else:
                st.info("No jobs posted yet. Create your first job posting above!")
        
        with tab2:
            st.subheader("🎓 Matched Candidates")
            
            company_jobs = st.session_state.jobs[st.session_state.jobs['Company'] == company_name]
            
            if not company_jobs.empty:
                for index, job_data in company_jobs.iterrows():
                    role = job_data['Role']
                    job_id = job_data['JobID']
                    
                    # Find matching students
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
                    
                    with st.expander(f"**{role}** ({job_id}) - {len(sorted_matches)} matching candidates", expanded=True):
                        if not sorted_matches:
                            st.info("No suitable student matches found for this role.")
                        else:
                            # Display candidates in a more structured format
                            for j, match in enumerate(sorted_matches):
                                if j > 0:
                                    st.markdown("---")
                                
                                col1, col2, col3 = st.columns([2, 2, 1])
                                
                                with col1:
                                    st.markdown(f"**{match['Name']}** ({match['StudentID']})")
                                    st.write(f"📚 {match['Degree']}")
                                    st.write(f"🏆 Resume: {match['Resume Score']}% | Test: {match['Test Score']}%")
                                
                                with col2:
                                    st.write("**Skills:**")
                                    skills_html = ""
                                    for skill in match['Skills']:
                                        if skill in job_data['Required Skills']:
                                            skills_html += f'<span style="background-color: #4CAF50; color: white; padding: 2px 6px; margin: 1px; border-radius: 8px; font-size: 11px;">{skill}</span> '
                                        else:
                                            skills_html += f'<span style="background-color: #e0e0e0; color: #333; padding: 2px 6px; margin: 1px; border-radius: 8px; font-size: 11px;">{skill}</span> '
                                    st.markdown(skills_html, unsafe_allow_html=True)
                                
                                with col3:
                                    # Match score with color coding
                                    score = match['Match Score']
                                    if score >= 80:
                                        score_color = "#4CAF50"  # Green
                                    elif score >= 60:
                                        score_color = "#FF9800"  # Orange
                                    else:
                                        score_color = "#F44336"  # Red
                                    
                                    st.markdown(f'<div style="text-align: center; padding: 10px; border-radius: 10px; background-color: {score_color}; color: white;"><strong>{score:.1f}%</strong><br>Match</div>', unsafe_allow_html=True)
                                    
                                    # Action buttons
                                    if st.button("Shortlist", key=f"shortlist_{job_id}_{match['StudentID']}", use_container_width=True):
                                        st.toast(f"✅ {match['Name']} shortlisted for {role}!")
                                    
                                    if st.button("View Profile", key=f"profile_{job_id}_{match['StudentID']}", use_container_width=True):
                                        st.info(f"Profile details for {match['Name']} would be shown here")
            else:
                st.info("No jobs posted yet. Post a job to see matched candidates!")
        
        with tab3:
            st.subheader("📊 Company Analytics")
            
            company_jobs = st.session_state.jobs[st.session_state.jobs['Company'] == company_name]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_jobs = len(company_jobs)
                st.metric("Jobs Posted", total_jobs)
            
            with col2:
                # Count matches from existing jobs
                total_matches = 0
                for _, job_data in company_jobs.iterrows():
                    for _, student in students_df.iterrows():
                        match_score = calculate_match(
                            student['Skills'], job_data['Required Skills'],
                            student['Resume Score'], job_data['Min Resume Score'],
                            student['Test Score'], job_data['Min Test Score']
                        )
                        if match_score > 0:
                            total_matches += 1
                st.metric("Total Matches", total_matches)
            
            with col3:
                st.metric("Applications", np.random.randint(50, 150))
            
            with col4:
                st.metric("Shortlisted", np.random.randint(10, 30))
            
            # Charts and visualizations
            st.markdown("---")
            
            # Skills demand chart
            if not company_jobs.empty:
                st.subheader("Skills in Demand")
                
                all_required_skills = []
                for _, job in company_jobs.iterrows():
                    all_required_skills.extend(job['Required Skills'])
                
                if all_required_skills:
                    skill_counts = Counter(all_required_skills)
                    skills_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Frequency'])
                    st.bar_chart(skills_df.set_index('Skill'))
            
            # Application trends (mock data)
            st.subheader("Application Trends")
            dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
            applications = np.random.randint(0, 20, len(dates))
            trends_df = pd.DataFrame({'Date': dates, 'Applications': applications})
            st.line_chart(trends_df.set_index('Date'))

# Run the dashboard
if __name__ == "__main__":
    display_company_dashboard()