# chatbot_navigasi_kampus/app.py

import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = st.secrets["API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

def query_openrouter(prompt: str, model="deepseek/deepseek-r1-0528-qwen3-8b:free"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Kamu adalah asisten kampus yang membantu orang menavigasi gedung-gedung dan memahami lokasi kampus."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message["content"]

st.set_page_config(page_title="Chatbot Navigasi UNTIRTA", page_icon="🌐")
st.title("🌐 Chatbot Navigasi UNTIRTA")
st.markdown("Tanyakan arah antar gedung atau informasi navigasi berdasarkan denah kampus.")

with open("denah.txt", "r", encoding="utf-8") as f:
    denah_kampus = f.read()

query = st.text_input("Masukkan pertanyaanmu:")
if query:
    with st.spinner("🔍 Tunggu sebentar yaaa..."):
        full_prompt = f"{denah_kampus}\n\nPertanyaan: {query}\nJawaban yang sopan dan ringkas:" 
        jawaban = query_openrouter(full_prompt)
        st.markdown("### ✨ Jawaban:")
        st.success(jawaban)
