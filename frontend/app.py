import streamlit as st
import requests

# Backend Kubernetes Service URL
BACKEND_URL = "http://backend-app-backend-chart.rag.svc.cluster.local:8000"

st.set_page_config(
    page_title="RAG PDF Chat",
    page_icon="📄",
    layout="centered"
)

st.title("📄 RAG PDF Chat Application")

st.markdown("Upload a PDF and ask questions from the document.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# Upload Button
if uploaded_file is not None:

    with st.spinner("Uploading PDF..."):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        try:
            response = requests.post(
                f"{BACKEND_URL}/upload-pdf",
                files=files
            )

            if response.status_code == 200:
                st.success("PDF uploaded successfully!")
            else:
                st.error(f"Upload failed: {response.text}")

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

# Ask Question
question = st.text_input("Ask a question from the PDF")

if st.button("Ask AI"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:

        with st.spinner("Generating answer..."):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "query": question
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    st.subheader("Answer")

                    st.write(data["response"])

                else:
                    st.error(f"Error: {response.text}")

            except Exception as e:
                st.error(f"Error: {e}")
