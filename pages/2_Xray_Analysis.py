import streamlit as st
import numpy as np
from PIL import Image
import onnxruntime as ort

st.title("🫁 X-Ray Analysis")
st.write("Upload a chest X-ray image to detect Pneumonia.")

@st.cache_resource
def load_model():
    session = ort.InferenceSession('models/xray_model.onnx')
    return session

uploaded_file = st.file_uploader("Choose an X-ray image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded X-Ray", use_column_width=True)

    if st.button("Analyze X-Ray"):
        with st.spinner("Analyzing..."):
            try:
                session = load_model()

                img = image.convert('RGB')
                img = img.resize((150, 150))
                img_array = np.array(img, dtype=np.float32) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                input_name = session.get_inputs()[0].name
                prediction = session.run(None, {input_name: img_array})[0]
                probability = prediction[0][0]

                if probability > 0.5:
                    st.error(f"⚠️ Pneumonia Detected ({probability*100:.1f}% confidence)")
                else:
                    st.success(f"✅ Normal ({(1-probability)*100:.1f}% confidence)")

                st.warning("⚠️ Always consult a qualified doctor for proper diagnosis.")

            except Exception as e:
                st.error(f"Error: {e}")
