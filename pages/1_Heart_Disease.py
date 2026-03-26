import streamlit as st
import joblib
import numpy as np

st.title("🫀 Heart Disease Prediction")
st.write("Enter your health information below to get a prediction.")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=50)
    sex = st.selectbox("Sex", ["Male", "Female"])
    cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3])
    trestbps = st.number_input("Resting Blood Pressure", value=120)
    chol = st.number_input("Cholesterol", value=200)
    fbs = st.selectbox("Fasting Blood Sugar > 120mg/dl", [0, 1])
    restecg = st.selectbox("Resting ECG", [0, 1, 2])

with col2:
    thalach = st.number_input("Max Heart Rate", value=150)
    exang = st.selectbox("Exercise Induced Angina", [0, 1])
    oldpeak = st.number_input("ST Depression", value=0.0)
    slope = st.selectbox("Slope", [0, 1, 2])
    ca = st.selectbox("Number of Major Vessels", [0, 1, 2, 3])
    thal = st.selectbox("Thal", [0, 1, 2, 3])

if st.button("Predict"):
    try:
        model = joblib.load('models/rf_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        
        sex_val = 1 if sex == "Male" else 0
        input_data = np.array([[age, sex_val, cp, trestbps, chol, 
                                 fbs, restecg, thalach, exang, 
                                 oldpeak, slope, ca, thal]])
        
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)[0][1]
        
        if prediction[0] == 1:
            st.error(f"⚠️ High risk of heart disease detected ({probability*100:.1f}% probability)")
        else:
            st.success(f"✅ Low risk of heart disease ({probability*100:.1f}% probability)")
            
        st.warning("⚠️ Always consult a qualified doctor for proper diagnosis.")
        
    except Exception as e:
        st.error(f"Error: {e}")
