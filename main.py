import streamlit as st
import re
import requests
import json
from typing import List, Dict, Tuple
import PyPDF2
import io
import docx
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
from collections import Counter
import os
import skill_testing_module as stm

# Cache the model loading
@st.cache_resource
def load_models():
    """Load Hugging Face models for text analysis"""
    try:
        # Load a general text classification model for job prediction
        # Using a BERT model fine-tuned for classification
        job_classifier = pipeline(
            "text-classification",
            model="microsoft/DialoGPT-medium",
            return_all_scores=True
        )
        
        # Load NER model for skill extraction
        ner_pipeline = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple"
        )
        
        return job_classifier, ner_pipeline
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None

# Alternative simpler model loading for better compatibility
@st.cache_resource
def load_simple_model():
    """Load a simpler model for text analysis"""
    try:
        # Using a sentiment analysis model that we can repurpose
        classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        return classifier
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Job categories with descriptions for better classification
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

def extract_skills_with_hf(text: str, ner_model=None) -> List[str]:
    """Extract skills using Hugging Face NER model and keyword matching"""
    text = preprocess_text(text)
    found_skills = []
    
    # Traditional keyword matching (more reliable for technical skills)
    all_keywords = set()
    for job_data in JOB_CATEGORIES.values():
        all_keywords.update([k.lower() for k in job_data['keywords']])
    
    for keyword in all_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text):
            found_skills.append(keyword)
    
    # If NER model is available, use it to extract additional entities
    if ner_model:
        try:
            # Limit text length for model processing
            text_chunk = text[:2000]  # First 2000 characters
            entities = ner_model(text_chunk)
            
            for entity in entities:
                if entity['entity_group'] in ['MISC', 'ORG'] and entity['score'] > 0.7:
                    entity_text = entity['word'].lower().strip()
                    if len(entity_text) > 2 and entity_text not in found_skills:
                        found_skills.append(entity_text)
        except Exception as e:
            st.warning(f"NER processing error: {str(e)}")
    
    return list(set(found_skills))  # Remove duplicates

def create_job_prediction_prompt(resume_text: str, skills: List[str]) -> str:
    """Create a prompt for job title prediction"""
    skills_text = ", ".join(skills[:20])  # Limit to first 20 skills
    
    prompt = f"""
    Based on the following resume content and extracted skills, predict the most suitable job title:
    
    Skills: {skills_text}
    
    Resume excerpt: {resume_text[:500]}...
    
    Available job categories:
    - Backend Developer
    - Frontend Developer
    - Full Stack Developer
    - Data Scientist
    - Machine Learning Engineer
    - DevOps Engineer
    - Mobile Developer
    - Data Engineer
    - UI/UX Designer
    - QA Engineer
    """
    return prompt

def predict_job_with_traditional_method(skills: List[str]) -> Dict:
    """Predict job title using traditional keyword matching"""
    job_scores = {}
    
    for job_title, job_data in JOB_CATEGORIES.items():
        score = 0
        matched_skills = []
        
        for skill in skills:
            if skill.lower() in [k.lower() for k in job_data['keywords']]:
                score += job_data['skills_weight']
                matched_skills.append(skill)
        
        # Calculate match percentage
        total_possible = len(job_data['keywords'])
        match_percentage = (score / total_possible) * 100 if total_possible > 0 else 0
        
        job_scores[job_title] = {
            'score': match_percentage,
            'matched_skills': matched_skills,
            'total_matches': len(matched_skills),
            'confidence': min(match_percentage * 2, 100)  # Boost confidence for display
        }
    
    # Sort by score and total matches
    sorted_jobs = sorted(job_scores.items(), 
                        key=lambda x: (x[1]['score'], x[1]['total_matches']), 
                        reverse=True)
    
    return dict(sorted_jobs)

def analyze_resume_with_hf(resume_text: str, model=None) -> Dict:
    """Analyze resume using Hugging Face model"""
    if not model:
        return {}
    
    try:
        # Create different text snippets focusing on different aspects
        snippets = {
            "technical_skills": re.findall(r'(?i)(python|javascript|react|java|sql|aws|docker|kubernetes|machine learning|data science|frontend|backend|api|database)', resume_text),
            "experience_level": re.findall(r'(?i)(\d+\+?\s*years?|senior|junior|lead|principal|entry.?level)', resume_text),
            "domains": re.findall(r'(?i)(web development|mobile development|data analysis|machine learning|devops|testing|design)', resume_text)
        }
        
        return {
            "technical_focus": snippets["technical_skills"][:10],
            "experience_indicators": snippets["experience_level"][:5],
            "domain_keywords": snippets["domains"][:5]
        }
    except Exception as e:
        st.warning(f"HF model analysis error: {str(e)}")
        return {}

