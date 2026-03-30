import streamlit as st
import requests
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="AI Health Chatbot", page_icon="🤖", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
.chat-header { background: linear-gradient(135deg, #1a3a1a 0%, #2d5a1a 50%, #3b6d11 100%); border-radius: 20px; padding: 1.5rem 2rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.chat-avatar { width: 56px; height: 56px; border-radius: 16px; background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; }
.chat-title { font-size: 18px; font-weight: 700; color: white; margin-bottom: 2px; }
.chat-subtitle { font-size: 12px; color: rgba(255,255,255,0.7); }
.status-badge { display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; padding: 6px 14px; font-size: 12px; color: #97c459; font-weight: 600; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #97c459; animation: pulse 2s infinite; display: inline-block; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }
.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1.25rem; }
.stat-card { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 0.875rem 1rem; position: relative; overflow: hidden; text-align: center; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg,#639922,#97c459); }
.stat-label { font-size: 10px; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 18px; font-weight: 700; color: #1a3a1a; }
.stat-sub { font-size: 10px; color: #639922; margin-top: 2px; font-weight: 500; }
.msg-user-wrap { display: flex; justify-content: flex-end; margin-bottom: 12px; }
.msg-user { background: linear-gradient(135deg,#2d5a1a,#639922); border-radius: 16px 16px 4px 16px; padding: 10px 14px; max-width: 75%; }
.msg-user-label { font-size: 10px; color: rgba(255,255,255,0.7); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; text-align: right; }
.msg-user-text { font-size: 13px; color: white; line-height: 1.6; }
.msg-ai-wrap { display: flex; gap: 10px; margin-bottom: 12px; align-items: flex-start; }
.msg-ai-avatar { width: 32px; height: 32px; border-radius: 10px; background: linear-gradient(135deg,#eaf3de,#d4edbe); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.msg-ai { background: #f8faf8; border: 1px solid #e0ece0; border-radius: 4px 16px 16px 16px; padding: 10px 14px; max-width: 80%; }
.msg-ai-label { font-size: 10px; color: #639922; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.msg-ai-text { font-size: 13px; color: #1a3a1a; line-height: 1.7; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chat-header">
    <div style="display:flex;align-items:center;gap:16px;">
        <div class="chat-avatar">🤖</div>
        <div>
            <div class="chat-title">HealthAI Assistant</div>
            <div class="chat-subtitle">Powered by FastAPI + LLaMA 3.3 70B via Groq</div>
        </div>
    </div>
    <div class="status-badge">
        <span class="status-dot"></span>
        Online · Ready
    </div>
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

msg_count = len(st.session_state.chat_history)

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-label">Messages</div>
        <div class="stat-value">{msg_count}</div>
        <div class="stat-sub">This session</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">AI Model</div>
        <div class="stat-value">70B</div>
        <div class="stat-sub">LLaMA 3.3</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Backend</div>
        <div class="stat-value">FastAPI</div>
        <div class="stat-sub">HuggingFace</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Languages</div>
        <div class="stat-value">50+</div>
        <div class="stat-sub">Supported</div>
    </div>
</div>
""", unsafe_allow_html=True)

def get_ai_response(user_input, history, language="English"):
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "message": user_input,
                "history": history,
                "language": language,
                "api_key": st.secrets.get("GROQ_API_KEY", "")
            },
            timeout=30
        )
        result = response.json()
        if "error" in result:
            return f"Error: {result['error']}"
        return result["reply"]
    except Exception as e:
        return f"Error: {e}"

col_main, col_side = st.columns([2, 1])

with col_side:
    st.markdown("### 💬 Quick Questions")
    quick_questions = [
        ("🫀", "Signs of a heart attack?"),
        ("🩸", "How to control blood sugar?"),
        ("🧠", "Stress and anxiety relief tips"),
        ("💊", "Common drug interactions"),
        ("🤒", "I have fever and body aches"),
        ("😴", "Tips for better sleep"),
        ("🏃", "Exercise for beginners"),
        ("🥗", "Best anti-inflammatory foods"),
    ]
    for icon, question in quick_questions:
        if st.button(f"{icon} {question}", key=f"q_{question}"):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner(""):
                reply = get_ai_response(question, st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    st.markdown("---")
    st.markdown("**🌐 Language:**")
    language = st.selectbox("Language", [
        "English", "Arabic", "Urdu", "Hindi", "French",
        "Spanish", "German", "Turkish", "Persian", "Malay"
    ], label_visibility="collapsed")

with col_main:
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="background:white;border:1px solid #e0ece0;border-radius:16px;padding:3rem;text-align:center;">
            <div style="font-size:3rem;margin-bottom:1rem;">🤖</div>
            <div style="font-size:16px;font-weight:600;color:#1a3a1a;margin-bottom:8px;">HealthAI Assistant Ready</div>
            <div style="font-size:13px;color:#7a8f7a;line-height:1.7;">
                Ask me about symptoms, medications, nutrition or any health concern.
                <br/><span style="color:#639922;font-weight:600;">Use quick questions or type below!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:white;border:1px solid #e0ece0;border-radius:16px;padding:1.5rem;">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="msg-user-wrap">
                    <div class="msg-user">
                        <div class="msg-user-label">You</div>
                        <div class="msg-user-text">{message["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-ai-wrap">
                    <div class="msg-ai-avatar">🤖</div>
                    <div class="msg-ai">
                        <div class="msg-ai-label">HealthAI Assistant</div>
                        <div class="msg-ai-text">{message["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask me anything about your health...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("🤖 HealthAI thinking..."):
            reply = get_ai_response(user_input, st.session_state.chat_history[:-1], language)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
    with col2:
        if st.session_state.chat_history:
            chat_text = "\n\n".join([f"{'You' if m['role']=='user' else 'HealthAI'}: {m['content']}" for m in st.session_state.chat_history])
            st.download_button("💾 Save Chat", data=chat_text, file_name="health_chat.txt", mime="text/plain")
    with col3:
        if st.button("🔄 New Session"):
            st.session_state.chat_history = []
            st.rerun()

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
