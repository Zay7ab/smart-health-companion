<div align="center">

# ⚕️ Smart Health Companion
### AI-Powered Disease Prediction & Health Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-00D4FF?style=for-the-badge)

**A multi-model AI system for disease prediction, medical image analysis, and intelligent health guidance**

[Live Demo](#) · [Report Bug](#) · [Request Feature](#)

</div>

---

## 🌟 Overview

Smart Health Companion is a final year project (FYP) that combines Machine Learning, Deep Learning, and Generative AI into a single web application. Users can predict heart disease risk, analyze chest X-rays for pneumonia, and chat with an AI health assistant — all in one futuristic glassmorphism UI.

---

## 🚀 Features

| Feature | Description | Tech Used |
|---|---|---|
| 🫀 Heart Disease Prediction | Predicts heart disease risk from patient data | Random Forest, SVM |
| 🫁 X-Ray Analysis | Detects pneumonia from chest X-ray images | CNN, ONNX |
| 🤖 Health Chatbot | Multi-turn symptom-based health assistant | LLaMA 3.3 70B, Groq |

---

## 📊 Model Performance

| Model | Metric | Score |
|---|---|---|
| Random Forest | AUC-ROC | 0.92 |
| Random Forest | Test Accuracy | ~87% |
| SVM | Test Accuracy | ~85% |
| CNN (X-Ray) | Train Accuracy | 95.28% |
| CNN (X-Ray) | Test Accuracy | 79.49% |

---

## 🛠️ Tech Stack

- **Frontend** — Streamlit with custom CSS (Glassmorphism UI)
- **Machine Learning** — Scikit-learn (Random Forest, SVM)
- **Deep Learning** — TensorFlow/Keras (CNN), ONNX Runtime
- **Generative AI** — Groq API (LLaMA 3.3 70B)
- **Data Processing** — Pandas, NumPy
- **Visualization** — Matplotlib, Seaborn
- **Deployment** — Streamlit Cloud

---

## 📁 Project Structure
```
smart-health-companion/
├── app.py                      # Main Streamlit app (home page)
├── pages/
│   ├── 1_Heart_Disease.py      # Heart disease prediction page
│   ├── 2_Xray_Analysis.py      # X-ray pneumonia detection page
│   └── 3_Health_Chatbot.py     # LLM health chatbot page
├── models/
│   ├── rf_model.pkl            # Trained Random Forest model
│   ├── scaler.pkl              # Feature scaler
│   └── xray_model.onnx         # CNN model in ONNX format
├── requirements.txt
└── README.md
```

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/smart-health-companion.git
cd smart-health-companion
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key
Create a `.streamlit/secrets.toml` file:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🗂️ Datasets Used

| Dataset | Source | Size |
|---|---|---|
| UCI Heart Disease | Kaggle | 299 patients, 15 features |
| Chest X-Ray Images | Kaggle (Paul Mooney) | 5,216 training images |

---

## 🧠 How It Works

### Heart Disease Prediction
1. User inputs 15 health parameters (age, cholesterol, BP, etc.)
2. Data is scaled using StandardScaler
3. Random Forest model predicts disease probability
4. Result displayed with confidence percentage

### X-Ray Analysis
1. User uploads a chest X-ray image
2. Image resized to 150x150 and normalized
3. CNN model (ONNX) predicts Normal vs Pneumonia
4. Result displayed with confidence score

### Health Chatbot
1. User describes symptoms in natural language
2. LLaMA 3.3 70B processes the query via Groq API
3. Multi-turn conversation maintains context
4. AI responds with possible conditions and advice

---

## ⚠️ Disclaimer

This application is built for **educational purposes only** as part of a Final Year Project. It is **not a substitute for professional medical advice**. Always consult a qualified healthcare professional for proper diagnosis and treatment.

---

## 👨‍💻 Author

**Muhammad Zayab Ansari**
- Final Year Project — AI & Machine Learning
- Built with ❤️ using Python & Streamlit

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
⭐ Star this repo if you found it helpful!
</div>
