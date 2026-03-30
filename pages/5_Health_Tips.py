import streamlit as st
import requests
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Health Tips", page_icon="💡", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
.topbar { background: white; border: 1px solid #e0ece0; border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.topbar-title { font-size: 20px; font-weight: 700; color: #1a3a1a; }
.topbar-sub { font-size: 12px; color: #639922; margin-top: 2px; }
.ai-badge { display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(135deg,#eaf3de,#d4edbe); border: 1px solid #97c459; border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #27500a; font-weight: 600; }
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #639922; display: inline-block; }
.tip-card { background: white; border: 1px solid #e0ece0; border-radius: 14px; padding: 1.25rem; margin-bottom: 10px; display: flex; gap: 1rem; align-items: flex-start; }
.tip-number { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg,#eaf3de,#d4edbe); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: #27500a; flex-shrink: 0; }
.tip-content { flex: 1; }
.tip-title { font-size: 13px; font-weight: 600; color: #1a3a1a; margin-bottom: 4px; }
.tip-text { font-size: 12px; color: #5a6b5a; line-height: 1.6; }
.daily-tip { background: linear-gradient(135deg,#1a3a1a,#2d5a1a); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.25rem; }
.daily-tip-label { font-size: 10px; color: #97c459; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.daily-tip-text { font-size: 14px; color: white; line-height: 1.7; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">💡 Health Tips Dashboard</div>
        <div class="topbar-sub">AI-generated personalized health tips via FastAPI</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# Daily tip
if "daily_tip" not in st.session_state:
    try:
        response = requests.post(
            f"{API_URL}/tips/daily",
            json={"api_key": st.secrets.get("GROQ_API_KEY", "")},
            timeout=30
        )
        result = response.json()
        st.session_state.daily_tip = result.get("tip", "Stay hydrated and exercise daily!")
    except:
        st.session_state.daily_tip = "Drink a glass of water first thing in the morning to kickstart your metabolism."

st.markdown(f"""
<div class="daily-tip">
    <div class="daily-tip-label">⭐ Today's AI Health Tip</div>
    <div class="daily-tip-text">{st.session_state.daily_tip}</div>
</div>
""", unsafe_allow_html=True)

categories = {
    "❤️ Heart Health": "heart health, cardiovascular fitness",
    "🫁 Lung Health": "lung health, breathing exercises",
    "🧠 Mental Health": "mental health, stress management",
    "🥗 Nutrition": "nutrition, healthy eating, diet",
    "🏃 Exercise": "exercise, fitness, workout routines",
    "😴 Sleep": "sleep quality, sleep hygiene",
    "💧 Hydration": "hydration, water intake",
    "🦷 Dental Health": "dental health, oral hygiene",
    "👁️ Eye Health": "eye health, vision care",
    "🧴 Skin Health": "skin health, skincare routine",
    "🦴 Bone Health": "bone health, calcium, osteoporosis",
    "🍽️ Digestive Health": "digestive health, gut microbiome"
}

st.markdown("### 🔍 Select a Health Category")
category = st.selectbox("Category", list(categories.keys()), label_visibility="collapsed")

col1, col2 = st.columns([3, 1])
with col1:
    age_group = st.selectbox("Age Group", ["18-25", "26-35", "36-45", "46-55", "55+"])
with col2:
    generate = st.button("⚡ Generate AI Tips")

if generate:
    with st.spinner("🤖 FastAPI generating tips..."):
        try:
            response = requests.post(
                f"{API_URL}/tips/generate",
                json={
                    "category": categories[category],
                    "age_group": age_group,
                    "api_key": st.secrets.get("GROQ_API_KEY", "")
                },
                timeout=30
            )
            result = response.json()
            st.session_state.tips_result = result.get("tips", "")
            st.session_state.tips_category = category
        except Exception as e:
            st.error(f"Error: {e}")

if "tips_result" in st.session_state:
    st.markdown(f"### {st.session_state.tips_category} Tips")
    lines = st.session_state.tips_result.strip().split('\n')
    tip_num = 0
    current_title = ""
    current_text = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("TITLE:"):
            if current_title and current_text:
                tip_num += 1
                st.markdown(f"""
                <div class="tip-card">
                    <div class="tip-number">{tip_num}</div>
                    <div class="tip-content">
                        <div class="tip-title">{current_title}</div>
                        <div class="tip-text">{current_text}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            current_title = line.replace("TITLE:", "").strip()
            current_text = ""
        elif line.startswith("TIP:"):
            current_text = line.replace("TIP:", "").strip()

    if current_title and current_text:
        tip_num += 1
        st.markdown(f"""
        <div class="tip-card">
            <div class="tip-number">{tip_num}</div>
            <div class="tip-content">
                <div class="tip-title">{current_title}</div>
                <div class="tip-text">{current_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
