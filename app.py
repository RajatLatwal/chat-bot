import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# --------------------🔐 Load and Configure API --------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# --------------------🎨 App Title --------------------
st.markdown(
    "<h2 style='text-align: center;'>🤖 Gemini AI Chatbot 💬</h2>",
    unsafe_allow_html=True
)

# --------------------🧠 Memory Management --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------💬 Display Chat History --------------------
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# --------------------📨 Chat Input --------------------
user_input = st.chat_input("💡 Ask me anything...")
if user_input:
    # Show user's message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    # Format chat history for Gemini API
    gemini_history = [
        {"role": msg["role"], "parts": [{"text": msg["content"]}]}
        for msg in st.session_state.chat_history
    ]

    # Generate response from Gemini
    response = model.generate_content(gemini_history)
    bot_reply = response.text

    # Show assistant reply
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_reply
    })
