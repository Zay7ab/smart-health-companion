<div align="center">

# 🏥 ClinIQ: Smart Health Companion
### Next-Gen AI Diagnostics & Integrated Clinical Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_LLM-00D4FF?style=for-the-badge)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)

**A professional multi-model AI suite for disease prediction, X-ray analysis, and contextual health guidance.**

[Live Demo](https://smart-health-companion.streamlit.app/) · [Report Bug](#) · [Request Feature](#)

</div>

---

## 🌟 Overview

**ClinIQ (Smart Health Companion)** is a final year project (FYP) that bridges the gap between static medical data and conversational AI. It features a unique **Vitals Observation Deck** that feeds real-time patient context into a **Llama 3.3 (70B)** powered assistant, alongside high-precision ML models for cardiac and pulmonary diagnostics.

---

## 🚀 Features

| Feature | Description | Tech Used |
|---|---|---|
| 📡 **Vitals Monitoring** | Real-time deck to track & edit BP, HR, Temp, and SpO2 | Session State, Custom CSS |
| 🫀 **Cardiac Analytics** | Predicts heart disease risk using 15 clinical parameters | Random Forest, Scikit-Learn |
| 🫁 **X-Ray Analysis** | Scans chest X-rays for pneumonia detection | CNN, ONNX Runtime |
| 🤖 **Clinical Chatbot** | Context-aware assistant using live vitals for advice | Llama 3.3 70B, Groq API |
| 📄 **Clinical Reports** | Generates professional session summaries in PDF | FPDF2, Python |

---

## 📊 Model Performance

| Model Component | Metric | Score |
|---|---|---|
| **Heart Disease (RF)** | AUC-ROC | **0.92** |
| **Heart Disease (RF)** | Test Accuracy | **~87%** |
| **CNN (X-Ray AI)** | Training Accuracy | **95.28%** |
| **CNN (X-Ray AI)** | Test Accuracy | **79.49%** |

---

## 🛠️ Tech Stack

- **Frontend** — Streamlit (Futuristic Dark Glassmorphism UI)
- **Intelligence Hub** — Groq Cloud API (Llama 3.3 70B Model)
- **Backend Communication** — FastAPI & Requests
- **Machine Learning** — Scikit-learn (Random Forest, SVM)
- **Deep Learning** — TensorFlow/Keras, ONNX
- **Reporting Engine** — FPDF2 for clinical document exports

---

## 📁 Project Structure
```text
smart-health-companion/
├── app.py                      # Main Dashboard & Vitals Observation Deck
├── pages/
│   ├── 1_Heart_Disease.py      # Cardiac prediction & risk analysis
│   ├── 2_Xray_Analysis.py      # CNN-based pneumonia detection
│   └── 3_Health_Chatbot.py     # AI Chatbot with context injection
├── models/
│   ├── rf_heart_model.pkl      # Trained ML weights
│   └── xray_model.onnx         # Optimized Deep Learning model
├── utils/
│   ├── pdf_generator.py        # Clinical PDF report logic
│   └── sidebar.py              # Navigation & theme settings
├── requirements.txt
└── README.md
