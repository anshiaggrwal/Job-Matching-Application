# company_sidebar_module.py
"""
Company Sidebar Module for Resume Analyzer
This module handles the display of connected companies in the sidebar
"""

import streamlit as st
import requests
import json
from typing import List, Dict

def load_companies_from_external_system():
    """
    Function to load company data from your external login system
    Replace this with actual integration to your login database
    """
    # Example integration options:
    # 
    # Option 1: API call to your login system
    # try:
    #     response = requests.get("https://your-login-api.com/companies")
    #     companies_data = response.json()
    #     # Expected format: [{"company_name": "Google Inc."}, {"company_name": "Microsoft"}]
    #     return companies_data
    # except:
    #     return []
    #
    # Option 2: Database connection
    # import sqlite3
    # try:
    #     conn = sqlite3.connect('your_login_database.db')
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT company_name FROM users WHERE user_type='company'")
    #     companies = [{"company_name": row[0]} for row in cursor.fetchall()]
    #     conn.close()
    #     return companies
    # except:
    #     return []
    #
    # Option 3: File-based integration
    # try:
    #     with open('companies_data.json', 'r') as f:
    #         companies = json.load(f)
    #     return companies
    # except:
    #     return []
    
    # For now, return empty list - will be populated by your external system
    return []

def get_connected_companies() -> List[Dict]:
    """Get list of all registered companies from external login system"""
    
    # Load from external system
    companies = load_companies_from_external_system()
    
    # If no external companies, try session state fallback
    if not companies and 'users_db' in st.session_state:
        for username, user_data in st.session_state.users_db.items():
            if user_data.get("user_type") == "company":
                companies.append({
                    "company_name": user_data.get("company_name", username)
                })
    
    return companies

def display_company_sidebar():
    """Display the connected companies sidebar"""
    st.markdown("### 🏢 Connected Companies")
    
    companies = get_connected_companies()
    
    if companies:
        st.markdown(f"**{len(companies)} companies** connected:")
        
        for company in companies:
            st.markdown(f"• {company['company_name']}")
        
        st.markdown("---")
        st.info("💡 Companies can connect with top performers!")
    else:
        st.info("No companies connected yet.")

def display_supported_roles(job_categories):
    """Display supported job roles"""
    st.markdown("### 📊 Supported Roles:")
    for job_title in job_categories.keys():
        st.markdown(f"• {job_title}")

def display_model_status():
    """Display AI model loading status and controls"""
    st.markdown("---")
    st.markdown("### 🔧 Model Status:")
    
    if st.button("Load AI Models"):
        with st.spinner("Loading Hugging Face models... This may take a moment."):
            try:
                # Import here to avoid circular imports
                from transformers import pipeline
                
                classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
                if classifier:
                    st.session_state.hf_model = classifier
                    st.session_state.models_loaded = True
                    st.success("✅ AI Model loaded successfully!")
                else:
                    st.error("❌ Failed to load AI models")
            except Exception as e:
                st.error(f"❌ Error loading models: {str(e)}")
    
    if st.session_state.get('models_loaded', False):
        st.success("🟢 AI Models Ready")
    else:
        st.warning("🟡 Click 'Load AI Models' to enable advanced features")

def create_complete_sidebar(job_categories):
    """Create the complete sidebar with companies, roles, and model status"""
    with st.sidebar:
        # Display connected companies
        display_company_sidebar()
        
        # Display supported roles
        display_supported_roles(job_categories)
        
        # Display model status
        display_model_status()

# Integration examples for different systems:

def example_api_integration():
    """Example of how to integrate with an API-based login system"""
    def load_companies_from_api():
        try:
            # Replace with your actual API endpoint
            response = requests.get(
                "https://your-domain.com/api/companies",
                headers={"Authorization": "Bearer YOUR_API_KEY"}
            )
            
            if response.status_code == 200:
                data = response.json()
                # Assuming API returns: {"companies": [{"name": "Company 1"}, ...]}
                companies = []
                for company in data.get("companies", []):
                    companies.append({
                        "company_name": company.get("name", "Unknown Company")
                    })
                return companies
            return []
        except Exception as e:
            st.error(f"Error connecting to API: {e}")
            return []
    
    return load_companies_from_api()

def example_database_integration():
    """Example of how to integrate with a database"""
    def load_companies_from_database():
        try:
            import sqlite3
            
            # Connect to your database
            conn = sqlite3.connect('path/to/your/login_database.db')
            cursor = conn.cursor()
            
            # Query for companies
            cursor.execute("""
                SELECT company_name 
                FROM users 
                WHERE user_type = 'company' 
                AND status = 'active'
            """)
            
            companies = []
            for row in cursor.fetchall():
                companies.append({
                    "company_name": row[0]
                })
            
            conn.close()
            return companies
            
        except Exception as e:
            st.error(f"Database error: {e}")
            return []
    
    return load_companies_from_database()

def example_file_integration():
    """Example of how to integrate with file-based systems"""
    def load_companies_from_file():
        try:
            # Read from a JSON file that your login system updates
            with open('data/companies.json', 'r') as f:
                data = json.load(f)
            
            companies = []
            for company in data.get("companies", []):
                companies.append({
                    "company_name": company.get("name", "Unknown Company")
                })
            
            return companies
            
        except FileNotFoundError:
            # File doesn't exist yet
            return []
        except Exception as e:
            st.error(f"File read error: {e}")
            return []
    
    return load_companies_from_file()

# Helper functions for testing and development
def add_test_company(company_name: str):
    """Add a test company (for development purposes)"""
    if 'test_companies' not in st.session_state:
        st.session_state.test_companies = []
    
    if company_name not in [c["company_name"] for c in st.session_state.test_companies]:
        st.session_state.test_companies.append({
            "company_name": company_name
        })

def get_test_companies():
    """Get test companies (for development purposes)"""
    return st.session_state.get('test_companies', [])

# Usage example in your main application:
# 
# In your main.py, replace the sidebar code with:
# 
# import company_sidebar_module as csm
# 
# # In the main function, replace the sidebar section with:
# csm.create_complete_sidebar(JOB_CATEGORIES)