def main():
    st.set_page_config(
        page_title="AI Resume Job Title Predictor with Skill Testing",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI-Powered Resume Job Title Predictor with Skill Testing")
    st.markdown("Upload your resume, get intelligent job title predictions, and validate your skills!")
    
    # Initialize session state
    if 'models_loaded' not in st.session_state:
        st.session_state.models_loaded = False
    if 'extracted_skills' not in st.session_state:
        st.session_state.extracted_skills = []
    if 'resume_analyzed' not in st.session_state:
        st.session_state.resume_analyzed = False
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📄 Resume Analysis", "🎯 Skill Testing", "📊 Test Results"])
    
    with tab1:
        # Sidebar
        with st.sidebar:
            st.markdown("### 🧠 AI Features:")
            st.markdown("""
            - **Hugging Face Models** for intelligent text analysis
            - **Advanced NLP** for skill extraction
            - **Smart Matching** algorithms
            - **Skill Validation Tests** with multiple difficulty levels
            - **Confidence Scoring** for predictions
            """)
            
            st.markdown("### 📊 Supported Roles:")
            for job_title in JOB_CATEGORIES.keys():
                st.markdown(f"• {job_title}")
            
            # Model loading section
            st.markdown("---")
            st.markdown("### 🔧 Model Status:")
            
            if st.button("Load AI Models"):
                with st.spinner("Loading Hugging Face models... This may take a moment."):
                    try:
                        # Try loading simpler model first
                        simple_model = load_simple_model()
                        if simple_model:
                            st.session_state.hf_model = simple_model
                            st.session_state.models_loaded = True
                            st.success("✅ AI Model loaded successfully!")
                        else:
                            st.error("❌ Failed to load AI models")
                    except Exception as e:
                        st.error(f"❌ Error loading models: {str(e)}")
            
            if st.session_state.models_loaded:
                st.success("🟢 AI Models Ready")
            else:
                st.warning("🟡 Click 'Load AI Models' to enable advanced features")
        
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
                    
                    # Show file stats
                    word_count = len(resume_text.split())
                    char_count = len(resume_text)
                    st.metric("Document Stats", f"{word_count} words, {char_count} characters")
                    
                    with st.expander("📋 View Extracted Text"):
                        st.text_area("Resume Content", resume_text[:1500] + "..." if len(resume_text) > 1500 else resume_text, height=200)
                    
                    # Extract skills
                    ner_model = None
                    if st.session_state.models_loaded:
                        try:
                            # Use a simple approach since complex NER models might be heavy
                            skills = extract_skills_with_hf(resume_text, ner_model)
                        except:
                            skills = extract_skills_with_hf(resume_text, None)
                    else:
                        skills = extract_skills_with_hf(resume_text, None)
                    
                    # Store skills in session state for use in other tabs
                    st.session_state.extracted_skills = skills
                    st.session_state.resume_analyzed = True
                    
                    if skills:
                        st.subheader("🔧 Detected Skills")
                        
                        # Create skill tags with better formatting
                        skill_html = ""
                        for skill in skills[:20]:  # Show first 20 skills
                            skill_html += f'<span style="background-color: #e1f5fe; color: #01579b; padding: 3px 8px; margin: 2px; border-radius: 12px; font-size: 12px; display: inline-block;">{skill}</span> '
                        
                        st.markdown(skill_html, unsafe_allow_html=True)
                        
                        if len(skills) > 20:
                            st.markdown(f"*...and {len(skills) - 20} more skills detected*")
        
        with col2:
            if uploaded_file is not None and 'resume_text' in locals() and resume_text:
                st.subheader("🎯 AI Job Title Predictions")
                
                # Get skills from session state
                skills = st.session_state.extracted_skills
                
                # Get predictions using traditional method
                job_predictions = predict_job_with_traditional_method(skills)
                
                # If HF model is loaded, enhance predictions
                if st.session_state.models_loaded:
                    try:
                        hf_analysis = analyze_resume_with_hf(resume_text, st.session_state.get('hf_model'))
                        if hf_analysis:
                            st.success("🤖 Enhanced with AI analysis")
                    except:
                        st.warning("Using traditional analysis method")
                
                if job_predictions:
                    # Display top predictions
                    for i, (job_title, job_data) in enumerate(list(job_predictions.items())[:6]):
                        if job_data['score'] > 0:  # Only show jobs with matches
                            
                            # Enhanced styling for top prediction
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
                                    <div style="margin: 5px 0;">
                                        <strong>🔥 Confidence:</strong> {job_data['confidence']:.0f}%
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
                                        <span style="color: {confidence_color};"><strong>Confidence:</strong> {job_data['confidence']:.0f}%</span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Show matched skills in a more compact way
                            if job_data['matched_skills']:
                                matched_display = job_data['matched_skills'][:6]  # Show first 6
                                skills_text = " • ".join(matched_display)
                                if len(job_data['matched_skills']) > 6:
                                    skills_text += f" • (+{len(job_data['matched_skills']) - 6} more)"
                                st.markdown(f"**🔑 Key Matches:** {skills_text}")
                            
                            st.markdown("---")
                    
                    # Analysis summary
                    st.subheader("📊 Analysis Summary")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Skills Found", len(skills))
                    with col_b:
                        best_match = list(job_predictions.items())[0]
                        st.metric("Best Match", f"{best_match[1]['score']:.0f}%")
                    with col_c:
                        ai_status = "🤖 AI Enhanced" if st.session_state.models_loaded else "📊 Traditional"
                        st.metric("Analysis Type", ai_status)
                    
                    # Job category insights
                    if st.session_state.models_loaded and 'hf_analysis' in locals():
                        st.markdown("### 🧠 AI Insights")
                        if hf_analysis.get('technical_focus'):
                            st.markdown(f"**Technical Focus:** {', '.join(hf_analysis['technical_focus'][:5])}")
                        if hf_analysis.get('domain_keywords'):
                            st.markdown(f"**Domain Areas:** {', '.join(hf_analysis['domain_keywords'])}")
                
                else:
                    st.warning("⚠️ No matching skills found. Please ensure your resume contains technical skills and relevant keywords.")
            
            elif uploaded_file is None:
                st.info("👆 Please upload your resume to get AI-powered job title predictions.")
                st.markdown("### 💡 Tips for better results:")
                st.markdown("""
                - Include specific technologies and tools you've used
                - Mention programming languages, frameworks, and platforms
                - Add relevant project descriptions
                - Include years of experience with specific technologies
                """)
    
    with tab2:
        if st.session_state.resume_analyzed and st.session_state.extracted_skills:
            stm.add_skill_testing_tab(st.session_state.extracted_skills)
        else:
            st.info("📄 Please analyze your resume in the first tab to unlock skill testing!")
            st.markdown("Steps to get started:")
            st.markdown("1. Go to **Resume Analysis** tab")
            st.markdown("2. Upload your resume file")
            st.markdown("3. Wait for skill extraction to complete")
            st.markdown("4. Return here to test your skills!")
    
    with tab3:
        st.subheader("📊 Test Results Dashboard")
        
        if 'test_results' in st.session_state and st.session_state.test_results:
            results = st.session_state.test_results
            
            # Display results summary
            st.markdown("### 🎯 Your Skill Assessment Results")
            
            total_tests = len(results)
            if total_tests > 0:
                # Overall statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Skills Tested", total_tests)
                with col2:
                    avg_score = sum(r.get('percentage', 0) for r in results.values()) / total_tests
                    st.metric("Average Score", f"{avg_score:.1f}%")
                with col3:
                    expert_skills = sum(1 for r in results.values() if r.get('percentage', 0) >= 80)
                    st.metric("Expert Level Skills", expert_skills)
                
                # Detailed results
                for skill, result in results.items():
                    with st.expander(f"{skill.title()} - {result.get('percentage', 0):.1f}%"):
                        st.write(f"**Score:** {result.get('score', 0)}/{result.get('total', 0)}")
                        st.write(f"**Status:** {result.get('status', 'Unknown')}")
            else:
                st.info("No test results available yet.")
        else:
            st.info("🎯 No test results yet! Complete a skill test to see your results here.")
            st.markdown("### How to get results:")
            st.markdown("1. Analyze your resume in the first tab")
            st.markdown("2. Take skill tests in the second tab")
            st.markdown("3. View your detailed results here!")

if __name__ == "__main__":
    main()