
import fitz
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import openai
import streamlit as st

model = SentenceTransformer("all-MiniLM-L6-v2")

def detect_language_and_translate(text):
    prompt = f"Detect the language of this text and translate it to English:\n\n{text}"
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'], 'en'

def translate_back_to_original(answer_en, original_lang):
    if original_lang == 'en':
        return answer_en
    prompt = f"Translate the following answer to {original_lang}:\n\n{answer_en}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

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
    question_en, lang = detect_language_and_translate(question)
    q_embedding = model.encode([question_en])
    D, I = index.search(np.array(q_embedding), k=3)
    context = "\n".join([chunks[i] for i in I[0]])
    prompt = f"Answer based on hotel standards:\n{context}\n\nQ: {question_en}\nA:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    answer_en = response['choices'][0]['message']['content']
    return translate_back_to_original(answer_en, lang)
