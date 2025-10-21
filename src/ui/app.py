from sidebar import render_sidebar
from src.core.llm_chain import generate_content
import streamlit as st


def main_app():

    st.set_page_config(
        page_title="LLM Content Creator",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'generated_content' not in st.session_state:
        st.session_state['generated_content'] = ""

    st.title("LLM-Powered Educational Content Creator (Topic Only Test)")
    st.markdown(
        "Configure your lesson details in the sidebar. The LLM will use its internal knowledge to generate content.")

    inputs = render_sidebar()

    required_fields = ['topic', 'department', 'subject']
    is_ready = all(inputs.get(field) and inputs.get(field).strip() for field in required_fields)

    prompt_vars = {
        'year': inputs['year'],
        'subject': inputs['subject'],
        'department': inputs['department'],
        'topic': inputs['topic'],
        'format': inputs['output_format']
    }

    st.header("Generated Study Material")

    if st.button("Generate Content", type="primary", disabled=not is_ready):

        with st.spinner(f"Creating lesson plan for '{inputs['topic']}'..."):

            raw_source_text = None

            try:

                content = generate_content(prompt_vars, raw_source_text)

                st.session_state['generated_content'] = content
                st.success("Content generation complete!")
            except Exception as e:
                st.error(f"An unexpected error occurred during LLM invocation: {e}")
                st.session_state['generated_content'] = f"Invocation Error: {e}"

    if st.session_state['generated_content']:
        st.markdown(st.session_state['generated_content'])
    else:
        st.warning("Click 'Generate Content' to see the study material.")


if __name__ == "__main__":
    main_app()