import streamlit as st
import random

st.set_page_config(page_title="Health Tips", page_icon="💡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%); font-family: 'Rajdhani', sans-serif; }
    .page-title { font-family: 'Orbitron', monospace; font-size: 2.5rem; font-weight: 900; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: glow 3s ease-in-out infinite alternate; }
    @keyframes glow { from { filter: drop-shadow(0 0 10px #00d4ff); } to { filter: drop-shadow(0 0 30px #7b2ff7); } }
    .tip-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(0,212,255,0.2); border-radius: 20px; padding: 1.5rem; margin: 0.8rem 0; transition: all 0.3s ease; animation: slideUp 0.5s ease-out; }
    .tip-card:hover { border-color: rgba(123,47,247,0.6); box-shadow: 0 8px 30px rgba(123,47,247,0.3); transform: translateY(-3px); }
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .tip-category { font-family: 'Orbitron', monospace; font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 0.5rem; }
    .tip-text { color: rgba(255,255,255,0.85); font-size: 1.05rem; line-height: 1.6; }
    .stButton > button { background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.8rem 3rem !important; font-family: 'Orbitron', monospace !important; font-weight: 700 !important; width: 100% !important; }
    .stSelectbox label { color: #00d4ff !important; }
    [data-testid="stSidebar"] { background: rgba(10,10,26,0.95) !important; border-right: 1px solid rgba(0,212,255,0.2) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>
<div class="page-title">💡 HEALTH TIPS DASHBOARD</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">AI-curated health tips for a better life</p>
""", unsafe_allow_html=True)

tips = {
    "❤️ Heart Health": [
        "Exercise at least 30 minutes daily to strengthen your heart muscle.",
        "Reduce sodium intake to keep blood pressure in check.",
        "Eat more omega-3 rich foods like salmon, walnuts, and flaxseeds.",
        "Quit smoking — it's the single best thing you can do for your heart.",
        "Manage stress through meditation, yoga, or deep breathing exercises.",
    ],
    "🫁 Lung Health": [
        "Practice deep breathing exercises for 10 minutes every morning.",
        "Avoid exposure to air pollutants and wear a mask in dusty areas.",
        "Stay hydrated — water helps keep your airways moist and clear.",
        "Get vaccinated against flu and pneumonia to protect your lungs.",
        "Indoor plants like peace lilies can help purify indoor air.",
    ],
    "🧠 Mental Health": [
        "Practice mindfulness meditation for at least 10 minutes daily.",
        "Maintain a consistent sleep schedule — aim for 7-9 hours per night.",
        "Stay socially connected — loneliness is as harmful as smoking.",
        "Limit social media usage to reduce anxiety and comparison.",
        "Journal your thoughts daily to process emotions effectively.",
    ],
    "🥗 Nutrition": [
        "Eat a rainbow of vegetables — different colors mean different nutrients.",
        "Drink at least 8 glasses of water daily to stay properly hydrated.",
        "Reduce processed sugar intake to lower inflammation in the body.",
        "Include probiotics like yogurt to maintain a healthy gut microbiome.",
        "Don't skip breakfast — it kickstarts your metabolism for the day.",
    ],
    "🏃 Exercise": [
        "Walk 10,000 steps daily to significantly improve cardiovascular health.",
        "Include strength training twice a week to maintain muscle mass.",
        "Stretch for 10 minutes after every workout to prevent injury.",
        "Take the stairs instead of the elevator whenever possible.",
        "Even 5 minutes of movement every hour reduces sedentary risk.",
    ],
    "😴 Sleep": [
        "Keep your bedroom cool (18-20°C) for optimal sleep quality.",
        "Avoid screens 1 hour before bed to reduce blue light exposure.",
        "Establish a consistent bedtime routine to signal your brain to sleep.",
        "Avoid caffeine after 2 PM to ensure it clears your system by bedtime.",
        "Use blackout curtains to create a dark sleep environment.",
    ],
}

category = st.selectbox("🔍 Select Health Category", list(tips.keys()))

if st.button("⚡ GET TIPS"):
    selected_tips = tips[category]
    colors = ["#00d4ff", "#7b2ff7", "#ff006e", "#00ff96", "#ffaa00"]

    for i, tip in enumerate(selected_tips):
        color = colors[i % len(colors)]
        st.markdown(f"""
        <div class="tip-card">
            <div class="tip-category" style="color:{color}">💡 TIP {i+1}</div>
            <div class="tip-text">{tip}</div>
        </div>
        """, unsafe_allow_html=True)

# Daily tip
st.markdown("---")
all_tips = [tip for tips_list in tips.values() for tip in tips_list]
daily_tip = random.choice(all_tips)
st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(123,47,247,0.1));
border: 1px solid rgba(0,212,255,0.3); border-radius: 20px; padding: 2rem; text-align: center;">
    <div style="font-family: Orbitron; color: #00d4ff; font-size: 0.8rem; letter-spacing: 3px; margin-bottom: 1rem;">
        ⭐ DAILY HEALTH TIP
    </div>
    <div style="color: white; font-size: 1.1rem; line-height: 1.6;">{daily_tip}</div>
</div>
""", unsafe_allow_html=True)
