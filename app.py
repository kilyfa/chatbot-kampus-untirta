# chatbot_navigasi_kampus/app.py

import streamlit as st
import requests
import json

# Ambil API Key dari secrets.toml (Streamlit Cloud)
API_KEY = st.secrets["API_KEY"]

def query_openrouter(prompt: str, model="deepseek/deepseek-r1-0528-qwen3-8b:free"):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Kamu adalah asisten kampus UNTIRTA. Jawab pertanyaan seputar lokasi dan navigasi kampus berdasarkan denah."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# UI Streamlit
st.set_page_config(page_title="Chatbot Navigasi UNTIRTA", page_icon="🌐")
st.title("🌐 Chatbot Navigasi UNTIRTA")
st.markdown("Tanyakan arah antar gedung atau informasi navigasi berdasarkan denah kampus.")

# Baca file denah kampus
try:
    with open("denah.txt", "r", encoding="utf-8") as f:
        denah_kampus = f.read()
except FileNotFoundError:
    st.error("❌ File denah.txt tidak ditemukan.")
    st.stop()

# Input pertanyaan pengguna
query = st.text_input("Masukkan pertanyaanmu:")
if query:
    with st.spinner("🔍 Tunggu sebentar yaaa..."):
        full_prompt = f"{denah_kampus}\n\nPertanyaan: {query}\nJawaban yang sopan dan ringkas:"
        jawaban = query_openrouter(full_prompt)
        st.markdown("### ✨ Jawaban:")
        st.success(jawaban)
