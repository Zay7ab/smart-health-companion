# 🏥 ClinIQ — AI-Powered Clinical Intelligence Platform

> Smart clinical intelligence at your fingertips. From disease prediction to emergency guidance — all in one premium dark-themed platform.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-purple)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-yellow)
![License](https://img.shields.io/badge/License-MIT-white)

---

## 🌟 Live Demo

🔗 **Web App:** [smart-health-companion.streamlit.app](https://smart-health-companion.streamlit.app)
📡 **API Docs:** [zay7ab-health-ai-api.hf.space/docs](https://zay7ab-health-ai-api.hf.space/docs)
💻 **Frontend GitHub:** [github.com/Zay7ab/smart-health-companion](https://github.com/Zay7ab/smart-health-companion)
⚙️ **Backend GitHub:** [github.com/Zay7ab/health-ai-api](https://github.com/Zay7ab/health-ai-api)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [ML Models](#ml-models)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Results](#results)

---

## 🎯 Overview

**ClinIQ** is a full-stack AI-powered health platform built with a premium dark theme UI. It combines Machine Learning, Deep Learning, and Large Language Models to provide intelligent health predictions, analysis, and guidance.

The platform uses a **microservices architecture** with:
- **FastAPI backend** deployed on Hugging Face Spaces (Docker) handling all ML predictions and AI processing
- **Streamlit frontend** deployed on Streamlit Cloud providing a premium dark-themed user interface
- **Groq API** powering all LLM-based features with LLaMA 3.3 70B

---

## ✨ Features

| Feature | Description | Technology |
|---|---|---|
| 🚨 Emergency SOS | First aid for 80+ countries worldwide | Groq LLaMA |
| 🫀 Heart Disease Prediction | 15-feature cardiac risk analysis | Random Forest ML |
| 🫁 X-Ray Analysis | Pneumonia detection from chest X-rays | CNN + ONNX |
| 🤖 AI Health Chatbot | Multi-language WhatsApp-style chat | LLaMA 3.3 70B |
| 🔍 Symptom Checker | AI-powered symptom analysis | Groq LLaMA |
| ⚖️ BMI & Vitals Calculator | Health metrics with AI insights | Groq LLaMA |
| 📊 Disease Risk Gauge | Cardiovascular risk assessment | Plotly + Groq |
| 💡 Health Tips | AI-generated personalized tips | Groq LLaMA |
| 📋 Medical History | Record tracking with AI patterns | Groq LLaMA |
| 📄 Patient Report PDF | AI-written medical reports | FPDF + Groq |
| 👨‍⚕️ Find a Doctor | Doctor & hospital recommendations | Groq LLaMA |

---

## 🛠️ Tech Stack

### Frontend
```
Streamlit          — Web interface (Dark Premium Theme)
Plotly             — Interactive charts and gauges
HTML/CSS           — Custom dark styling
```

### Backend
```
FastAPI            — REST API framework
Uvicorn            — ASGI server
Pydantic           — Data validation
Docker             — Containerization
```

### Machine Learning
```
Scikit-learn       — Random Forest, StandardScaler
TensorFlow/Keras   — CNN Deep Learning
ONNX Runtime       — Model deployment
Joblib             — Model serialization
```

### AI & NLP
```
Groq API           — LLM inference (ultra-fast)
LLaMA 3.3 70B      — Language model
```

### Deployment
```
Streamlit Cloud    — Frontend hosting (Free)
Hugging Face       — Backend API hosting (Free Docker)
GitHub             — Version control
```

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────┐
│           User Browser                      │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│      Streamlit Frontend                     │
│      (Streamlit Cloud)                      │
│      Dark Premium Theme UI                  │
│      11 Pages · FastAPI calls               │
└──────────────┬──────────────────────────────┘
               │ HTTP Requests
┌──────────────▼──────────────────────────────┐
│      FastAPI Backend                        │
│      (Hugging Face Spaces · Docker)         │
│                                             │
│  /predict/heart  /predict/xray  /chat       │
│  /bmi  /risk  /symptoms  /tips              │
│  /history  /report  /doctor  /emergency     │
└──────┬──────────────────────┬───────────────┘
       │                      │
┌──────▼──────┐    ┌──────────▼──────────────┐
│ ML Models   │    │   Groq API              │
│ rf_model    │    │   LLaMA 3.3 70B         │
│ scaler      │    │   AI insights + chat    │
│ xray.onnx   │    └─────────────────────────┘
└─────────────┘
```

---

## 🤖 ML Models

### 1. Random Forest Classifier (Heart Disease)
- **Dataset:** UCI Heart Disease Dataset
- **Features:** 15 cardiac indicators
- **Performance:** AUC Score 0.92
- **Task:** Binary classification (Disease/No Disease)
- **Format:** `.pkl` via joblib

### 2. CNN Deep Learning (X-Ray Analysis)
- **Dataset:** NIH Chest X-Ray Dataset
- **Architecture:** 3 Conv layers + MaxPooling + Dense
- **Training Accuracy:** 95%
- **Task:** Binary classification (Normal/Pneumonia)
- **Format:** `.onnx` (ONNX Runtime)

### 3. LLaMA 3.3 70B via Groq (All AI Features)
- **Provider:** Groq API
- **Speed:** ~2 seconds response time
- **Use Cases:** Chatbot, insights, tips, reports, emergency, symptom analysis

---

## 📡 API Endpoints

### Base URL: `https://zay7ab-health-ai-api.hf.space`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| POST | `/predict/heart` | Heart disease prediction |
| POST | `/predict/xray` | X-Ray pneumonia analysis |
| POST | `/chat` | AI health chatbot |
| POST | `/bmi` | BMI & vitals calculation |
| POST | `/risk` | Disease risk gauge |
| POST | `/symptoms/check` | Symptom checker |
| POST | `/tips/generate` | Generate health tips |
| POST | `/tips/daily` | Daily health tip |
| POST | `/history/analyze` | Medical history analysis |
| POST | `/report/notes` | AI doctor notes |
| POST | `/doctor/find` | Find doctor & hospital |
| POST | `/emergency/firstaid` | Emergency first aid |

---

## 🚀 Installation

### Frontend (Streamlit)
```bash
git clone https://github.com/Zay7ab/smart-health-companion
cd smart-health-companion
pip install -r requirements.txt
streamlit run app.py
```

### Backend (FastAPI)
```bash
git clone https://github.com/Zay7ab/health-ai-api
cd health-ai-api
pip install -r requirements.txt
uvicorn main:app --reload
```

### Streamlit Secrets
```toml
GROQ_API_KEY = "your_groq_api_key"
API_BASE_URL = "https://zay7ab-health-ai-api.hf.space"
```

---

## 🗂️ Project Structure
```
smart-health-companion/          # Frontend
├── app.py                       # Main home page
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── utils/
│   └── sidebar.py               # Shared dark sidebar
└── pages/
    ├── 0_🚨_Emergency.py        # Emergency SOS
    ├── 1_Heart_Disease.py       # Heart prediction
    ├── 2_Xray_Analysis.py       # X-Ray CNN
    ├── 3_Health_Chatbot.py      # AI Chatbot
    ├── 4_BMI_Calculator.py      # BMI & Vitals
    ├── 5_Health_Tips.py         # AI Tips
    ├── 6_Risk_Gauge.py          # Risk gauge
    ├── 7_Symptom_Checker.py     # Symptoms
    ├── 8_Medical_History.py     # History
    ├── 9_Patient_Report.py      # PDF Report
    └── 10_Find_Doctor.py        # Find Doctor

health-ai-api/                   # Backend
├── main.py                      # FastAPI app
├── requirements.txt
├── Dockerfile
├── README.md
├── models/
│   ├── rf_model.pkl
│   ├── scaler.pkl
│   └── xray_model.onnx
└── routers/
    ├── __init__.py
    ├── heart.py
    ├── xray.py
    ├── chat.py
    ├── bmi.py
    ├── risk.py
    ├── symptoms.py
    ├── tips.py
    ├── history.py
    ├── report.py
    ├── doctor.py
    └── emergency.py
```

---

## 📊 Results

| Model | Metric | Score |
|---|---|---|
| Random Forest | AUC Score | 0.92 |
| CNN X-Ray | Training Accuracy | 95% |
| LLaMA 3.3 70B | Response Speed | ~2s |
| FastAPI | API Uptime | 99%+ |

---

## ⚠️ Disclaimer

This application is for **educational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional. In emergencies call **999/911/112** immediately.

---

## 👨‍💻 Author

**Muhammad Zayab Ansari**
- LinkedIn: [[linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/muhammad-zayab-ansari-33947a121/)
- GitHub: [github.com/Zay7ab](https://github.com/Zay7ab)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
    <b>Made with ❤️ using Python · Streamlit · FastAPI · Groq AI · Hugging Face</b>
</div>
