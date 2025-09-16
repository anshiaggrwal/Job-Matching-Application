import streamlit as st
import re
import requests
import json
from typing import List, Dict
import PyPDF2
import io
import docx
from collections import Counter

# Job title mappings based on skills
SKILL_TO_JOB_MAPPING = {
    'backend_developer': {
        'keywords': ['python', 'java', 'nodejs', 'django', 'flask', 'spring', 'express', 'api', 'rest', 'mongodb', 'postgresql', 'mysql', 'redis', 'microservices', 'docker', 'kubernetes'],
        'weight': 1.0
    },
    'frontend_developer': {
        'keywords': ['react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css', 'sass', 'webpack', 'bootstrap', 'tailwind', 'jquery', 'nextjs', 'nuxtjs'],
        'weight': 1.0
    },
    'full_stack_developer': {
        'keywords': ['react', 'nodejs', 'python', 'django', 'flask', 'javascript', 'mongodb', 'postgresql', 'api', 'rest', 'html', 'css'],
        'weight': 1.2
    },
    'data_scientist': {
        'keywords': ['python', 'r', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter', 'machine learning', 'deep learning', 'statistics'],
        'weight': 1.0
    },
    'machine_learning_engineer': {
        'keywords': ['python', 'tensorflow', 'pytorch', 'scikit-learn', 'mlops', 'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'machine learning', 'deep learning'],
        'weight': 1.0
    },
    'devops_engineer': {
        'keywords': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform', 'ansible', 'jenkins', 'gitlab', 'ci/cd', 'linux', 'bash', 'monitoring'],
        'weight': 1.0
    },
    'mobile_developer': {
        'keywords': ['react native', 'flutter', 'swift', 'kotlin', 'android', 'ios', 'xamarin', 'cordova', 'ionic'],
        'weight': 1.0
    },
    'ui_ux_designer': {
        'keywords': ['figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator', 'wireframing', 'prototyping', 'user research', 'design thinking'],
        'weight': 1.0
    },
    'qa_engineer': {
        'keywords': ['selenium', 'cypress', 'jest', 'junit', 'testing', 'automation', 'manual testing', 'api testing', 'performance testing'],
        'weight': 1.0
    },
    'product_manager': {
        'keywords': ['product management', 'agile', 'scrum', 'roadmap', 'stakeholder', 'user stories', 'analytics', 'a/b testing', 'jira', 'confluence'],
        'weight': 1.0
    },
    'cybersecurity_analyst': {
        'keywords': ['security', 'penetration testing', 'vulnerability', 'firewall', 'encryption', 'compliance', 'risk assessment', 'incident response'],
        'weight': 1.0
    }
}

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
    # Convert to lowercase
    text = text.lower()
    # Remove special characters but keep spaces and common punctuation
    text = re.sub(r'[^\w\s\.\-\+\#]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def extract_skills(text: str) -> List[str]:
    """Extract skills from text using keyword matching"""
    text = preprocess_text(text)
    found_skills = []
    
    # Collect all possible skills from job mappings
    all_skills = set()
    for job_data in SKILL_TO_JOB_MAPPING.values():
        all_skills.update(job_data['keywords'])
    
    # Find skills in text
    for skill in all_skills:
        # Use word boundaries for exact matches
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
            found_skills.append(skill)
    
    return found_skills

def predict_job_title(skills: List[str]) -> Dict:
    """Predict job title based on extracted skills"""
    job_scores = {}
    
    for job_title, job_data in SKILL_TO_JOB_MAPPING.items():
        score = 0
        matched_skills = []
        
        for skill in skills:
            if skill.lower() in [k.lower() for k in job_data['keywords']]:
                score += job_data['weight']
                matched_skills.append(skill)
        
        # Normalize score by number of total keywords for the job
        normalized_score = score / len(job_data['keywords']) if job_data['keywords'] else 0
        
        job_scores[job_title] = {
            'score': normalized_score,
            'matched_skills': matched_skills,
            'total_matches': len(matched_skills)
        }
    
    # Sort by score
    sorted_jobs = sorted(job_scores.items(), key=lambda x: (x[1]['score'], x[1]['total_matches']), reverse=True)
    
    return dict(sorted_jobs)

def format_job_title(job_key: str) -> str:
    """Format job title for display"""
    return job_key.replace('_', ' ').title()

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Resume Job Title Predictor",
        page_icon="💼",
        layout="wide"
    )
    
    st.title("💼 Resume Job Title Predictor")
    st.markdown("Upload your resume and get AI-powered job title predictions based on your skills!")
    
    # Sidebar for information
    with st.sidebar:
        st.markdown("### How it works:")
        st.markdown("""
        1. **Upload** your resume (PDF, DOCX, or TXT)
        2. **Extract** skills and technologies from your resume
        3. **Analyze** skills against job profiles
        4. **Predict** the most suitable job titles
        """)
        
        st.markdown("### Supported Job Titles:")
        for job_key in SKILL_TO_JOB_MAPPING.keys():
            st.markdown(f"• {format_job_title(job_key)}")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Upload Resume")
        
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
                
                with st.expander("📋 View Extracted Text"):
                    st.text_area("Resume Content", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200)
                
                # Extract skills
                skills = extract_skills(resume_text)
                
                if skills:
                    st.subheader("🔧 Detected Skills")
                    
                    # Display skills as tags
                    skill_cols = st.columns(3)
                    for i, skill in enumerate(skills[:15]):  # Show first 15 skills
                        with skill_cols[i % 3]:
                            st.markdown(f"`{skill}`")
                    
                    if len(skills) > 15:
                        st.markdown(f"*...and {len(skills) - 15} more skills*")
    
    with col2:
        if uploaded_file is not None and resume_text:
            st.subheader("🎯 Job Title Predictions")
            
            # Get predictions
            job_predictions = predict_job_title(skills)
            
            if job_predictions:
                # Display top 5 predictions
                for i, (job_key, job_data) in enumerate(list(job_predictions.items())[:5]):
                    if job_data['score'] > 0:  # Only show jobs with matches
                        job_title = format_job_title(job_key)
                        
                        # Create a card-like display
                        with st.container():
                            if i == 0:
                                st.markdown(f"""
                                <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #f0f8f0;">
                                    <h3 style="color: #2E7D32; margin: 0;">🏆 #{i+1} {job_title}</h3>
                                    <p style="margin: 5px 0;"><strong>Match Score:</strong> {job_data['score']:.2%}</p>
                                    <p style="margin: 5px 0;"><strong>Skills Matched:</strong> {job_data['total_matches']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin: 8px 0;">
                                    <h4 style="margin: 0;">#{i+1} {job_title}</h4>
                                    <p style="margin: 5px 0;"><strong>Match Score:</strong> {job_data['score']:.2%}</p>
                                    <p style="margin: 5px 0;"><strong>Skills Matched:</strong> {job_data['total_matches']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Show matched skills
                            if job_data['matched_skills']:
                                st.markdown("**Matched Skills:**")
                                matched_skills_text = ", ".join(job_data['matched_skills'][:5])
                                if len(job_data['matched_skills']) > 5:
                                    matched_skills_text += f" (+{len(job_data['matched_skills']) - 5} more)"
                                st.markdown(f"*{matched_skills_text}*")
                            
                            st.markdown("---")
                
                # Additional insights
                st.subheader("📊 Analysis Summary")
                total_skills = len(skills)
                st.metric("Total Skills Detected", total_skills)
                
                if job_predictions:
                    best_match = list(job_predictions.items())[0]
                    st.metric("Best Match Confidence", f"{best_match[1]['score']:.1%}")
            
            else:
                st.warning("⚠️ No matching skills found. Please make sure your resume contains technical skills and keywords.")
        
        elif uploaded_file is None:
            st.info("👆 Please upload your resume to get job title predictions.")

if __name__ == "__main__":
    main()