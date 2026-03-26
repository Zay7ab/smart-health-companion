import streamlit as st
from PIL import Image
import numpy as np

st.title("🫁 X-Ray Analysis")
st.write("Upload a chest X-ray image to detect Pneumonia.")

st.warning("⚠️ X-Ray analysis model is loading. Please use Heart Disease Prediction and Chatbot for now.")

uploaded_file = st.file_uploader("Choose an X-ray image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded X-Ray", use_column_width=True)
    st.info("🔄 Model deployment in progress. Check back soon!")
