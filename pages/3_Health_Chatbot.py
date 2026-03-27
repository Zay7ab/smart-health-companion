import streamlit as st
from groq import Groq
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="AI Health Chatbot", page_icon="🤖", layout="wide")
load_sidebar()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e0ece0 !important; }

.chat-header { background: linear-gradient(135deg, #1a3a1a 0%, #2d5a1a 50%, #3b6d11 100%); border-radius: 20px; padding: 1.5rem 2rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.chat-header-left { display: flex; align-items: center; gap: 16px; }
.chat-avatar { width: 56px; height: 56px; border-radius: 16px; background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; }
.chat-title { font-size: 18px; font-weight: 700; color: white; margin-bottom: 2px; }
.chat-subtitle { font-size: 12px; color: rgba(255,255,255,0.7); }
.status-badge { display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; padding: 6px 14px; font-size: 12px; color: #97c459; font-weight: 600; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #97c459; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }

.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1.25rem; }
.stat-card { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 0.875rem 1rem; position: relative; overflow: hidden; text-align: center; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg,#639922,#97c459); }
.stat-label { font-size: 10px; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 18px; font-weight: 700; color: #1a3a1a; }
.stat-sub { font-size: 10px; color: #639922; margin-top: 2px; font-weight: 500; }

.chat-layout { display: grid; grid-template-columns: 1fr 280px; gap: 1rem; }
.chat-main { display: flex; flex-direction: column; gap: 1rem; }
.chat-sidebar-panel { display: flex; flex-direction: column; gap: 1rem; }

.chat-window { background: white; border: 1px solid #e0ece0; border-radius: 16px; overflow: hidden; }
.chat-window-header { padding: 1rem 1.25rem; border-bottom: 1px solid #e0ece0; background: #f8faf8; display: flex; align-items: center; justify-content: space-between; }
.chat-window-title { font-size: 13px; font-weight: 600; color: #1a3a1a; }
.chat-messages { padding: 1.25rem; min-height: 350px; max-height: 450px; overflow-y: auto; }

.msg-user-wrap { display: flex; justify-content: flex-end; margin-bottom: 12px; }
.msg-user { background: linear-gradient(135deg,#2d5a1a,#639922); border-radius: 16px 16px 4px 16px; padding: 10px 14px; max-width: 75%; }
.msg-user-label { font-size: 10px; color: rgba(255,255,255,0.7); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; text-align: right; }
.msg-user-text { font-size: 13px; color: white; line-height: 1.6; }

.msg-ai-wrap { display: flex; gap: 10px; margin-bottom: 12px; align-items: flex-start; }
.msg-ai-avatar { width: 32px; height: 32px; border-radius: 10px; background: linear-gradient(135deg,#eaf3de,#d4edbe); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.msg-ai { background: #f8faf8; border: 1px solid #e0ece0; border-radius: 4px 16px 16px 16px; padding: 10px 14px; max-width: 80%; }
.msg-ai-label { font-size: 10px; color: #639922; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.msg-ai-text { font-size: 13px; color: #1a3a1a; line-height: 1.7; }

.msg-typing { display: flex; gap: 4px; align-items: center; padding: 8px 0; }
.typing-dot { width: 8px; height: 8px; border-radius: 50%; background: #97c459; animation: typing 1.4s infinite; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing { 0%,60%,100%{transform:translateY(0);} 30%{transform:translateY(-8px);} }

.quick-replies { background: white; border: 1px solid #e0ece0; border-radius: 14px; padding: 1rem; }
.quick-replies-title { font-size: 11px; font-weight: 600; color: #639922; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
.quick-btn { width: 100%; background: #f5f9f0; border: 1px solid #d4edbe; border-radius: 8px; padding: 8px 12px; font-size: 12px; color: #1a3a1a; text-align: left; cursor: pointer; margin-bottom: 6px; transition: all 0.15s; display: flex; align-items: center; gap: 8px; }
.quick-btn:hover { background: #eaf3de; border-color: #97c459; }

.chat-features { background: white; border: 1px solid #e0ece0; border-radius: 14px; padding: 1rem; }
.chat-features-title { font-size: 11px; font-weight: 600; color: #639922; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
.feature-item { display: flex; align-items: center; gap: 8px; padding: 6px 0; border-bottom: 1px solid #f0f4f0; }
.feature-item:last-child { border-bottom: none; }
.feature-dot { width: 6px; height: 6px; border-radius: 50%; background: #639922; flex-shrink: 0; }
.feature-text { font-size: 12px; color: #5a6b5a; }

.chat-topics { background: white; border: 1px solid #e0ece0; border-radius: 14px; padding: 1rem; }
.topic-tag { display: inline-block; background: #eaf3de; color: #3b6d11; border: 1px solid #d4edbe; border-radius: 20px; padding: 4px 10px; font-size: 11px; font-weight: 500; margin: 3px; cursor: pointer; transition: all 0.15s; }
.topic-tag:hover { background: #d4edbe; border-color: #97c459; }

.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; }
div[data-testid="stButton"] button:hover { background: linear-gradient(135deg,#27500a,#3b6d11) !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-header">
    <div class="chat-header-left">
        <div class="chat-avatar">🤖</div>
        <div>
            <div class="chat-title">HealthAI Assistant</div>
            <div class="chat-subtitle">Powered by LLaMA 3.3 70B · Groq API · Medical AI</div>
        </div>
    </div>
    <div class="status-badge">
        <div class="status-dot"></div>
        Online · Ready to help
    </div>
</div>
""", unsafe_allow_html=True)

# Stats
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0
if "topics_covered" not in st.session_state:
    st.session_state.topics_covered = set()

msg_count = len(st.session_state.chat_history)
user_msgs = len([m for m in st.session_state.chat_history if m["role"] == "user"])

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
        <div class="stat-label">Response</div>
        <div class="stat-value">~2s</div>
        <div class="stat-sub">Average speed</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Languages</div>
        <div class="stat-value">50+</div>
        <div class="stat-sub">Supported</div>
    </div>
</div>
""", unsafe_allow_html=True)

def get_ai_response(user_input, language="English"):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    system_prompt = f"""You are HealthAI Assistant — a professional, compassionate and highly knowledgeable medical AI assistant.
    You respond in {language} language.
    
    Your capabilities:
    - Analyze symptoms and suggest possible conditions
    - Provide evidence-based health information
    - Give medication information and interactions
    - Offer mental health support and guidance  
    - Explain medical procedures and tests
    - Provide nutrition and lifestyle advice
    - Answer questions about diseases and conditions
    - Guide on when to seek emergency care
    
    Guidelines:
    - Be professional yet warm and empathetic
    - Use clear, simple language (avoid jargon)
    - Always recommend professional medical consultation
    - Be thorough but concise (4-6 sentences)
    - If emergency symptoms, prioritize calling emergency services
    - Never diagnose definitively — always say "possible" or "may suggest"
    
    Always end with: 'Please consult a qualified doctor for proper diagnosis and treatment.'"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat_history,
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

# Main layout
col_main, col_side = st.columns([2, 1])

with col_side:
    # Quick replies
    st.markdown("""
    <div class="quick-replies">
        <div class="quick-replies-title">💬 Quick Questions</div>
    </div>
    """, unsafe_allow_html=True)

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
                try:
                    reply = get_ai_response(question)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.session_state.total_messages += 1
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    # Language selector
    st.markdown("**🌐 Response Language:**")
    language = st.selectbox("Language", [
        "English", "Arabic", "Urdu", "Hindi", "French",
        "Spanish", "German", "Turkish", "Persian", "Malay"
    ], label_visibility="collapsed")

    st.markdown("---")

    # Features
    st.markdown("""
    <div class="chat-features">
        <div class="chat-features-title">✨ AI Capabilities</div>
        <div class="feature-item"><div class="feature-dot"></div><div class="feature-text">Symptom analysis</div></div>
        <div class="feature-item"><div class="feature-dot"></div><div class="feature-text">Drug information</div></div>
        <div class="feature-item"><div class="feature-dot"></div><div class="feature-text">Mental health support</div></div>
        <div class="feature-item"><div class="feature-dot"></div><div class="feature-text">Nutrition advice</div></div>
        <div class="feature-item"><div class="feature-dot"></div><div class="feature-text">Emergency guidance</div></div>
        <div class="feature-item"><div class="feature-dot"></div><div class="feature-text">50+ languages</div></div>
        <div class="feature-item"><div class="feature-dot"></div><div class="feature-text">Medical Q&A</div></div>
        <div class="feature-item"><div class="feature-dot"></div><div class="feature-text">Lab result explanations</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Topics
    st.markdown("""
    <div class="chat-topics">
        <div class="chat-features-title">🏷️ Popular Topics</div>
        <div>
            <span class="topic-tag">Heart Health</span>
            <span class="topic-tag">Diabetes</span>
            <span class="topic-tag">Blood Pressure</span>
            <span class="topic-tag">Cancer</span>
            <span class="topic-tag">Mental Health</span>
            <span class="topic-tag">Nutrition</span>
            <span class="topic-tag">Sleep</span>
            <span class="topic-tag">Pregnancy</span>
            <span class="topic-tag">Children Health</span>
            <span class="topic-tag">Skin Care</span>
            <span class="topic-tag">Allergies</span>
            <span class="topic-tag">COVID-19</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_main:
    # Chat window
    st.markdown('<div class="chat-window">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-window-header">
        <div class="chat-window-title">💬 Conversation</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">🤖</div>
            <div style="font-size:16px;font-weight:600;color:#1a3a1a;margin-bottom:8px;">Hello! I'm HealthAI Assistant</div>
            <div style="font-size:13px;color:#7a8f7a;line-height:1.7;max-width:400px;margin:0 auto;">
                I'm here to help with your health questions. Ask me about symptoms, medications, 
                nutrition, mental health, or any medical concerns you have.
                <br/><br/>
                <span style="color:#639922;font-weight:600;">👈 Use quick questions on the right or type below!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
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

    st.markdown('</div></div>', unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Ask me anything about your health...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("HealthAI is thinking..."):
            try:
                reply = get_ai_response(user_input, language)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.session_state.total_messages += 1
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # Action buttons
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
            st.session_state.total_messages = 0
            st.rerun()

st.markdown('<div class="disclaimer">⚠️ HealthAI provides general health information only. Always consult a qualified doctor for medical advice, diagnosis or treatment. In emergencies call 999/911/112 immediately.</div>', unsafe_allow_html=True)
