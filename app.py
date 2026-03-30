import streamlit as st
import requests
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="MediMate Chatbot", page_icon="🟢", layout="wide")

# API URL (Apne hisab se change kar sakte hain)
API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- 2. CUSTOM CSS (FULL DESIGN & FIXES) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Font aur Background */
* { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background-color: #F8F9FE !important; }

/* Top Blank Space Fix */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    max-width: 650px !important; /* Mobile width feel */
    margin: auto;
}

/* Header Design */
.chat-header {
    background: white;
    padding: 15px 20px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #F0F2F6;
    position: sticky;
    top: 0;
    z-index: 999;
}
.back-btn { color: #10B981; font-size: 20px; margin-right: 15px; cursor: pointer; }
.bot-icon {
    width: 40px; height: 40px;
    background: #F0FDF4;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin-right: 12px;
    font-size: 20px;
}
.header-titles p { margin: 0; line-height: 1.2; }
.sub-t { font-size: 11px; color: #6B7280; }
.main-t { font-size: 15px; font-weight: 700; color: #1F2937; }

/* Chat Bubbles */
.chat-area { padding: 20px 0; min-height: 300px; }
.ai-msg {
    background: #F3F4F6;
    color: #374151;
    padding: 12px 16px;
    border-radius: 4px 18px 18px 18px;
    max-width: 85%;
    font-size: 14px;
    margin-bottom: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}
.user-msg {
    background: #10B981;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 4px 18px 18px;
    max-width: 85%;
    font-size: 14px;
    margin-left: auto;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2);
}

/* Symptom Card Styling */
.symptom-label {
    text-align: center;
    font-weight: 700;
    font-size: 13px;
    color: #1F2937;
    margin-top: 20px;
}
div[data-testid="stCheckbox"] {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 15px;
    padding: 10px 15px;
    margin-bottom: 5px;
    transition: 0.3s;
}
div[data-testid="stCheckbox"]:hover { border-color: #10B981; }

/* Button Styling */
div[data-testid="stButton"] button {
    width: 100%;
    background: #10B981 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px !important;
    font-weight: 600 !important;
    margin-top: 10px;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC & SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_ai_response(user_input, history):
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "message": user_input,
                "history": history,
                "api_key": st.secrets.get("GROQ_API_KEY", "")
            },
            timeout=30
        )
        return response.json().get("reply", "Pardon me, I couldn't process that.")
    except:
        return "Connection error. Please check your API."

# --- 4. UI COMPONENTS ---

# Fixed Header
st.markdown("""
<div class="chat-header">
    <div class="back-btn">←</div>
    <div class="bot-icon">🩺</div>
    <div class="header-titles">
        <p class="sub-t">Your Health Assistant</p>
        <p class="main-t">MediMate Chatbot</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Display Area
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

# Static Welcome Message (Hamesha dikhega)
st.markdown('<div class="ai-msg">Hi! I am MediMate. How can I help you today?</div>', unsafe_allow_html=True)

# Loop through history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Symptom Selection (Grid style)
st.markdown('<p class="symptom-label">SELECT SYMPTOMS</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:11px; color:#6B7280; margin-bottom:15px;">Choose what you are feeling</p>', unsafe_allow_html=True)

symptoms_data = [
    ("🌡️", "Fever"), ("🤢", "Vomiting"), ("😮‍💨", "Breathless"),
    ("😔", "Depression"), ("👄", "Mouth Sore"), ("🚽", "Diarrhea")
]

selected_symptoms = []
sym_cols = st.columns(3)
for idx, (icon, name) in enumerate(symptoms_data):
    with sym_cols[idx % 3]:
        if st.checkbox(f"{icon} {name}", key=f"check_{name}"):
            selected_symptoms.append(name)

if st.button("NEXT →"):
    if selected_symptoms:
        symptom_text = f"I am experiencing: {', '.join(selected_symptoms)}"
        st.session_state.chat_history.append({"role": "user", "content": symptom_text})
        with st.spinner("Analyzing..."):
            ans = get_ai_response(symptom_text, st.session_state.chat_history[:-1])
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
        st.rerun()

# Chat Input Area (Bottom)
user_query = st.chat_input("Type message here...")
if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.spinner("Thinking..."):
        ans = get_ai_response(user_query, st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({"role": "assistant", "content": ans})
    st.rerun()

# Disclaimer
st.markdown("""
<div style="margin-top: 30px; padding: 15px; background: #FFFBEB; border: 1px solid #FEF3C7; border-radius: 12px; font-size: 10px; color: #92400E; text-align: center;">
    ⚠️ <b>Disclaimer:</b> MediMate is an AI for information purposes only. 
    In case of emergency, please visit the nearest hospital or call 1122.
</div>
""", unsafe_allow_html=True)
