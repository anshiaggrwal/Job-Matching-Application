import streamlit as st
import pandas as pd
import numpy as np
import re
import PyPDF2
import io
import docx
from typing import List, Dict
from collections import Counter
import os

# Set page config at the very beginning
st.set_page_config(page_title="Smart Job Portal", page_icon="💼", layout="wide")

# Job categories for skill selection (shared across all modules)
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

# CSS Styling
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
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
def initialize_session_state():
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
    if 'student_profiles' not in st.session_state:
        st.session_state.student_profiles = {}
    if 'company_jobs' not in st.session_state:
        st.session_state.company_jobs = {}
    if 'student_matches' not in st.session_state:
        st.session_state.student_matches = {}
    if 'extracted_skills' not in st.session_state:
        st.session_state.extracted_skills = []
    if 'resume_analyzed' not in st.session_state:
        st.session_state.resume_analyzed = False
    if 'test_results' not in st.session_state:
        st.session_state.test_results = {}

# Utility Functions for Resume Analysis
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def preprocess_text(text: str) -> str:
    """Clean and preprocess text"""
    text = text.lower()
    text = re.sub(r'[^\w\s\.\-\+\#\/]', ' ', text)
    text = ' '.join(text.split())
    return text

def extract_skills_from_text(text: str) -> List[str]:
    """Extract skills using keyword matching"""
    text = preprocess_text(text)
    found_skills = []
    
    all_keywords = set()
    for job_data in JOB_CATEGORIES.values():
        all_keywords.update([k.lower() for k in job_data['keywords']])
    
    for keyword in all_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text):
            found_skills.append(keyword)
    
    return list(set(found_skills))

def predict_job_from_skills(skills: List[str]) -> Dict:
    """Predict job title using traditional keyword matching"""
    job_scores = {}
    
    for job_title, job_data in JOB_CATEGORIES.items():
        score = 0
        matched_skills = []
        
        for skill in skills:
            if skill.lower() in [k.lower() for k in job_data['keywords']]:
                score += job_data['skills_weight']
                matched_skills.append(skill)
        
        total_possible = len(job_data['keywords'])
        match_percentage = (score / total_possible) * 100 if total_possible > 0 else 0
        
        job_scores[job_title] = {
            'score': match_percentage,
            'matched_skills': matched_skills,
            'total_matches': len(matched_skills),
            'confidence': min(match_percentage * 2, 100)
        }
    
    sorted_jobs = sorted(job_scores.items(), 
                        key=lambda x: (x[1]['score'], x[1]['total_matches']), 
                        reverse=True)
    
    return dict(sorted_jobs)

# Mock data functions
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

def calculate_match(student_skills, required_skills, student_resume, min_resume, student_test, min_test):
    if student_resume < min_resume or student_test < min_test:
        return 0
    common_skills = set(student_skills) & set(required_skills)
    skill_match_score = len(common_skills) / len(required_skills) if len(required_skills) > 0 else 0
    resume_score_ratio = (student_resume - min_resume) / (100 - min_resume) if (100 - min_resume) > 0 else 0
    test_score_ratio = (student_test - min_test) / (100 - min_test) if (100 - min_test) > 0 else 0
    final_score = (0.6 * skill_match_score) + (0.2 * resume_score_ratio) + (0.2 * test_score_ratio)
    return round(final_score * 100, 2)

def go_back():
    """Resets all relevant session state variables to return to the main page."""
    st.session_state.role = None
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.details_submitted = False
    st.rerun()

