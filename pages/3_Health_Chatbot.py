import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Health Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e0ece0 !important; }
[data-testid="stSidebar"] * { color: #1a3a1a !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] { background: linear-gradient(135deg,#eaf3de,#d4edbe) !important; color: #27500a !important; font-weight: 600 !important; }
.topbar { background: white; border: 1px solid #e0ece0; border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.topbar-title { font-size: 20px; font-weight: 700; color: #1a3a1a; }
.topbar-sub { font-size: 12px; color: #639922; margin-top: 2px; }
.ai-badge { display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(135deg,#eaf3de,#d4edbe); border: 1px solid #97c459; border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #27500a; font-weight: 600; }
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #639922; display: inline-block; }
.chat-container { background: white; border: 1px solid #e0ece0; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; }
.chat-user { background: linear-gradient(135deg,#eaf3de,#d4edbe); border-radius: 16px 16px 4px 16px; padding: 0.875rem 1.125rem; margin: 0.5rem 0; max-width: 75%; margin-left: auto; }
.chat-user-label { font-size: 10px; color: #3b6d11; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; text-align: right; }
.chat-user-text { font-size: 13px; color: #1a3a1a; line-height: 1.6; text-align: right; }
.chat-ai { background: #f8faf8; border: 1px solid #e0ece0; border-radius: 16px 16px 16px 4px; padding: 0.875rem 1.125rem; margin: 0.5rem 0; max-width: 75%; }
.chat-ai-label { font-size: 10px; color: #639922; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.chat-ai-text { font-size: 13px; color: #1a3a1a; line-height: 1.7; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; }
div[data-testid="stButton"] button:hover { background: linear-gradient(135deg,#27500a,#3b6d11) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 AI Health Chatbot</div>
        <div class="topbar-sub">Powered by LLaMA 3.3 70B via Groq</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> LLaMA 3.3 Active</div>
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_ai_response(user_input):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    system_prompt = """You are a Smart Health Companion AI assistant — professional,
    compassionate and knowledgeable. Your job is to:
    - Listen carefully to the user's symptoms and health concerns
    - Provide clear, accurate health information and insights
    - Suggest possible conditions based on symptoms (with appropriate caveats)
    - Give actionable lifestyle and wellness recommendations
    - Be empathetic and supportive in your tone
    Always end responses with: 'Please consult a qualified doctor for proper diagnosis.'
    Keep responses concise — 3-5 sentences maximum unless more detail is needed."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat_history,
        temperature=0.7,
        max_tokens=400
    )
    return response.choices[0].message.content

# Show suggestions only when chat is empty
if not st.session_state.chat_history:
    st.markdown("### 💡 Quick questions — click to ask:")
    col1, col2 = st.columns(2)
    suggestions = [
        "💊 What are symptoms of diabetes?",
        "❤️ How to improve heart health?",
        "🤒 I have fever and headache, what could it be?",
        "🏃 Best exercises for weight loss?"
    ]
    with col1:
        if st.button(suggestions[0], key="s1"):
            st.session_state.chat_history.append({"role": "user", "content": suggestions[0]})
            reply = get_ai_response(suggestions[0])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
        if st.button(suggestions[2], key="s3"):
            st.session_state.chat_history.append({"role": "user", "content": suggestions[2]})
            reply = get_ai_response(suggestions[2])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
    with col2:
        if st.button(suggestions[1], key="s2"):
            st.session_state.chat_history.append({"role": "user", "content": suggestions[1]})
            reply = get_ai_response(suggestions[1])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
        if st.button(suggestions[3], key="s4"):
            st.session_state.chat_history.append({"role": "user", "content": suggestions[3]})
            reply = get_ai_response(suggestions[3])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

# Chat history display
if st.session_state.chat_history:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-user">
                <div class="chat-user-label">You</div>
                <div class="chat-user-text">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-ai">
                <div class="chat-ai-label">🤖 AI Health Assistant</div>
                <div class="chat-ai-text">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Describe your symptoms or ask a health question...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("🤖 AI is thinking..."):
        try:
            reply = get_ai_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# Clear button
if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
