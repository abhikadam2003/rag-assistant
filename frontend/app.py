#!/bin/env python3

import os
import sys
import time
import tempfile
import streamlit as st

# Add rag_backend folder to Python path
sys.path.append(os.path.abspath("../rag_backend"))

from rag import ChatPDF

st.set_page_config(page_title="ChatPDF", layout="wide")


def display_messages():
    st.subheader("Chat")

    for msg, is_user in st.session_state["messages"]:

        if is_user:
            with st.chat_message("user"):
                st.write(msg)

        else:
            with st.chat_message("assistant"):
                st.write(msg)

    st.session_state["thinking_spinner"] = st.empty()


def process_input():

    user_input = st.session_state.get("user_input", "").strip()

    if user_input:

        with st.session_state["thinking_spinner"], st.spinner("Thinking..."):

            agent_text = st.session_state["assistant"].ask(user_input)

        st.session_state["messages"].append((user_input, True))
        st.session_state["messages"].append((agent_text, False))

        st.session_state["user_input"] = ""


def read_and_save_file():

    st.session_state["assistant"].clear()
    st.session_state["messages"] = []

    for file in st.session_state["file_uploader"]:

        with tempfile.NamedTemporaryFile(delete=False) as tf:

            tf.write(file.getbuffer())
            file_path = tf.name

        with st.spinner(f"Ingesting {file.name}..."):

            t0 = time.time()

            st.session_state["assistant"].ingest(file_path)

            t1 = time.time()

        st.session_state["messages"].append(
            (
                f"✅ Ingested {file.name} in {t1 - t0:.2f} seconds",
                False,
            )
        )

        os.remove(file_path)


def page():

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "assistant" not in st.session_state:
        st.session_state["assistant"] = ChatPDF()

    st.title("📄 ChatPDF")

    st.subheader("Upload PDF Document")

    st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        accept_multiple_files=True,
    )

    display_messages()

    st.text_input(
        "Ask a question about the PDF",
        key="user_input",
        on_change=process_input,
    )


if __name__ == "__main__":
    page()