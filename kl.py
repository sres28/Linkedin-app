import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- Configure Gemini ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash-lite")

st.title("💼 Optimize Your LinkedIn Profile (Smart Mode)")

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload your LinkedIn profile PDF", type=["pdf"])

if uploaded_file is not None:
    # Extract PDF text
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    st.success("✅ Profile uploaded successfully!")

    # --- User preferences ---
    st.subheader("🎯 Select sections you want AI help with:")
    col1, col2 = st.columns(2)

    with col1:
        headline_help = st.checkbox("💼 Headline")
        about_help = st.checkbox("📝 About / Summary")
        experience_help = st.checkbox("💼 Experience")

    with col2:
        education_help = st.checkbox("🎓 Education")
        skills_help = st.checkbox("🧠 Skills & Certifications")

    # --- AI Optimization Button ---
    if st.button("🤖 Get AI Optimization Help"):
        # Build a smart dynamic prompt
        selected_sections = []
        if headline_help:
            selected_sections.append("Headline")
        if about_help:
            selected_sections.append("About/Summary")
        if experience_help:
            selected_sections.append("Experience")
        if education_help:
            selected_sections.append("Education")
        if skills_help:
            selected_sections.append("Skills & Certifications")

        if not selected_sections:
            st.warning("⚠️ Please select at least one section for AI help.")
        else:
            with st.spinner("Analyzing your profile..."):
                prompt = f"""
                You are an expert LinkedIn career coach.
                Analyze and optimize only the following sections: {', '.join(selected_sections)}.

                Provide specific, concise suggestions to make them recruiter-friendly:
                - Rewrite or improve the text
                - Add keywords and action verbs
                - Suggest better phrasing or layout

                Profile Text:
                {text}
                """

                response = model.generate_content(prompt)

            st.subheader("✨ AI Optimization Suggestions")
            st.write(response.text)
