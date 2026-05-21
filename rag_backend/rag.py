from langchain_core.globals import set_verbose, set_debug
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.prompts import ChatPromptTemplate


set_debug(True)
set_verbose(True)


class ChatPDF:

    vector_store = None
    retriever = None
    chain = None

    def __init__(self, llm_model: str = "qwen2.5:1.5b"):

        # Connect to Ollama running inside Kubernetes
        self.model = ChatOllama(
            model=llm_model,
            base_url="http://ollama-app-ollama-chart:11434"
        )

        # Split PDF into chunks
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=100
        )

        # Prompt Template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant that answers questions from uploaded PDF documents.",
                ),
                (
                    "human",
                    "Here is the document content:\n{context}\n\nQuestion: {question}",
                ),
            ]
        )

        self.vector_store = None
        self.retriever = None
        self.chain = None

    def ingest(self, pdf_file_path: str):

        # Load PDF
        docs = PyPDFLoader(
            file_path=pdf_file_path
        ).load()

        # Split text into chunks
        chunks = self.text_splitter.split_documents(docs)

        # Clean metadata
        chunks = filter_complex_metadata(chunks)

        # Store embeddings in ChromaDB
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=FastEmbedEmbeddings(),
            persist_directory="chroma_db",
        )

    def ask(self, query: str):

        # Load vector DB if not already loaded
        if not self.vector_store:

            self.vector_store = Chroma(
                persist_directory="chroma_db",
                embedding_function=FastEmbedEmbeddings(),
            )

        # Retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 10,
                "score_threshold": 0.0,
            },
        )

        # Create chain
        self.chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.model
            | StrOutputParser()
        )

        if not self.chain:
            return "Please upload a PDF document first."

        # Generate response
        return self.chain.invoke(query)

    def clear(self):

        self.vector_store = None
        self.retriever = None
        self.chain = None
