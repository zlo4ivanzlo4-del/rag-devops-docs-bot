import streamlit as st
import requests

st.set_page_config(page_title="DevOps/Python Docs Assistant")
st.title("Ассистент по документации")

API_URL = "http://api:8000/ask"  # для Docker
# Для локального запуска замените на "http://localhost:8000/ask"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Задайте вопрос по Docker, FastAPI или scikit-learn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            resp = requests.post(API_URL, json={"question": prompt, "top_k": 6})
            resp.raise_for_status()
            data = resp.json()
            answer = data["answer"]
            sources = data["sources"]
            hits = data["hits"]
            
            st.markdown(answer)
            with st.expander("Источники"):
                for src in sources:
                    st.write(f"- {src}")
                for h in hits:
                    st.write(f"**{h['source']}** (score: {h['score']:.3f})")
                    st.code(h['text'][:500] + "...")
            
            # Добавляем сообщение только при успехе
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Ошибка: {e}")
            # Не добавляем сообщение при ошибке, чтобы не ломать чат