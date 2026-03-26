import streamlit as st

st.set_page_config(
    page_title="Smart Health Companion",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Smart Health Companion")
st.subheader("AI-Powered Disease Prediction & Health Assistant")

st.markdown("""
### Welcome! Choose a service from the sidebar:

- 🫀 **Heart Disease Prediction** — Enter your health data and get a prediction
- 🫁 **X-Ray Analysis** — Upload a chest X-ray for pneumonia detection
- 🤖 **Health Chatbot** — Chat with our AI health assistant
""")

st.info("⚠️ This app is for educational purposes only. Always consult a qualified doctor.")
