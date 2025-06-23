
import fitz
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import openai
from googletrans import Translator
import streamlit as st

model = SentenceTransformer("all-MiniLM-L6-v2")
translator = Translator()

def detect_language(text):
    return translator.detect(text).lang

def translate(text, src='auto', dest='en'):
    return translator.translate(text, src=src, dest=dest).text

def process_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    return chunks

def create_vector_store(chunks):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(384)
    index.add(np.array(embeddings))
    return index, chunks

def query_llm(question, index, chunks):
    lang = detect_language(question)
    question_en = translate(question, src=lang, dest='en')
    q_embedding = model.encode([question_en])
    D, I = index.search(np.array(q_embedding), k=3)
    context = "\n".join([chunks[i] for i in I[0]])
    prompt = f"Answer based on hotel standards:\n{context}\n\nQ: {question_en}\nA:"
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    answer_en = response['choices'][0]['message']['content']
    return translate(answer_en, src='en', dest=lang)
