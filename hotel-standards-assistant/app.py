
import streamlit as st
from utils import process_pdf, create_vector_store, query_llm
import os

st.set_page_config(page_title="Hotel Standards Assistant", layout="wide")
st.title("📘 Hotel Standards Assistant")

PDF_PATH = "hotel-standards-assistant/data/lcbsa2025.pdf"

if "index" not in st.session_state:
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            chunks = process_pdf(f)
            index, chunk_texts = create_vector_store(chunks)
            st.session_state.index = index
            st.session_state.chunks = chunk_texts
            st.success("Standards loaded and ready.")
    else:
        st.warning("Please upload a standards PDF to begin.")

uploaded_file = st.file_uploader("Upload a new hotel standards PDF", type="pdf")
if uploaded_file:
    if st.button("Update Standards"):
        with open(PDF_PATH, "wb") as f:
            f.write(uploaded_file.read())
        with open(PDF_PATH, "rb") as f:
            chunks = process_pdf(f)
            index, chunk_texts = create_vector_store(chunks)
            st.session_state.index = index
            st.session_state.chunks = chunk_texts
            st.success("New standards uploaded and processed.")

if "index" in st.session_state:
    question = st.text_input("Ask a question (EN / GR / ES):")
    if question:
        with st.spinner("Thinking..."):
            answer = query_llm(question, st.session_state.index, st.session_state.chunks)
        st.markdown(f"**Answer:** {answer}")
