Here is the updated Streamlit code with the **Quick Questions** sidebar section and the **Symptom Selector** grid removed, while keeping all other logic, styles, and formatting exactly as you provided.

```python
import streamlit as st
import requests
import datetime
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="AI Health Chatbot", page_icon="🤖", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background: #f0f4f0 !important; }
.chat-topbar { background: white; border-radius: 16px; padding: 1rem 1.5rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 12px; border: 1px solid #e0ece0; }
.chat-topbar-avatar { width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg,#2d5a1a,#639922); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; flex-shrink: 0; }
.chat-topbar-name { font-size: 16px; font-weight: 700; color: #1a3a1a; }
.chat-topbar-status { font-size: 11px; color: #639922; display: flex; align-items: center; gap: 4px; margin-top: 2px; }
.online-dot { width: 6px; height: 6px; border-radius: 50%; background: #639922; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.topbar-badge { background: #eaf3de; color: #27500a; font-size: 10px; font-weight: 600; padding: 4px 10px; border-radius: 20px; border: 1px solid #d4edbe; margin-left: auto; }
.msg-ai { display: flex; align-items: flex-end; gap: 8px; margin-bottom: 14px; }
.msg-ai-ava { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg,#2d5a1a,#639922); display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; }
.msg-ai-bubble { background: white; border: 1px solid #e8f0e8; border-radius: 4px 16px 16px 16px; padding: 10px 14px; max-width: 75%; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.msg-ai-text { font-size: 13px; color: #1a3a1a; line-height: 1.7; }
.msg-time { font-size: 10px; color: #aab8aa; margin-top: 4px; }
.msg-user { display: flex; justify-content: flex-end; align-items: flex-end; gap: 8px; margin-bottom: 14px; }
.msg-user-ava { width: 32px; height: 32px; border-radius: 50%; background: #d4edbe; display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; }
.msg-user-bubble { background: linear-gradient(135deg,#2d5a1a,#4a8520); border-radius: 16px 4px 16px 16px; padding: 10px 14px; max-width: 75%; }
.msg-user-text { font-size: 13px; color: white; line-height: 1.6; }
.msg-time-user { font-size: 10px; color: rgba(255,255,255,0.55); margin-top: 4px; text-align: right; }
.date-badge { text-align: center; margin-bottom: 12px; }
.date-badge span { background: #f0f4f0; color: #7a8f7a; font-size: 11px; padding: 3px 12px; border-radius: 20px; }
.chat-box-header { background: #f8faf8; border: 1px solid #e0ece0; border-bottom: none; border-radius: 16px 16px 0 0; padding: 0.75rem 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.chat-box-title { font-size: 13px; font-weight: 600; color: #1a3a1a; }
.chat-box-badge { font-size: 10px; color: #639922; background: #eaf3de; padding: 2px 8px; border-radius: 20px; }
.symptom-card-wrap { background: white; border: 1.5px solid #e0ece0; border-radius: 12px; padding: 0.75rem 0.5rem; text-align: center; }
.symptom-icon { font-size: 1.5rem; }
.symptom-name { font-size: 11px; font-weight: 600; color: #1a3a1a; margin-top: 4px; }
.section-label { font-size: 11px; font-weight: 600; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; margin-top: 1rem; }
.cap-item { display: flex; align-items: center; gap: 8px; padding: 5px 0; border-bottom: 1px solid #f5f7f5; font-size: 12px; color: #3a4a3a; }
.cap-item:last-child { border-bottom: none; }
.cap-dot { width: 6px; height: 6px; border-radius: 50%; background: #639922; flex-shrink: 0; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: white !important; color: #27500a !important; border: 1.5px solid #d4edbe !important; border-radius: 20px !important; font-weight: 500 !important; font-size: 12px !important; padding: 0.4rem 1rem !important; }
div[data-testid="stButton"] button:hover { background: #eaf3de !important; border-color: #97c459 !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

now = datetime.datetime.now().strftime("%I:%M %p")

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
            return "Sorry, I encountered an error. Please try again."
        return result["reply"]
    except:
        return "Connection error. Please try again."

# Topbar
st.markdown(f"""
<div class="chat-topbar">
    <div class="chat-topbar-avatar">🤖</div>
    <div>
        <div class="chat-topbar-name">HealthAI Assistant</div>
        <div class="chat-topbar-status"><span class="online-dot"></span> Your Health Assistant · Online</div>
    </div>
    <div class="topbar-badge">FastAPI + LLaMA 3.3</div>
</div>
""", unsafe_allow_html=True)

col_main, col_side = st.columns([3, 1])

with col_side:
    st.markdown('<div class="section-label">✨ Capabilities</div>', unsafe_allow_html=True)
    for cap in ["Symptom analysis", "Drug information", "Mental health", "Nutrition advice", "Emergency guidance", "Lab results", "50+ languages"]:
        st.markdown(f'<div class="cap-item"><div class="cap-dot"></div>{cap}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">🏷️ Topics</div>', unsafe_allow_html=True)
    topics_html = ""
    for t in ["Heart Health", "Diabetes", "Blood Pressure", "Mental Health", "Nutrition", "Sleep", "Pregnancy", "Allergies"]:
        topics_html += f'<span style="display:inline-block;background:#f0f4f0;border:1px solid #d4edbe;color:#3b6d11;border-radius:20px;padding:3px 9px;font-size:11px;margin:2px;">{t}</span>'
    st.markdown(f'<div style="line-height:2.2;">{topics_html}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">🌐 Language</div>', unsafe_allow_html=True)
    language = st.selectbox("", ["English","Arabic","Urdu","Hindi","French","Spanish","German","Turkish","Persian","Malay"], label_visibility="collapsed")

with col_main:
    st.markdown("""
    <div class="chat-box-header">
        <span class="chat-box-title">💬 Conversation</span>
        <span class="chat-box-badge">FastAPI Powered</span>
    </div>
    """, unsafe_allow_html=True)

    chat_area = st.container(height=450, border=True)

    with chat_area:
        st.markdown('<div class="date-badge"><span>Today</span></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="msg-ai">
            <div class="msg-ai-ava">🤖</div>
            <div class="msg-ai-bubble">
                <div class="msg-ai-text">Hi! I am <b>HealthAI Assistant</b>. I am here to help with health questions, symptom analysis, medication information and wellness advice.<br/><br/>How can I help you today?</div>
                <div class="msg-time">{now}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="msg-user">
                    <div class="msg-user-bubble">
                        <div class="msg-user-text">{message["content"]}</div>
                        <div class="msg-time-user">{now}</div>
                    </div>
                    <div class="msg-user-ava">👤</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-ai">
                    <div class="msg-ai-ava">🤖</div>
                    <div class="msg-ai-bubble">
                        <div class="msg-ai-text">{message["content"]}</div>
                        <div class="msg-time">{now}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Auto scroll anchor
        st.markdown('<div id="chat-end"></div>', unsafe_allow_html=True)

    # Auto scroll JavaScript
    st.markdown("""
    <script>
        function autoScroll() {
            var iframes = window.parent.document.querySelectorAll('iframe');
            iframes.forEach(function(iframe) {
                try {
                    var scrollable = iframe.contentDocument.querySelectorAll('[data-testid="stVerticalBlockBorderWrapper"]');
                    scrollable.forEach(function(el) {
                        el.scrollTop = el.scrollHeight;
                    });
                } catch(e) {}
            });
            var blocks = window.parent.document.querySelectorAll('[data-testid="stVerticalBlockBorderWrapper"]');
            blocks.forEach(function(el) {
                el.scrollTop = el.scrollHeight;
            });
        }
        setTimeout(autoScroll, 200);
        setTimeout(autoScroll, 600);
        setTimeout(autoScroll, 1200);
    </script>
    """, unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Type your health question here...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("HealthAI is thinking..."):
            reply = get_ai_response(user_input, st.session_state.chat_history[:-1], language)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    if st.session_state.chat_history:
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
        with b2:
            chat_text = "\n\n".join([f"{'You' if m['role']=='user' else 'HealthAI'}: {m['content']}" for m in st.session_state.chat_history])
            st.download_button("💾 Save Chat", data=chat_text, file_name="health_chat.txt", mime="text/plain")
        with b3:
            if st.button("🔄 New Session"):
                st.session_state.chat_history = []
                st.rerun()

st.markdown('<div class="disclaimer">⚠️ HealthAI provides general health information only. Always consult a qualified doctor. In emergencies call 999/911/112 immediately.</div>', unsafe_allow_html=True)
```
