import streamlit as st
import requests
import datetime
import sys
import json
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="AI Health Chatbot", page_icon="🤖", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background: #0a0f0a !important; }

.chat-topbar { background: #0d120d; border-radius: 16px; padding: 1rem 1.5rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 12px; border: 1px solid #1a2e1a; }
.chat-topbar-avatar { width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg,#166534,#4ade80); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; flex-shrink: 0; }
.chat-topbar-name { font-size: 16px; font-weight: 700; color: #ffffff; }
.chat-topbar-status { font-size: 11px; color: #4ade80; display: flex; align-items: center; gap: 4px; margin-top: 2px; }
.online-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.topbar-badge { background: rgba(74,222,128,0.1); color: #4ade80; font-size: 10px; font-weight: 600; padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(74,222,128,0.2); margin-left: auto; }

.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; margin-bottom: 1rem; }
.stat-box { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 0.75rem; text-align: center; position: relative; overflow: hidden; }
.stat-box::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background: linear-gradient(90deg,#4ade80,#22c55e); }
.stat-box-label { font-size: 9px; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.5px; }
.stat-box-value { font-size: 16px; font-weight: 700; color: #ffffff; margin: 3px 0; }
.stat-box-sub { font-size: 9px; color: #4ade80; font-weight: 500; }

.msg-ai { display: flex; align-items: flex-end; gap: 8px; margin-bottom: 14px; }
.msg-ai-ava { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg,#166534,#4ade80); display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; }
.msg-ai-bubble { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 4px 16px 16px 16px; padding: 10px 14px; max-width: 80%; }
.msg-ai-text { font-size: 13px; color: rgba(255,255,255,0.85); line-height: 1.7; }
.msg-time { font-size: 10px; color: rgba(255,255,255,0.25); margin-top: 4px; }

.msg-user { display: flex; justify-content: flex-end; align-items: flex-end; gap: 8px; margin-bottom: 14px; }
.msg-user-ava { width: 32px; height: 32px; border-radius: 50%; background: rgba(74,222,128,0.15); display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; }
.msg-user-bubble { background: linear-gradient(135deg,#166534,#15803d); border-radius: 16px 4px 16px 16px; padding: 10px 14px; max-width: 80%; }
.msg-user-text { font-size: 13px; color: white; line-height: 1.6; }
.msg-time-user { font-size: 10px; color: rgba(255,255,255,0.4); margin-top: 4px; text-align: right; }

.date-badge { text-align: center; margin-bottom: 12px; }
.date-badge span { background: #0f1a0f; color: rgba(255,255,255,0.3); font-size: 11px; padding: 3px 12px; border-radius: 20px; border: 1px solid #1a2e1a; }

.chat-box-header { background: #0d120d; border: 1px solid #1a2e1a; border-bottom: none; border-radius: 16px 16px 0 0; padding: 0.75rem 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.chat-box-title { font-size: 13px; font-weight: 600; color: #ffffff; }
.chat-box-badge { font-size: 10px; color: #4ade80; background: rgba(74,222,128,0.1); padding: 2px 8px; border-radius: 20px; border: 1px solid rgba(74,222,128,0.2); }

.symptom-card-wrap { background: #0d120d; border: 1.5px solid #1a2e1a; border-radius: 12px; padding: 0.75rem 0.5rem; text-align: center; transition: all 0.15s; }
.symptom-card-wrap:hover { border-color: #4ade80; background: #0f1a0f; }
.symptom-icon { font-size: 1.4rem; }
.symptom-name { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.7); margin-top: 4px; }

.section-label { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; margin-top: 1rem; }

.cap-item { display: flex; align-items: center; gap: 8px; padding: 5px 0; border-bottom: 1px solid #0f1a0f; font-size: 12px; color: rgba(255,255,255,0.6); }
.cap-item:last-child { border-bottom: none; }
.cap-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; flex-shrink: 0; }

.mood-card { background: #0d120d; border: 1.5px solid #1a2e1a; border-radius: 12px; padding: 0.75rem; text-align: center; cursor: pointer; transition: all 0.15s; }
.mood-card:hover { border-color: #4ade80; background: #0f1a0f; transform: translateY(-2px); }
.mood-icon { font-size: 1.6rem; margin-bottom: 4px; }
.mood-name { font-size: 10px; font-weight: 600; color: rgba(255,255,255,0.6); }

.history-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between; }
.history-preview { font-size: 12px; color: rgba(255,255,255,0.6); }
.history-time { font-size: 10px; color: rgba(255,255,255,0.3); }

.typing-indicator { display: flex; align-items: center; gap: 4px; padding: 8px 0; }
.typing-dot { width: 8px; height: 8px; border-radius: 50%; background: #4ade80; animation: typing 1.4s infinite; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing { 0%,60%,100%{transform:translateY(0);opacity:0.4} 30%{transform:translateY(-6px);opacity:1} }

.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 1rem; }

div[data-testid="stButton"] button { background: rgba(74,222,128,0.1) !important; color: #4ade80 !important; border: 1px solid rgba(74,222,128,0.2) !important; border-radius: 20px !important; font-weight: 500 !important; font-size: 12px !important; padding: 0.4rem 1rem !important; }
div[data-testid="stButton"] button:hover { background: rgba(74,222,128,0.2) !important; border-color: #4ade80 !important; }
label { color: rgba(255,255,255,0.7) !important; }
p { color: rgba(255,255,255,0.5) !important; }
.stSelectbox > div > div { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stTextArea > div > div > textarea { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
[data-testid="stTabs"] { background: transparent !important; }
[data-testid="stTab"] { color: rgba(255,255,255,0.5) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0
if "saved_sessions" not in st.session_state:
    st.session_state.saved_sessions = []
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "General Health"

now = datetime.datetime.now().strftime("%I:%M %p")
today = datetime.datetime.now().strftime("%B %d, %Y")

def get_ai_response(user_input, history, language="English", mode="General Health"):
    try:
        mode_prompts = {
            "General Health": "general health questions, symptoms, medications and wellness advice",
            "Mental Health": "mental health, stress, anxiety, depression and emotional wellbeing",
            "Nutrition": "nutrition, diet, food, calories and healthy eating habits",
            "Fitness": "exercise, fitness, workout routines and physical activity",
            "Emergency": "emergency first aid and urgent medical guidance"
        }
        mode_context = mode_prompts.get(mode, "general health")
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

def send_message(msg, language="English", mode="General Health"):
    st.session_state.chat_history.append({"role": "user", "content": msg, "time": now})
    with st.spinner(""):
        reply = get_ai_response(msg, st.session_state.chat_history[:-1], language, mode)
        st.session_state.chat_history.append({"role": "assistant", "content": reply, "time": now})
        st.session_state.total_messages += 1
    st.rerun()

# ─── Top Bar ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="chat-topbar">
    <div class="chat-topbar-avatar">🤖</div>
    <div>
        <div class="chat-topbar-name">HealthAI Assistant</div>
        <div class="chat-topbar-status"><span class="online-dot"></span> Your Health Assistant · Online · {today}</div>
    </div>
    <div class="topbar-badge">FastAPI + LLaMA 3.3 70B</div>
</div>
""", unsafe_allow_html=True)

# ─── Stats Row ────────────────────────────────────────────────────
msg_count = len(st.session_state.chat_history)
user_msgs = len([m for m in st.session_state.chat_history if m["role"] == "user"])
sessions_saved = len(st.session_state.saved_sessions)

st.markdown(f"""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-box-label">Messages</div>
        <div class="stat-box-value">{msg_count}</div>
        <div class="stat-box-sub">This session</div>
    </div>
    <div class="stat-box">
        <div class="stat-box-label">Mode</div>
        <div class="stat-box-value" style="font-size:11px;">{st.session_state.chat_mode}</div>
        <div class="stat-box-sub">Active</div>
    </div>
    <div class="stat-box">
        <div class="stat-box-label">Saved</div>
        <div class="stat-box-value">{sessions_saved}</div>
        <div class="stat-box-sub">Sessions</div>
    </div>
    <div class="stat-box">
        <div class="stat-box-label">Model</div>
        <div class="stat-box-value">70B</div>
        <div class="stat-box-sub">LLaMA 3.3</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Main Layout ──────────────────────────────────────────────────
col_main, col_side = st.columns([3, 1])

# ─── Sidebar Panel ────────────────────────────────────────────────
with col_side:

    # Chat Mode Selector
    st.markdown('<div class="section-label">🎯 Chat Mode</div>', unsafe_allow_html=True)
    mode = st.selectbox("", [
        "General Health", "Mental Health", "Nutrition", "Fitness", "Emergency"
    ], label_visibility="collapsed", key="mode_select")
    st.session_state.chat_mode = mode

    mode_colors = {
        "General Health": "#4ade80",
        "Mental Health": "#a78bfa",
        "Nutrition": "#fb923c",
        "Fitness": "#38bdf8",
        "Emergency": "#ef4444"
    }
    mc = mode_colors.get(mode, "#4ade80")
    st.markdown(f'<div style="background:rgba(255,255,255,0.03);border:1px solid {mc}30;border-radius:10px;padding:8px 12px;margin-bottom:8px;font-size:11px;color:{mc};">Active: {mode} Mode</div>', unsafe_allow_html=True)

    # Language
    st.markdown('<div class="section-label">🌐 Language</div>', unsafe_allow_html=True)
    language = st.selectbox("", [
        "English", "Arabic", "Urdu", "Hindi", "French",
        "Spanish", "German", "Turkish", "Persian", "Malay",
        "Bengali", "Swahili", "Portuguese"
    ], label_visibility="collapsed")

    # Quick Questions
    st.markdown('<div class="section-label">💬 Quick Questions</div>', unsafe_allow_html=True)
    quick_by_mode = {
        "General Health": [("🫀","Signs of heart attack?"),("🩸","Control blood sugar"),("🤒","Fever and body aches"),("💊","Drug interactions"),("😴","Better sleep tips"),("🏃","Exercise for beginners")],
        "Mental Health": [("😰","Signs of anxiety?"),("😔","Dealing with depression"),("🧘","Meditation tips"),("😤","Stress relief techniques"),("💤","Insomnia help"),("🤝","How to talk to therapist")],
        "Nutrition": [("🥗","Best anti-inflammatory foods"),("🍎","Foods for immunity"),("💧","How much water daily?"),("🫐","Superfoods list"),("🍖","Protein rich foods"),("🚫","Foods to avoid")],
        "Fitness": [("🏋️","Beginner workout plan"),("🧘","Best stretches"),("🔥","Burn belly fat"),("💪","Build muscle fast"),("🏃","Running tips"),("⚡","HIIT workout guide")],
        "Emergency": [("🚨","Heart attack first aid"),("🔥","Burn treatment"),("🩸","Stop bleeding"),("😵","Unconscious person"),("🐍","Snake bite steps"),("💊","Drug overdose help")]
    }
    current_qs = quick_by_mode.get(mode, quick_by_mode["General Health"])
    for icon, question in current_qs:
        if st.button(f"{icon}  {question}", key=f"qq_{mode}_{question}"):
            send_message(question, language, mode)

    # Mood Tracker
    st.markdown('<div class="section-label">😊 Mood Tracker</div>', unsafe_allow_html=True)
    moods = [("😄","Great"), ("🙂","Good"), ("😐","Okay"), ("😔","Low"), ("😰","Anxious")]
    mood_cols = st.columns(5)
    for i, (icon, mood_name) in enumerate(moods):
        with mood_cols[i]:
            st.markdown(f'<div class="mood-card"><div class="mood-icon">{icon}</div><div class="mood-name">{mood_name}</div></div>', unsafe_allow_html=True)
            if st.button("", key=f"mood_{mood_name}", help=f"I feel {mood_name}"):
                mood_entry = {"mood": mood_name, "icon": icon, "time": now, "date": today}
                st.session_state.mood_log.append(mood_entry)
                msg = f"I am feeling {mood_name} today. {icon} Can you give me some health advice based on my mood?"
                send_message(msg, language, mode)

    # Capabilities
    st.markdown('<div class="section-label">✨ Capabilities</div>', unsafe_allow_html=True)
    caps = ["Symptom analysis", "Drug information", "Mental health support", "Nutrition advice", "Emergency guidance", "Lab result explanations", "50+ languages", "Mood-based advice", "Health summaries"]
    for cap in caps:
        st.markdown(f'<div class="cap-item"><div class="cap-dot"></div>{cap}</div>', unsafe_allow_html=True)

    # Topics
    st.markdown('<div class="section-label">🏷️ Topics</div>', unsafe_allow_html=True)
    topics_html = ""
    for t in ["Heart Health", "Diabetes", "Blood Pressure", "Mental Health", "Nutrition", "Sleep", "Pregnancy", "Allergies", "Cancer", "COVID-19"]:
        topics_html += f'<span style="display:inline-block;background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.15);color:#4ade80;border-radius:20px;padding:3px 9px;font-size:11px;margin:2px;">{t}</span>'
    st.markdown(f'<div style="line-height:2.2;">{topics_html}</div>', unsafe_allow_html=True)

# ─── Main Chat Area ───────────────────────────────────────────────
with col_main:

    # Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Mood Log", "📁 Saved Sessions"])

    with tab1:
        st.markdown("""
        <div class="chat-box-header">
            <span class="chat-box-title">💬 Conversation</span>
            <span class="chat-box-badge">FastAPI Powered</span>
        </div>
        """, unsafe_allow_html=True)

        chat_area = st.container(height=420, border=True)
        with chat_area:
            st.markdown('<div class="date-badge"><span>Today</span></div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="msg-ai">
                <div class="msg-ai-ava">🤖</div>
                <div class="msg-ai-bubble">
                    <div class="msg-ai-text">Hi! I am <b style="color:#4ade80;">HealthAI Assistant</b> running in <b style="color:#4ade80;">{mode}</b> mode.<br/><br/>
                    I can help with health questions, symptom analysis, medication information, mental health support and wellness advice.<br/><br/>
                    How can I help you today? 💚</div>
                    <div class="msg-time">{now}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            for message in st.session_state.chat_history:
                t = message.get("time", now)
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="msg-user">
                        <div class="msg-user-bubble">
                            <div class="msg-user-text">{message["content"]}</div>
                            <div class="msg-time-user">{t}</div>
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
                            <div class="msg-time">{t}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Symptom Selector
        st.markdown('<div class="section-label">🩺 Quick Symptom Selector</div>', unsafe_allow_html=True)
        symptoms_list = [
            ("🌡️","Fever"),("🤒","Headache"),("💔","Chest Pain"),
            ("😮‍💨","Breathless"),("🤢","Nausea"),("😴","Fatigue"),
            ("🩸","Bleeding"),("🦴","Joint Pain"),("👁️","Blurred Vision"),
        ]
        selected_symptoms = []
        sym_cols = st.columns(9)
        for i, (icon, symptom) in enumerate(symptoms_list):
            with sym_cols[i]:
                st.markdown(f'<div class="symptom-card-wrap"><div class="symptom-icon">{icon}</div><div class="symptom-name">{symptom}</div></div>', unsafe_allow_html=True)
                if st.checkbox("", key=f"sym_{symptom}", label_visibility="collapsed"):
                    selected_symptoms.append(symptom)

        if selected_symptoms:
            st.markdown(f'<div style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.2);border-radius:10px;padding:0.6rem 1rem;margin-top:0.5rem;font-size:12px;color:#4ade80;"><b>Selected:</b> {", ".join(selected_symptoms)}</div>', unsafe_allow_html=True)
            if st.button("🔍 Analyze These Symptoms"):
                msg = f"I have these symptoms: {', '.join(selected_symptoms)}. What could be wrong and what should I do?"
                send_message(msg, language, mode)

        # Custom question input
        st.markdown('<div class="section-label">✍️ Ask a Custom Question</div>', unsafe_allow_html=True)
        custom_q = st.text_area("", placeholder="e.g. What foods help reduce inflammation? What is the normal blood pressure range?", height=70, label_visibility="collapsed", key="custom_q")
        if st.button("📤 Send Custom Question") and custom_q.strip():
            send_message(custom_q.strip(), language, mode)

        # Chat input
        user_input = st.chat_input("Type your health question here...")
        if user_input:
            send_message(user_input, language, mode)

        # Action Buttons
        if st.session_state.chat_history:
            b1, b2, b3, b4, b5 = st.columns(5)
            with b1:
                if st.button("🗑️ Clear"):
                    st.session_state.chat_history = []
                    st.rerun()
            with b2:
                chat_text = "\n\n".join([f"{'You' if m['role']=='user' else 'HealthAI'}: {m['content']}" for m in st.session_state.chat_history])
                st.download_button("💾 Save .txt", data=chat_text, file_name=f"chat_{today}.txt", mime="text/plain")
            with b3:
                chat_json = json.dumps(st.session_state.chat_history, indent=2)
                st.download_button("📋 Save .json", data=chat_json, file_name=f"chat_{today}.json", mime="application/json")
            with b4:
                if st.button("📁 Archive"):
                    if st.session_state.chat_history:
                        session = {
                            "date": today,
                            "time": now,
                            "mode": mode,
                            "messages": len(st.session_state.chat_history),
                            "preview": st.session_state.chat_history[0]["content"][:50] + "..." if st.session_state.chat_history else "",
                            "history": st.session_state.chat_history.copy()
                        }
                        st.session_state.saved_sessions.append(session)
                        st.success("✅ Session archived!")
            with b5:
                if st.button("🔄 New"):
                    st.session_state.chat_history = []
                    st.rerun()

        # Get AI Health Summary
        if len(st.session_state.chat_history) >= 4:
            st.markdown('<div class="section-label">📊 AI Session Summary</div>', unsafe_allow_html=True)
            if st.button("🧠 Generate Health Summary"):
                with st.spinner("🤖 Analyzing conversation..."):
                    convo = "\n".join([f"{'Patient' if m['role']=='user' else 'AI'}: {m['content']}" for m in st.session_state.chat_history])
                    summary_msg = f"Based on this health conversation, provide a brief summary of: 1) Main health concerns discussed, 2) Key advice given, 3) Recommended next steps. Conversation:\n{convo}"
                    summary = get_ai_response(summary_msg, [], language, mode)
                    st.markdown(f'<div style="background:#0d120d;border:1px solid rgba(74,222,128,0.2);border-radius:12px;padding:1rem;margin-top:0.5rem;"><div style="font-size:11px;color:#4ade80;font-weight:600;text-transform:uppercase;margin-bottom:8px;">🧠 AI Session Summary</div><div style="font-size:13px;color:rgba(255,255,255,0.7);line-height:1.7;">{summary}</div></div>', unsafe_allow_html=True)

    # ─── Tab 2: Mood Log ─────────────────────────────────────────
    with tab2:
        st.markdown("### 😊 Mood History")
        if st.session_state.mood_log:
            for entry in reversed(st.session_state.mood_log):
                st.markdown(f"""
                <div class="history-card">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span style="font-size:1.5rem;">{entry['icon']}</span>
                        <div>
                            <div style="font-size:13px;color:#ffffff;font-weight:600;">{entry['mood']}</div>
                            <div style="font-size:11px;color:rgba(255,255,255,0.4);">{entry['date']} at {entry['time']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Mood Stats
            st.markdown("### 📊 Mood Stats")
            mood_counts = {}
            for entry in st.session_state.mood_log:
                mood_counts[entry['mood']] = mood_counts.get(entry['mood'], 0) + 1
            for mood_name, count in mood_counts.items():
                pct = int((count / len(st.session_state.mood_log)) * 100)
                icon = next((e[0] for e in [("😄","Great"),("🙂","Good"),("😐","Okay"),("😔","Low"),("😰","Anxious")] if e[1] == mood_name), "😐")
                st.markdown(f"""
                <div style="background:#0d120d;border:1px solid #1a2e1a;border-radius:10px;padding:0.75rem 1rem;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="font-size:13px;color:#ffffff;">{icon} {mood_name}</span>
                        <span style="font-size:12px;color:#4ade80;">{count}x ({pct}%)</span>
                    </div>
                    <div style="background:#1a2e1a;border-radius:20px;height:6px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,#4ade80,#22c55e);border-radius:20px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🗑️ Clear Mood Log"):
                st.session_state.mood_log = []
                st.rerun()
        else:
            st.markdown('<div style="text-align:center;padding:3rem;color:rgba(255,255,255,0.3);"><div style="font-size:3rem;margin-bottom:1rem;">😊</div><div style="font-size:14px;">No mood entries yet</div><div style="font-size:12px;margin-top:8px;">Use the mood buttons in the sidebar to track your mood</div></div>', unsafe_allow_html=True)

    # ─── Tab 3: Saved Sessions ────────────────────────────────────
    with tab3:
        st.markdown("### 📁 Archived Chat Sessions")
        if st.session_state.saved_sessions:
            for i, session in enumerate(reversed(st.session_state.saved_sessions)):
                with st.expander(f"📅 {session['date']} at {session['time']} — {session['mode']} ({session['messages']} messages)"):
                    st.markdown(f'<div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:8px;">Preview: {session["preview"]}</div>', unsafe_allow_html=True)
                    for msg in session["history"]:
                        role = "You" if msg["role"] == "user" else "HealthAI"
                        color = "#4ade80" if msg["role"] == "assistant" else "#ffffff"
                        st.markdown(f'<div style="margin-bottom:8px;"><span style="font-size:11px;color:{color};font-weight:600;">{role}:</span><span style="font-size:12px;color:rgba(255,255,255,0.6);margin-left:8px;">{msg["content"][:200]}{"..." if len(msg["content"])>200 else ""}</span></div>', unsafe_allow_html=True)
                    chat_text = "\n\n".join([f"{'You' if m['role']=='user' else 'HealthAI'}: {m['content']}" for m in session["history"]])
                    st.download_button(f"💾 Download Session", data=chat_text, file_name=f"session_{session['date']}.txt", mime="text/plain", key=f"dl_{i}")
            if st.button("🗑️ Clear All Sessions"):
                st.session_state.saved_sessions = []
                st.rerun()
        else:
            st.markdown('<div style="text-align:center;padding:3rem;color:rgba(255,255,255,0.3);"><div style="font-size:3rem;margin-bottom:1rem;">📁</div><div style="font-size:14px;">No saved sessions yet</div><div style="font-size:12px;margin-top:8px;">Click Archive button in chat to save sessions</div></div>', unsafe_allow_html=True)

st.markdown('<div class="disclaimer">⚠️ HealthAI provides general health information only. Always consult a qualified doctor. In emergencies call 999/911/112 immediately.</div>', unsafe_allow_html=True)
