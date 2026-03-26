import streamlit as st
from groq import Groq

st.set_page_config(page_title="Health Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    .page-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 3s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px #00d4ff); }
        to { filter: drop-shadow(0 0 30px #7b2ff7); }
    }
    .chat-user {
        background: linear-gradient(135deg, rgba(123, 47, 247, 0.3), rgba(0, 212, 255, 0.1));
        border: 1px solid rgba(123, 47, 247, 0.4);
        border-radius: 15px 15px 0 15px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        color: white;
        animation: slideLeft 0.3s ease-out;
    }
    .chat-assistant {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px 15px 15px 0;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        color: rgba(255,255,255,0.9);
        animation: slideRight 0.3s ease-out;
    }
    @keyframes slideLeft {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideRight {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .chat-label-user {
        color: #7b2ff7;
        font-family: 'Orbitron', monospace;
        font-size: 0.7rem;
        letter-spacing: 2px;
        margin-bottom: 0.3rem;
    }
    .chat-label-ai {
        color: #00d4ff;
        font-family: 'Orbitron', monospace;
        font-size: 0.7rem;
        letter-spacing: 2px;
        margin-bottom: 0.3rem;
    }
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 26, 0.95) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.2) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>

<div class="page-title">🤖 AI HEALTH CHATBOT</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">
    Describe your symptoms for intelligent health guidance
</p>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-user">
            <div class="chat-label-user">▶ YOU</div>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-assistant">
            <div class="chat-label-ai">⚕ AI HEALTH COMPANION</div>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

user_input = st.chat_input("Describe your symptoms...")

if user_input:
    st.markdown(f"""
    <div class="chat-user">
        <div class="chat-label-user">▶ YOU</div>
        {user_input}
    </div>
    """, unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("AI analyzing..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            system_prompt = """You are a Smart Health Companion AI assistant.
            Your job is to:
            - Listen to the user's symptoms
            - Suggest possible conditions (always remind them to see a doctor)
            - Give general health advice
            - Answer health-related questions clearly and compassionately
            Always end with: 'Please consult a qualified doctor for proper diagnosis.'
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat_history,
                temperature=0.7,
                max_tokens=500
            )
            reply = response.choices[0].message.content
            st.markdown(f"""
            <div class="chat-assistant">
                <div class="chat-label-ai">⚕ AI HEALTH COMPANION</div>
                {reply}
            </div>
            """, unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"Error: {e}")
