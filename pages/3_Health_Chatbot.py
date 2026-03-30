import streamlit as st
import requests
import datetime

# --- CONFIG & SIDEBAR ---
st.set_page_config(page_title="MediMate Chatbot", page_icon="🟢", layout="wide")
# load_sidebar() # Isko uncomment kar dein agar file available hai

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- CUSTOM CSS (MEDIMATE DESIGN) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background-color: #F8F9FE !important; }

/* Main Container */
.chat-container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    border-radius: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    overflow: hidden;
}

/* Top Bar */
.chat-header {
    padding: 20px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #F0F2F6;
    background: white;
}
.back-arrow { font-size: 20px; color: #10B981; margin-right: 15px; cursor: pointer; }
.bot-avatar {
    width: 45px; height: 45px;
    background: #F0FDF4;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin-right: 12px;
}
.header-text { flex-grow: 1; }
.header-title { font-size: 16px; font-weight: 700; color: #1F2937; margin: 0; }
.header-subtitle { font-size: 12px; color: #6B7280; margin: 0; }

/* Message Bubbles */
.chat-box { padding: 20px; background: #FFFFFF; min-height: 400px; }

.ai-row { display: flex; margin-bottom: 20px; align-items: flex-start; }
.ai-bubble {
    background: #F3F4F6;
    color: #374151;
    padding: 12px 16px;
    border-radius: 4px 20px 20px 20px;
    max-width: 80%;
    font-size: 14px;
    line-height: 1.5;
}

.user-row { display: flex; justify-content: flex-end; margin-bottom: 20px; }
.user-bubble {
    background: #10B981;
    color: white;
    padding: 12px 16px;
    border-radius: 20px 4px 20px 20px;
    max-width: 80%;
    font-size: 14px;
}

.timestamp { font-size: 10px; color: #9CA3AF; margin-top: 5px; }

/* Symptom Selection Cards */
.symptom-section {
    background: white;
    padding: 20px;
    border-radius: 25px 25px 0 0;
    box-shadow: 0 -5px 20px rgba(0,0,0,0.03);
}
.symptom-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 15px;
}
/* Streamlit checkbox styling to look like cards */
div[data-testid="stCheckbox"] {
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 10px;
    transition: 0.3s;
}
div[data-testid="stCheckbox"]:has(input:checked) {
    border: 2px solid #10B981;
    background: #ECFDF5;
}

/* Buttons */
div[data-testid="stButton"] button {
    width: 100%;
    background-color: #10B981 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 10px !important;
    font-weight: 600 !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
        return response.json().get("reply", "Error in response")
    except:
        return "Connection error. Please try again."

# --- UI LAYOUT ---

# 1. Header
st.markdown("""
<div class="chat-header">
    <div class="back-arrow">←</div>
    <div class="bot-avatar">🩺</div>
    <div class="header-text">
        <p class="header-subtitle">Your Health Assistant</p>
        <p class="header-title">MediMate Chatbot</p>
    </div>
    <div style="color: #6B7280;">⋮</div>
</div>
""", unsafe_allow_html=True)

# 2. Chat Messages
current_time = datetime.datetime.now().strftime("%I:%M %p")

with st.container():
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    
    # Welcome Message
    st.markdown(f"""
    <div class="ai-row">
        <div class="ai-bubble">
            Hi! I am MediMate. How can I help you today?
            <div class="timestamp">{current_time}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-row"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-row"><div class="ai-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Symptom Selector (Image Style)
st.markdown('<div class="symptom-section">', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight:700; color:#1F2937;'>SELECT SYMPTOMS</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:12px; color:#6B7280;'>Please choose symptoms you've been experiencing.</p>", unsafe_allow_html=True)

symptoms = [
    ("🌡️", "Fever"), ("🤢", "Vomiting"), ("😮‍💨", "Breathless"),
    ("😔", "Depression"), ("👄", "Mouth Sore"), ("🚽", "Diarrhea")
]

selected = []
cols = st.columns(3)
for i, (icon, name) in enumerate(symptoms):
    with cols[i % 3]:
        if st.checkbox(f"{icon}\n{name}", key=f"sym_{name}"):
            selected.append(name)

if st.button("NEXT →"):
    if selected:
        user_msg = f"I am feeling: {', '.join(selected)}"
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        reply = get_ai_response(user_msg, st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# 4. Input Area
user_input = st.chat_input("Type message here...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    reply = get_ai_response(user_input, st.session_state.chat_history[:-1])
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("""
<div style="padding: 15px; font-size: 10px; color: #9CA3AF; text-align: center;">
    ⚠️ General info only. Consult a doctor for emergencies.
</div>
""", unsafe_allow_html=True)
