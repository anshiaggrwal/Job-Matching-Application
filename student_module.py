import streamlit as st
import re
import PyPDF2
import io
import docx
from typing import List, Dict
import pandas as pd
import numpy as np
import skill_testing_module as stm  # Assuming the provided skill_testing_module.py is saved in the same directory

# Job categories for skill selection (unchanged)
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

# Utility functions (unchanged)
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
    """Predict job title using keyword matching"""
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

# Initialize data in session state (moved from @st.cache_data to allow modifications)
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

if 'user_credentials' not in st.session_state:
    st.session_state.user_credentials = {row['StudentID']: "stu@1234" for index, row in st.session_state.students.iterrows()}

def calculate_match(student_skills, required_skills, student_resume, min_resume, student_test, min_test):
    if student_resume < min_resume or student_test < min_test:
        return 0
    common_skills = set(student_skills) & set(required_skills)
    skill_match_score = len(common_skills) / len(required_skills) if len(required_skills) > 0 else 0
    resume_score_ratio = (student_resume - min_resume) / (100 - min_resume) if (100 - min_resume) > 0 else 0
    test_score_ratio = (student_test - min_test) / (100 - min_test) if (100 - min_test) > 0 else 0
    final_score = (0.6 * skill_match_score) + (0.2 * resume_score_ratio) + (0.2 * test_score_ratio)
    return round(final_score * 100, 2)

def display_student_dashboard():
    """Main student dashboard function"""
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
    unsafe_allow_html=True)
    
    st.header("🎓 Student Portal")
    
    # Initialize session state if not present
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'details_submitted' not in st.session_state:
        st.session_state.details_submitted = False
    if 'extracted_skills' not in st.session_state:
        st.session_state.extracted_skills = []
    if 'resume_analyzed' not in st.session_state:
        st.session_state.resume_analyzed = False
    if 'test_results' not in st.session_state:
        st.session_state.test_results = {}
    
    if not st.session_state.logged_in:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔑 Login")
            with st.form("student_login_form"):
                student_id = st.text_input("Enter Student ID (e.g., STU1001)")
                student_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if student_id in st.session_state.user_credentials and student_password == st.session_state.user_credentials[student_id]:
                        st.session_state.logged_in = True
                        st.session_state.user_id = student_id
                        st.session_state.details_submitted = True  # Assume details already submitted for existing users
                        st.rerun()
                    else:
                        st.error("❌ Invalid Student ID or Password")
        
        with col2:
            st.subheader("📝 Signup")
            with st.form("student_signup_form"):
                new_name = st.text_input("Full Name")
                new_degree = st.text_input("Degree")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                if st.form_submit_button("Signup"):
                    if new_name and new_degree and new_email and new_password:
                        new_id = f"STU{len(st.session_state.students) + 1001}"
                        new_student = {
                            'StudentID': new_id,
                            'Name': new_name,
                            'Degree': new_degree,
                            'Resume Score': 0,
                            'Test Score': 0,
                            'Skills': []
                        }
                        st.session_state.students = pd.concat([st.session_state.students, pd.DataFrame([new_student])], ignore_index=True)
                        st.session_state.user_credentials[new_id] = new_password
                        st.success(f"✅ Signup successful! Your Student ID is {new_id}. Please login.")
                    else:
                        st.error("⚠️ Please complete all fields.")
    else:
        student_data = st.session_state.students[st.session_state.students['StudentID'] == st.session_state.user_id].iloc[0]
        
        # Create tabs for student features
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Job Matches", "📄 Resume Analysis", "🎯 Skill Testing", "📊 Test Results"])
        
        with tab1:
            st.success(f"🎉 Welcome {student_data['Name']}! Here are your recommended jobs.")
            st.subheader(f"Recommended Jobs for {student_data['Name']}")
            
            matches = []
            for index, job in st.session_state.jobs.iterrows():
                match_score = calculate_match(
                    student_data['Skills'], job['Required Skills'],
                    student_data['Resume Score'], job['Min Resume Score'],
                    student_data['Test Score'], job['Min Test Score']
                )
                if match_score > 0:  # Only show jobs with positive match score (hiding non-matching "admin things")
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
                stm.add_skill_testing_tab(st.session_state.extracted_skills)
            else:
                st.info("📄 Please analyze your resume first to unlock skill testing!")
        
        with tab4:
            stm.display_test_results()

# Run the dashboard
if __name__ == "__main__":
    display_student_dashboard()