# Student Dashboard
def display_student_dashboard():
    st.header("🎓 Student Portal")
    students_df, jobs_df = get_matching_data()
    
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
        # Create tabs for student features
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Job Matches", "📄 Resume Analysis", "🎯 Skill Testing", "📊 Test Results"])
        
        with tab1:
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
        
        with tab2:
            st.subheader("📄 Resume Analysis")
            
            uploaded_file = st.file_uploader(
                "Choose your resume file",
                type=['pdf', 'docx', 'txt'],
                help="Upload your resume in PDF, DOCX, or TXT format"
            )
            
            if uploaded_file is not None:
                # Extract text based on file type
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_text = extract_text_from_docx(uploaded_file)
                else:  # txt file
                    resume_text = str(uploaded_file.read(), "utf-8")
                
                if resume_text:
                    st.success("✅ Resume uploaded successfully!")
                    
                    word_count = len(resume_text.split())
                    char_count = len(resume_text)
                    st.metric("Document Stats", f"{word_count} words, {char_count} characters")
                    
                    with st.expander("📋 View Extracted Text"):
                        st.text_area("Resume Content", resume_text[:1500] + "..." if len(resume_text) > 1500 else resume_text, height=200)
                    
                    # Extract skills
                    skills = extract_skills_from_text(resume_text)
                    st.session_state.extracted_skills = skills
                    st.session_state.resume_analyzed = True
                    
                    if skills:
                        st.subheader("🔧 Detected Skills")
                        
                        skill_html = ""
                        for skill in skills[:20]:
                            skill_html += f'<span style="background-color: #e1f5fe; color: #01579b; padding: 3px 8px; margin: 2px; border-radius: 12px; font-size: 12px; display: inline-block;">{skill}</span> '
                        
                        st.markdown(skill_html, unsafe_allow_html=True)
                        
                        if len(skills) > 20:
                            st.markdown(f"*...and {len(skills) - 20} more skills detected*")
                        
                        # Get job predictions
                        st.subheader("🎯 AI Job Title Predictions")
                        job_predictions = predict_job_from_skills(skills)
                        
                        for i, (job_title, job_data) in enumerate(list(job_predictions.items())[:6]):
                            if job_data['score'] > 0:
                                if i == 0:
                                    st.markdown(f"""
                                    <div style="border: 3px solid #4CAF50; border-radius: 15px; padding: 20px; margin: 15px 0; background: linear-gradient(135deg, #f0f8f0 0%, #e8f5e8 100%); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                                        <h3 style="color: #2E7D32; margin: 0; display: flex; align-items: center;">
                                            🏆 #{i+1} {job_title}
                                        </h3>
                                        <div style="margin: 10px 0;">
                                            <strong>🎯 Match Score:</strong> <span style="color: #2E7D32; font-size: 18px;">{job_data['score']:.1f}%</span>
                                        </div>
                                        <div style="margin: 5px 0;">
                                            <strong>✅ Skills Matched:</strong> {job_data['total_matches']} skills
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    confidence_color = "#4CAF50" if job_data['confidence'] > 60 else "#FF9800" if job_data['confidence'] > 30 else "#f44336"
                                    st.markdown(f"""
                                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #fafafa;">
                                        <h4 style="margin: 0; color: #333;">#{i+1} {job_title}</h4>
                                        <div style="margin: 8px 0; display: flex; justify-content: space-between;">
                                            <span><strong>Match:</strong> {job_data['score']:.1f}%</span>
                                            <span><strong>Skills:</strong> {job_data['total_matches']}</span>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
        
        with tab3:
            if st.session_state.resume_analyzed and st.session_state.extracted_skills:
                st.subheader("🎯 Skill Testing")
                st.info("Interactive skill testing feature would be implemented here")
                st.markdown("Available skills for testing:")
                for skill in st.session_state.extracted_skills[:10]:
                    if st.button(f"Test {skill.title()}", key=f"test_{skill}"):
                        # Simulate test results
                        score = np.random.randint(60, 100)
                        if skill not in st.session_state.test_results:
                            st.session_state.test_results[skill] = {
                                'score': score,
                                'percentage': score,
                                'status': 'Expert' if score >= 80 else 'Intermediate' if score >= 60 else 'Beginner'
                            }
                        st.success(f"Test completed! You scored {score}% in {skill.title()}")
            else:
                st.info("📄 Please analyze your resume first to unlock skill testing!")
        
        with tab4:
            st.subheader("📊 Test Results Dashboard")
            
            if st.session_state.test_results:
                total_tests = len(st.session_state.test_results)
                avg_score = sum(r.get('percentage', 0) for r in st.session_state.test_results.values()) / total_tests
                expert_skills = sum(1 for r in st.session_state.test_results.values() if r.get('percentage', 0) >= 80)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Skills Tested", total_tests)
                with col2:
                    st.metric("Average Score", f"{avg_score:.1f}%")
                with col3:
                    st.metric("Expert Level Skills", expert_skills)
                
                for skill, result in st.session_state.test_results.items():
                    with st.expander(f"{skill.title()} - {result.get('percentage', 0):.1f}%"):
                        st.write(f"**Status:** {result.get('status', 'Unknown')}")
                        st.write(f"**Score:** {result.get('percentage', 0):.1f}%")
            else:
                st.info("🎯 No test results yet! Complete a skill test to see your results here.")

# Company Dashboard
def display_company_dashboard():
    st.header("🏢 Company Portal")
    students_df, jobs_df = get_matching_data()
    
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
    else:
        tab1, tab2 = st.tabs(["📋 Job Postings", "🎓 Candidate Matches"])
        
        with tab1:
            st.subheader("📋 Post New Job")
            with st.form("job_posting_form"):
                company_name = st.text_input("Company Name")
                job_role = st.text_input("Job Role")
                job_description = st.text_area("Job Description")
                required_skills = st.multiselect(
                    "Required Skills",
                    [skill for job in JOB_CATEGORIES.values() for skill in job['keywords']]
                )
                num_openings = st.number_input("Number of Openings", min_value=1, value=1)
                
                if st.form_submit_button("Post Job"):
                    if company_name and job_role and job_description and required_skills:
                        if 'company_jobs' not in st.session_state:
                            st.session_state.company_jobs = {}
                        if st.session_state.user_id not in st.session_state.company_jobs:
                            st.session_state.company_jobs[st.session_state.user_id] = []
                        
                        st.session_state.company_jobs[st.session_state.user_id].append({
                            "name": company_name,
                            "openings": num_openings,
                            "role": job_role,
                            "description": job_description,
                            "required_skills": required_skills
                        })
                        st.success(f"🎯 Job '{job_role}' posted successfully!")
                    else:
                        st.error("⚠️ Please fill all required fields.")
        
        with tab2:
            company_name_map = {"COMP001": "Innovatech"}
            company_name = company_name_map.get(st.session_state.user_id, "Unknown Company")
            
            st.subheader("🎓 Matched Candidates")
            company_jobs = jobs_df[jobs_df['Company'] == company_name]

            if company_jobs.empty:
                st.info("No job postings found.")
            else:
                for index, job_data in company_jobs.iterrows():
                    role = job_data['Role']
                    job_id = job_data['JobID']
                    
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
                    
                    with st.expander(f"**{role}** ({job_id}) - {len(sorted_matches)} matching candidates"):
                        if not sorted_matches:
                            st.info("No suitable student matches found for this role.")
                        else:
                            for match in sorted_matches:
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.write(f"**{match['Name']}**")
                                    st.write(f"Degree: {match['Degree']}")
                                    st.caption(f"Skills: {', '.join(match['Skills'])}")
                                with col2:
                                    st.metric("Match", f"{match['Match Score']}%")
                                    if st.button("Shortlist", key=f"shortlist_{job_id}_{match['StudentID']}"):
                                        st.toast(f"✅ {match['Name']} shortlisted!")
                                st.markdown("---")

# Admin Dashboard
def display_admin_dashboard():
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
        # Mock admin data
        admin_students = pd.DataFrame({
            'StudentID': [f'STU{1000+i}' for i in range(1, 21)],
            'Name': [f'Student {i}' for i in range(1, 21)],
            'College': np.random.choice(['Tech University', 'Global Institute', 'City College'], 20),
            'Verified': np.random.choice([True, False], 20, p=[0.8, 0.2])
        })
        
        admin_companies = pd.DataFrame({
            'CompanyID': [f'COMP{100+i}' for i in range(1, 11)],
            'Name': [f'Company {i}' for i in range(1, 11)],
            'Industry': np.random.choice(['SaaS', 'FinTech', 'AI/ML'], 10),
            'Status': np.random.choice(['Verified', 'Pending'], 10, p=[0.7, 0.3])
        })
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🎓 Students", "🏢 Companies", "⚙️ Settings"])
        
        with tab1:
            st.subheader("📊 Dashboard Analytics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Students", len(admin_students))
            col2.metric("Total Companies", len(admin_companies))
            col3.metric("Verified Companies", admin_companies[admin_companies['Status'] == 'Verified'].shape[0])
            col4.metric("Pending Approvals", admin_companies[admin_companies['Status'] == 'Pending'].shape[0])
        
        with tab2:
            st.subheader("🎓 Manage Students")
            st.dataframe(admin_students, use_container_width=True)
        
        with tab3:
            st.subheader("🏢 Manage Companies")
            st.dataframe(admin_companies, use_container_width=True)
        
        with tab4:
            st.subheader("⚙️ Portal Settings")
            new_announcement = st.text_area("Site-wide announcement", value=st.session_state.announcement)
            if st.button("Update Announcement"):
                st.session_state.announcement = new_announcement
                st.success("Announcement updated!")

# Main Application
def main():
    initialize_session_state()
    
    # Header
    st.markdown('<p class="big-title">💼 Smart Job Portal</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Connecting Students & Companies through AI-powered matching</p>', unsafe_allow_html=True)
    
    # Role selection or dashboard
    if st.session_state.role is None:
        # Show announcement if available
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

        # Statistics display
        st.markdown("---")
        colA, colB, colC = st.columns(3)
        with colA:
            st.metric("Students Registered", "2,340")
        with colB:
            st.metric("Companies Onboarded", "120")
        with colC:
            st.metric("Jobs Posted", "450+")

    else:
        # Show back button
        st.button("⬅️ Back to Home", on_click=go_back)
        
        # Route to appropriate dashboard based on role
        if st.session_state.role == "student":
            display_student_dashboard()
        elif st.session_state.role == "company":
            display_company_dashboard()
        elif st.session_state.role == "admin":
            display_admin_dashboard()

if __name__ == "__main__":
    main()