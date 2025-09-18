import streamlit as st

# Job categories for skill selection
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
        "imports": ["docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible", "jenkins", "gitlab", "ci/cd", "linux", "bash", "monitoring", "infrastructure"],
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

def display_login_page():
    """Display the login page with Foundation role"""
    st.set_page_config(page_title="Smart Job Portal", page_icon="💼", layout="wide")

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

    if st.session_state.role is None:
        st.subheader("Choose Your Role to Continue")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="highlight-box">🎓 <br> I am a Student</div>', unsafe_allow_html=True)
            if st.button("Login as Student"):
                st.session_state.role = "student"

        with col2:
            st.markdown('<div class="highlight-box">🏢 <br> I am a Company</div>', unsafe_allow_html=True)
            if st.button("Login as Company"):
                st.session_state.role = "company"

        with col3:
            st.markdown('<div class="highlight-box">🤝 <br> I am a Foundation</div>', unsafe_allow_html=True)
            if st.button("Login as Foundation"):
                st.session_state.role = "foundation"

        st.markdown("---")
        colA, colB, colC = st.columns(3)
        with colA:
            st.metric("Students Registered", "2,340")
        with colB:
            st.metric("Companies Onboarded", "120")
        with colC:
            st.metric("Jobs Posted", "450+")

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
                    required_skills = st.multiselect("Select Required Skills",
                                                    [skill for job in JOB_CATEGORIES.values() for skill in job['keywords']],
                                                    help="Select skills required for this job")
                    save_job = st.form_submit_button("Submit Job Details")
                
                if save_job:
                    if company_name and job_role and job_description and required_skills:
                        if 'company_jobs' not in st.session_state:
                            st.session_state.company_jobs = {}
                        if company_id not in st.session_state.company_jobs:
                            st.session_state.company_jobs[company_id] = []
                        st.session_state.company_jobs[company_id].append({
                            "name": company_name,
                            "openings": num_openings,
                            "role": job_role,
                            "description": job_description,
                            "keywords": required_skills,
                            "required_skills": required_skills
                        })
                        st.session_state.logged_in = True
                        st.session_state.company_id = company_id
                        st.success(f"🎯 Job '{job_role}' added successfully!")
                        st.info("Your job has been submitted and will be matched with student profiles.")
                    else:
                        st.error("⚠️ Please fill all job details and select at least one skill.")
            else:
                st.error("❌ Invalid Company ID or Password")

        if st.button("⬅️ Back"):
            st.session_state.role = None

    elif st.session_state.role == "student":
        st.error("❌ Please access the Student Dashboard via main.py")
        if st.button("⬅️ Back"):
            st.session_state.role = None

    elif st.session_state.role == "foundation":
        st.error("❌ Please access the Foundation Dashboard via organisation.py")
        if st.button("⬅️ Back"):
            st.session_state.role = None

def display_company_interface():
    """Display the company interface to view jobs and matched students"""
    st.set_page_config(page_title="Company Dashboard - Smart Job Portal", page_icon="🏢", layout="wide")
    st.title("🏢 Company Dashboard")
    st.markdown("View your job postings and matched student profiles.")

    company_id = st.session_state.company_id

    if 'company_jobs' in st.session_state and company_id in st.session_state.company_jobs:
        st.subheader("📋 Your Job Postings")
        for job in st.session_state.company_jobs[company_id]:
            with st.expander(f"Job: {job['role']} at {job['name']}"):
                st.write(f"**Openings:** {job['openings']}")
                st.write(f"**Description:** {job['description']}")
                st.write(f"**Required Skills:** {', '.join(job['required_skills'])}")
        
        st.subheader("🎓 Matched Student Profiles")
        if 'student_matches' in st.session_state and company_id in st.session_state.student_matches:
            for student_id, matches in st.session_state.student_matches.items():
                for match in matches:
                    if match['company_id'] == company_id:
                        with st.expander(f"Student {student_id} - Match Score: {match['match_score']:.1f}%"):
                            student = st.session_state.student_profiles.get(student_id, {})
                            st.write(f"**Name:** {student.get('name', 'N/A')}")
                            st.write(f"**Email:** {student.get('email', 'N/A')}")
                            st.write(f"**College:** {student.get('college', 'N/A')}")
                            st.write(f"**Degree:** {student.get('degree', 'N/A')}")
                            st.write(f"**Matched Skills:** {', '.join(match['matched_skills'])}")
                            st.write(f"**Test Score:** {match['test_score']:.1f}%")
        else:
            st.info("No student profiles matched yet. Please wait for the Foundation to process matches.")
    else:
        st.info("No job postings found. Please add a job in the login section.")

def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'student_profiles' not in st.session_state:
        st.session_state.student_profiles = {}
    if 'company_jobs' not in st.session_state:
        st.session_state.company_jobs = {}
    if 'student_matches' not in st.session_state:
        st.session_state.student_matches = {}

    # Check if user is logged in and has the correct role
    if not st.session_state.logged_in:
        display_login_page()
    elif st.session_state.role != "company":
        st.error("❌ This page is for companies only. Please access the correct dashboard.")
    else:
        display_company_interface()

if __name__ == "__main__":
    main()