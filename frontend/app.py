#!/bin/env python3

import requests
import streamlit as st

# Backend Kubernetes Service URL
BACKEND_URL = "http://backend-app-backend-chart.rag.svc.cluster.local:8000"

st.set_page_config(
    page_title="ChatPDF",
    layout="wide"
)

# -----------------------------------
# Session State
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []


# -----------------------------------
# Display Chat Messages
# -----------------------------------
def display_messages():

    st.subheader("Chat")

    for msg, is_user in st.session_state["messages"]:

        if is_user:

            with st.chat_message("user"):
                st.write(msg)

        else:

            with st.chat_message("assistant"):
                st.write(msg)


# -----------------------------------
# Upload PDF
# -----------------------------------
def handle_pdf_upload(uploaded_files):

    for file in uploaded_files:

        # Avoid duplicate uploads
        if file.name in st.session_state["uploaded_files"]:
            continue

        with st.spinner(f"Uploading {file.name}..."):

            try:

                files = {
                    "file": (
                        file.name,
                        file,
                        "application/pdf"
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/upload-pdf",
                    files=files,
                    timeout=300
                )

                if response.status_code == 200:

                    st.session_state["uploaded_files"].append(file.name)

                    st.session_state["messages"].append(
                        (
                            f"✅ Uploaded {file.name}",
                            False
                        )
                    )

                else:

                    st.session_state["messages"].append(
                        (
                            f"❌ Upload Failed: {response.text}",
                            False
                        )
                    )

            except Exception as e:

                st.session_state["messages"].append(
                    (
                        f"❌ Error: {str(e)}",
                        False
                    )
                )


# -----------------------------------
# Ask Question
# -----------------------------------
def process_input():

    user_input = st.session_state.get("user_input", "").strip()

    if user_input:

        st.session_state["messages"].append(
            (
                user_input,
                True
            )
        )

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "question": user_input
                    },
                    timeout=300
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = (
                        data.get("response")
                        or data.get("answer")
                        or str(data)
                    )

                    st.session_state["messages"].append(
                        (
                            answer,
                            False
                        )
                    )

                else:

                    st.session_state["messages"].append(
                        (
                            f"❌ Error: {response.text}",
                            False
                        )
                    )

            except Exception as e:

                st.session_state["messages"].append(
                    (
                        f"❌ Error: {str(e)}",
                        False
                    )
                )

        st.session_state["user_input"] = ""


# -----------------------------------
# Main Page
# -----------------------------------
def page():

    st.title("📄 ChatPDF")

    st.subheader("Upload PDF Document")

    uploaded_files = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        accept_multiple_files=True,
    )

    # Upload files directly
    if uploaded_files:
        handle_pdf_upload(uploaded_files)

    # Display Chat
    display_messages()

    # Question Input
    st.text_input(
        "Ask a question about the PDF",
        key="user_input",
        on_change=process_input,
    )


# -----------------------------------
# Run App
# -----------------------------------
if __name__ == "__main__":
    page()
