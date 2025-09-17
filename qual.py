
import streamlit as st

st.set_page_config(page_title="Smart Job Portal", page_icon="💼", layout="wide")

# ---------------------- Session Init ----------------------
if "role" not in st.session_state:
    st.session_state.role = None
if "qualified_students" not in st.session_state:
    st.session_state.qualified_students = []  # list to hold notifications

# ---------------------- Home ----------------------
if st.session_state.role is None:
    st.title("💼 Smart Job Portal")
    st.subheader("Connecting Students & Companies through AI-powered Matching")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 Login as Student"):
            st.session_state.role = "student"

    with col2:
        if st.button("🏢 Login as Company"):
            st.session_state.role = "company"

# ---------------------- Student Section ----------------------
elif st.session_state.role == "student":
    st.header("🎓 Student Login")
    with st.form("student_form"):
        student_id = st.text_input("Student ID (e.g., Roll No.)")
        student_password = st.text_input("Password", type="password")
        submit_student = st.form_submit_button("Login")

    if submit_student:
        if student_id == "STU1001" and student_password == "stu@1234":
            st.success(f"✅ Welcome {student_id}!")

            with st.form("student_details"):
                student_name = st.text_input("Full Name")
                student_email = st.text_input("Email")
                student_phone = st.text_input("Phone")
                student_college = st.text_input("College")
                student_degree = st.text_input("Degree")

                resume_score = st.slider("📄 Resume Score", 0, 100, 75)
                test_score = st.slider("📝 Skill Test Score", 0, 100, 80)

                save_details = st.form_submit_button("Submit & Analyze")

            if save_details:
                if resume_score > 60 and test_score > 70:
                    st.success("🚀 You qualified for company notifications!")

                    st.session_state.qualified_students.append({
                        "id": student_id,
                        "name": student_name,
                        "email": student_email,
                        "phone": student_phone,
                        "college": student_college,
                        "degree": student_degree,
                        "resume_score": resume_score,
                        "test_score": test_score
                    })
                else:
                    st.warning("⚠️ Scores are below threshold, not notified to companies.")
        else:
            st.error("❌ Invalid Student ID or Password")

    if st.button("⬅️ Back"):
        st.session_state.role = None

# ---------------------- Company Section ----------------------
elif st.session_state.role == "company":
    st.header("🏢 Company Login")
    with st.form("company_form"):
        company_id = st.text_input("Company ID")
        company_password = st.text_input("Password", type="password")
        submit_company = st.form_submit_button("Login")

    if submit_company:
        if company_id == "COMP001" and company_password == "comp@123":
            st.success(f"✅ Welcome {company_id}!")

            st.subheader("📢 Qualified Student Notifications")

            if len(st.session_state.qualified_students) > 0:
                for student in st.session_state.qualified_students:
                    st.markdown("---")
                    st.markdown(f"**👤 Name:** {student['name']}")
                    st.markdown(f"**📧 Email:** {student['email']}")
                    st.markdown(f"**📱 Phone:** {student['phone']}")
                    st.markdown(f"**🎓 College:** {student['college']}")
                    st.markdown(f"**📘 Degree:** {student['degree']}")
                    st.markdown(f"**📄 Resume Score:** {student['resume_score']}")
                    st.markdown(f"**📝 Test Score:** {student['test_score']}")
            else:
                st.info("No qualified students yet.")
        else:
            st.error("❌ Invalid Company ID or Password")

    if st.button("⬅️ Back"):
        st.session_state.role = None
