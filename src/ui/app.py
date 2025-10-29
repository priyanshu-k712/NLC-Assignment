import sys, os
import streamlit as st
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sidebar import render_sidebar
from src.core.llm_chain import generate_content, generate_content_from_data
from src.core.content_loader import (
    load_content_from_url,
    load_content_from_file,
    load_ppt,
    safe_load_json_from_string
)
from src.core.ppt_generator import generate_pptx


def safe_remove(filepath):
    if isinstance(filepath, str) and os.path.exists(filepath):
        os.remove(filepath)


def main_app():
    st.set_page_config(
        page_title="LLM Content Creator",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'generated_content' not in st.session_state:
        st.session_state['generated_content'] = ""

    st.title("LLM-Powered Educational Content Creator")
    st.markdown(
        "Configure your lesson details in the sidebar. The LLM will use its internal knowledge to generate content."
    )

    inputs = render_sidebar()

    prompt_vars = {
        'year': inputs['year'],
        'subject': inputs['subject'],
        'department': inputs['department'],
        'topic': inputs['topic'],
        'format': inputs['output_format']
    }

    st.header("Generated Study Material")

    if st.button("Generate Content", type="primary"):
        with st.spinner(f"Creating {inputs['output_format']} for '{inputs['topic']}'..."):

            if inputs['external_content'] is None:
                # Case 1: Topic only
                if inputs['output_format'] == 'PPT Outline Code(Structured JSON Code)':
                    try:
                        prompt_vars['content'] = (
                            "your expert internal knowledge and the topic name only. "
                            "Since the requested format is **PPT Outline Code(Structured JSON Code)**, "
                            "the output MUST be a JSON array of slides, each having 'title' and 'bullets' (a list of strings) keys."
                        )
                        content = generate_content(prompt_vars)
                        slides_data = safe_load_json_from_string(content)
                        path = generate_pptx(slides_data)

                        try:
                            st.download_button(
                                label="Download PowerPoint File",
                                data=load_ppt(path),
                                file_name=f"{inputs['topic']}.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )
                            st.session_state['generated_content'] = "Your PPT has been generated!"
                        except Exception as e:
                            st.error(str(e) + "\nTry Generating again if you get a JSON Error.")
                        finally:
                            safe_remove(path)

                        st.success("Content generation complete!")
                    except Exception as e:
                        st.error(f"An unexpected error occurred during Generating PPT with Topic: {e}")
                        st.session_state['generated_content'] = f"Invocation Error: {e}"

                else:
                    try:
                        prompt_vars['content'] = "your expert internal knowledge and the topic name only."
                        content = generate_content(prompt_vars)
                        st.session_state['generated_content'] = content
                        st.success("Content generation complete!")
                    except Exception as e:
                        st.error(f"An unexpected error occurred during Generating Content with Topic: {e}")
                        st.session_state['generated_content'] = f"Invocation Error: {e}"

            else:

                if inputs['source_mode']=="All":
                    if inputs['output_format'] == 'PPT Outline Code(Structured JSON Code)':
                        try:
                            data_list = load_content_from_url(inputs['external_content'])
                            data_string1 = "\n".join(data_list)

                            data_bytes = load_content_from_file(inputs['external_content2'])
                            try:
                                data_string2 = data_bytes.decode('utf-8', errors='replace')
                            except UnicodeDecodeError:
                                data_string2 = data_bytes.decode('latin-1', errors='replace')


                            prompt_vars['content'] = (
                                f"Use the following text to generate the content: {data_string1 + "\n"+data_string2}\n\n"
                                "Since the requested format is **PPT Outline Code(Structured JSON Code)**, "
                                "the output MUST be a JSON array of slides, each having 'title' and 'bullets' (a list of strings) keys."
                            )
                            prompt_vars['format'] = inputs['output_format']
                            code = generate_content_from_data(prompt_vars)
                            slides_data = safe_load_json_from_string(code)
                            path = generate_pptx(slides_data)

                            try:
                                st.download_button(
                                    label="Download PowerPoint File",
                                    data=load_ppt(path),
                                    file_name=f"{inputs['topic']}.pptx",
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                )
                                st.session_state['generated_content'] = "Your PPT has been generated!"
                            except Exception as e:
                                st.error(str(e) + "\nTry Generating again if you get a JSON Error.")
                            finally:
                                safe_remove(path)
                                safe_remove(inputs['external_content2'])

                            st.success("Content generation complete!")
                        except Exception as e:
                            st.error(f"An unexpected error occurred during Generating PPT With URL: {e}")
                            st.session_state['generated_content'] = f"Invocation Error: {e}"
                    else:
                        data_list = load_content_from_url(inputs['external_content'])
                        data_string1 = "\n".join(data_list)
                        try:
                            data_bytes = load_content_from_file(inputs['external_content2'])
                            try:
                                data_string = data_bytes.decode('utf-8', errors='replace')
                            except UnicodeDecodeError:
                                data_string = data_bytes.decode('latin-1', errors='replace')

                            prompt_vars['content'] = data_string1 + "\n" + data_string
                            content = generate_content_from_data(prompt_vars)
                            st.session_state['generated_content'] = content
                            st.success("Content generation complete!")
                        except Exception as e:
                            st.error(f"An unexpected error occurred during Generating Content with File Upload: {e}")
                            st.session_state['generated_content'] = f"Invocation Error: {e}"
                        finally:
                            safe_remove(inputs['external_content2'])



                # Case 2: External content provided
                elif inputs['source_mode'] == "Use URL":
                    # From URL
                    if inputs['output_format'] == 'PPT Outline Code(Structured JSON Code)':
                        try:
                            data_list = load_content_from_url(inputs['external_content'])
                            data_string = "\n".join(data_list)
                            prompt_vars['content'] = (
                                f"Use the following text to generate the content: {data_string}\n\n"
                                "Since the requested format is **PPT Outline Code(Structured JSON Code)**, "
                                "the output MUST be a JSON array of slides, each having 'title' and 'bullets' (a list of strings) keys."
                            )
                            prompt_vars['format'] = inputs['output_format']
                            code = generate_content_from_data(prompt_vars)
                            slides_data = safe_load_json_from_string(code)
                            path = generate_pptx(slides_data)

                            try:
                                st.download_button(
                                    label="Download PowerPoint File",
                                    data=load_ppt(path),
                                    file_name=f"{inputs['topic']}.pptx",
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                )
                                st.session_state['generated_content'] = "Your PPT has been generated!"
                            except Exception as e:
                                st.error(str(e) + "\nTry Generating again if you get a JSON Error.")
                            finally:
                                safe_remove(path)

                            st.success("Content generation complete!")
                        except Exception as e:
                            st.error(f"An unexpected error occurred during Generating PPT With URL: {e}")
                            st.session_state['generated_content'] = f"Invocation Error: {e}"

                    else:
                        try:
                            data_list = load_content_from_url(inputs['external_content'])
                            data_string = "\n".join(data_list)
                            prompt_vars['content'] = data_string
                            content = generate_content_from_data(prompt_vars)
                            st.session_state['generated_content'] = content
                            st.success("Content generation complete!")
                        except Exception as e:
                            st.error(f"An unexpected error occurred during Generating Content with Topic: {e}")
                            st.session_state['generated_content'] = f"Invocation Error: {e}"

                else:
                    # From uploaded file
                    if inputs['output_format'] == 'PPT Outline Code(Structured JSON Code)':
                        try:
                            data_bytes = load_content_from_file(inputs['external_content'])
                            try:
                                data_string = data_bytes.decode('utf-8', errors='replace')
                            except UnicodeDecodeError:
                                data_string = data_bytes.decode('latin-1', errors='replace')

                            prompt_vars['content'] = (
                                f"Use the following text to generate the content: {data_string}\n\n"
                                "Since the requested format is **PPT Outline Code(Structured JSON Code)**, "
                                "the output MUST be a JSON array of slides, each having 'title' and 'bullets' (a list of strings) keys."
                            )
                            prompt_vars['format'] = inputs['output_format']
                            code = generate_content_from_data(prompt_vars)
                            slides_data = safe_load_json_from_string(code)
                            path = generate_pptx(slides_data)

                            try:
                                st.download_button(
                                    label="Download PowerPoint File",
                                    data=load_ppt(path),
                                    file_name=f"{inputs['topic']}.pptx",
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                )
                                st.session_state['generated_content'] = "Your PPT has been generated!"
                            except Exception as e:
                                st.error(str(e) + "\nTry Generating again if you get a JSON Error.")
                            finally:
                                safe_remove(inputs['external_content'])
                                safe_remove(path)

                            st.success("Content generation complete!")
                        except Exception as e:
                            st.error(f"An unexpected error occurred during Generating PPT with File Upload: {e}")
                            st.session_state['generated_content'] = f"Invocation Error: {e}"

                    else:
                        try:
                            data_bytes = load_content_from_file(inputs['external_content'])
                            try:
                                data_string = data_bytes.decode('utf-8', errors='replace')
                            except UnicodeDecodeError:
                                data_string = data_bytes.decode('latin-1', errors='replace')

                            prompt_vars['content'] = data_string
                            content = generate_content_from_data(prompt_vars)
                            st.session_state['generated_content'] = content
                            st.success("Content generation complete!")
                        except Exception as e:
                            st.error(f"An unexpected error occurred during Generating Content with File Upload: {e}")
                            st.session_state['generated_content'] = f"Invocation Error: {e}"

    if st.session_state['generated_content']:
        st.markdown(st.session_state['generated_content'])
    else:
        st.warning("Click 'Generate Content' to see the study material.")


if __name__ == "__main__":
    main_app()
