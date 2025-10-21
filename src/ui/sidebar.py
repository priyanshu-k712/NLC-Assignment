import streamlit as st
from typing import Dict, Any, Optional


def render_sidebar() -> Dict[str, Any]:

    with st.sidebar:
        st.header("📚 Lesson Plan Creator")
        st.markdown("Configure the context and input source below.")

        st.subheader("Faculty Details")

        inputs = {}
        inputs['year'] = st.selectbox("Year of Study",
                                      ["1st Year", "2nd Year", "3rd Year", "4th Year", "Post-Graduate"])
        inputs['department'] = st.text_input("Department Name", placeholder="e.g., Computer Science, History")
        inputs['subject'] = st.text_input("Subject Name", placeholder="e.g., Data Structures, Modern European History")

        st.divider()

        st.subheader("Content Request")
        inputs['topic'] = st.text_input("Topic Name", placeholder="e.g., Python Decorators, French Revolution Causes")

        inputs['output_format'] = st.selectbox(
            "Desired Output Format",
            ["Detailed long comprehensive study material (Raw Text)", "PPT Outline (Structured JSON)"]
        )

        st.divider()

        st.subheader("Source Material")

        source_mode = st.radio(
            "How will you provide the source material?",
            ["Topic Only (Use LLM Knowledge)", "Use URL", "Upload File"],
            index=0
        )

        inputs['source_mode'] = source_mode

        inputs['external_content'] = None

        if source_mode == "Use URL":
            url_input = st.text_input("Enter URL", placeholder="https://example.com/lesson-source")
            if url_input:
                st.info("URL input received. The core logic will fetch content from this URL.")
                inputs['external_content'] = url_input  # Pass URL string for the loader
            else:
                st.warning("Please provide a valid URL.")

        elif source_mode == "Upload File":
            uploaded_file = st.file_uploader("Upload PDF or Text File", type=['pdf', 'txt', 'md'])
            if uploaded_file is not None:

                inputs['external_content'] = uploaded_file.name
                st.success(f"File '{uploaded_file.name}' uploaded successfully.")



    return inputs
