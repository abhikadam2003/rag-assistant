#!/bin/env python3

import requests
import streamlit as st

# Backend API URL
BACKEND_URL = "http://backend-app-backend-chart.rag.svc.cluster.local:8000"

st.set_page_config(
    page_title="ChatPDF",
    layout="wide"
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "processing" not in st.session_state:
    st.session_state.processing = False


# Display chat
def display_messages():

    st.subheader("Chat")

    for msg, is_user in st.session_state.messages:

        with st.chat_message("user" if is_user else "assistant"):
            st.write(msg)


# Upload PDF
def upload_pdf(file):

    try:

        files = {
            "file": (
                file.name,
                file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            f"{BACKEND_URL}/upload-pdf",
            files=files,
            timeout=300
        )

        if response.status_code == 200:

            st.session_state.messages.append(
                (
                    f"✅ Uploaded {file.name}",
                    False
                )
            )

            st.success("PDF Uploaded Successfully")

            st.session_state.uploaded_file_name = file.name

        else:

            st.error(response.text)

    except Exception as e:

        st.error(str(e))


# Ask Question
def ask_question(question):

    try:

        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={
                "question": question
            },
            timeout=300
        )

        if response.status_code == 200:

            data = response.json()

            answer = (
                data.get("answer")
                or data.get("response")
                or str(data)
            )

            st.session_state.messages.append(
                (
                    answer,
                    False
                )
            )

        else:

            st.session_state.messages.append(
                (
                    f"❌ Error: {response.text}",
                    False
                )
            )

    except Exception as e:

        st.session_state.messages.append(
            (
                f"❌ Error: {str(e)}",
                False
            )
        )


# Main UI
def page():

    st.title("📄 ChatPDF")

    st.subheader("Upload PDF Document")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    # Upload only once per file
    if (
        uploaded_file
        and uploaded_file.name != st.session_state.uploaded_file_name
    ):

        upload_pdf(uploaded_file)

    display_messages()

    question = st.chat_input("Ask a question about the PDF")

    if question and not st.session_state.processing:

        st.session_state.processing = True

        st.session_state.messages.append(
            (
                question,
                True
            )
        )

        ask_question(question)

        st.session_state.processing = False

        st.rerun()


if __name__ == "__main__":
    page()
