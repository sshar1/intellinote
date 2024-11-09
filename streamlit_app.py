import os
import shutil
import streamlit as st
from functools import partial
from openai import OpenAI

# Initialize session state if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'home'  # Default page

def switch_page(new_page: str):
    st.session_state.page = new_page  # Update the session state
    st.switch_page(new_page)  # This will switch the page based on the session state

if st.session_state.page == 'home':
    with st.sidebar:
        anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")

    # Show title and description.
    st.title("📄 Your Intellinotes")
    st.write(
        "Upload a document below and Intellinote will create a personalized study quiz from it! "
        "To use this app, you need to provide an OpenAI API key in the sidebar "
    )

    # Let the user upload a file via `st.file_uploader`.
    # TODO add option to extract txt from pdf
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Runs every time a new file is uploaded
    if uploaded_file:

        file_path = os.path.join('IntellinoteFiles', uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())  # Write the in-memory file to disk

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()

    for file_name in os.listdir('IntellinoteFiles'):
            file_button, delete_button = st.columns(2)
            with file_button:
                st.button(
                    label=file_name,
                    icon='📝',
                    on_click=partial(st.session_state.update, {'page': 'chat_page', 'intellinote' : file_name})  # Update session state
                )
            with delete_button:
                st.button(
                    label='❌',
                    key=file_name+'x',
                    on_click=partial(os.remove, os.path.join('IntellinoteFiles', file_name))
                )

# File Page (for displaying a specific file's content)
elif st.session_state.page == 'chat_page':
    st.title(str(st.session_state.intellinote) + " Chat Page")
    question = st.container(border = True)
    user_answer_display = st.container(border = True)
    explanation = st.container(border = True)
    user_answer_textbox = st.text_area('label', placeholder="Put your answer here!", label_visibility="hidden")

    question.write("This is where the question will be displayed")
    if user_answer_textbox:
        user_answer_display.write('YOUR ANSWER\n\n' + user_answer_textbox)
        explanation.write("EXPLANATION\n\nThis will be the explanation")

    # Back button to return to the main page
    if st.button("Back to Home"):
        st.session_state.page = 'home'  # Update session state to go back to home page
        # st.experimental_rerun()  # Trigger rerun to load the home page