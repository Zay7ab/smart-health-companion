import streamlit as st
import requests
import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="MediMate AI", page_icon="🟢", layout="wide")

# API Configuration
API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- 2. THE MAGIC CSS (For Mobile Look & Clean UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Overall Page Background */
    .stApp { background-color: #F4F7F6 !important; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Remove Top Spacing */
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    header { visibility: hidden; }

    /* Centered Chat Container */
    .main-app-container {
        max-width: 500px;
        margin: 20px auto;
        background: white;
        border-radius: 28px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.05);
        overflow: hidden;
    }

    /* Custom Header */
    .medimate-header {
        background: white;
        padding: 15px 20px;
        border-bottom: 1px solid #f0f0f0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .status-dot { width: 8px; height: 8px; background: #10B981; border-radius: 50%; display: inline-block; margin-right: 4px; }

    /* Message Bubbles */
    .ai-bubble {
        background: #F3F4F6;
        color: #1F2937;
        padding: 12px 16px;
        border-radius: 4px 18px 18px 18px;
        margin-bottom: 15px;
        font-size: 14px;
        max-width: 85%;
        line-height: 1.5;
    }
    .user-bubble {
        background: #10B981;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 4px 18px 18px;
        margin-bottom: 15px;
        font-size: 14px;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }

    /* Symptom Grid Styling */
    div[data-testid="stCheckbox"] {
        background: #ffffff;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 8px 12px;
        transition: 0.2s;
    }
    div[data-testid="stCheckbox"]:hover { border-color: #10B981; }

    /* Bottom Buttons */
    div[data-testid="stButton"] button {
        width: 100%;
        background: #10B981 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_response(prompt, history, lang):
    try:
        res = requests.post(f"{API_URL}/chat", json={
            "message": prompt, "history": history, "language": lang,
            "api_key": st.secrets.get("GROQ_API_KEY", "")
        }, timeout=30)
        return res.json().get("reply", "Something went wrong.")
    except:
        return "Connection error. Please try again."

# --- 4. LAYOUT: CENTERED COLUMN ---
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    # Header UI
    st.markdown("""
    <div class="medimate-header">
        <div style="font-size: 24px;">🩺</div>
        <div>
            <div style="font-weight: 700; color: #1F2937; font-size: 16px;">MediMate Chatbot</div>
            <div style="font-size: 11px; color: #10B981;"><span class="status-dot"></span>Online</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat Area
    with st.container():
        st.markdown('<div style="padding: 20px 0;">', unsafe_allow_html=True)
        # Welcome
        st.markdown('<div class="ai-bubble">Hi! I am MediMate. How can I help you today?</div>', unsafe_allow_html=True)
        
        for m in st.session_state.messages:
            role_class = "user-bubble" if m["role"] == "user" else "ai-bubble"
            st.markdown(f'<div class="{role_class}">{m["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Symptom Grid
    st.markdown("<p style='text-align:center; font-weight:700; font-size:13px; color:#374151; margin-top:20px;'>SELECT SYMPTOMS</p>", unsafe_allow_html=True)
    
    sym_list = [("🌡️", "Fever"), ("🤢", "Vomiting"), ("😮‍💨", "Breathless"), 
                ("😔", "Depression"), ("👄", "Mouth Sore"), ("🚽", "Diarrhea")]
    
    selected = []
    cols = st.columns(3)
    for i, (icon, name) in enumerate(sym_list):
        if cols[i%3].checkbox(f"{icon} {name}", key=name):
            selected.append(name)

    if st.button("ANALYZE SYMPTOMS →"):
        if selected:
            user_msg = f"I am feeling: {', '.join(selected)}"
            st.session_state.messages.append({"role": "user", "content": user_msg})
            with st.spinner("Analyzing..."):
                reply = get_response(user_msg, st.session_state.messages[:-1], "English")
                st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

    # Chat Input & Language
    lang = st.selectbox("🌐 Select Language", ["English", "Urdu", "Arabic", "Hindi"], label_visibility="collapsed")
    user_input = st.chat_input("Type your health question...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            reply = get_response(user_input, st.session_state.messages[:-1], lang)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    # Footer Buttons
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.rerun()
    with f_col2:
        if st.session_state.messages:
            st.download_button("💾 Save", data=str(st.session_state.messages), file_name="chat.txt")

    st.markdown("<p style='font-size:10px; color:#9CA3AF; text-align:center; margin-top:20px;'>⚠️ Consultation with a doctor is advised for medical emergencies.</p>", unsafe_allow_html=True)
