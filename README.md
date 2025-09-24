
# Medic-AI: Agentic AI Symptom Checker 🩺

## 📖 Description
**Medic-AI** is an intelligent, agent-based system designed to analyze user-reported symptoms and provide preliminary advice.  
Users can register, log in, and describe their symptoms in natural language.  
The system leverages a **multi-agent architecture** to classify the input, match it against a local health database, and offer safe, responsible guidance.

---

## 📝 Overview
This project provides a **user-friendly interface** for individuals to quickly check their symptoms.  
When a user inputs their health concerns, the system processes the information through a pipeline of specialized AI agents.  

The final output is a **helpful suggestion** based on the analysis of a local CSV dataset containing symptom and advice information.

---

## ✨ Features
- **User Authentication**: Secure registration and login system for users.  
- **Natural Language Input**: Users can describe their symptoms conversationally.  
- **Multi-Agent System**: Utilizes three distinct agents for a structured analysis process.  
- **Symptom Matching**: Compares user input against a local health data file.  
- **Personalized Advice**: Delivers relevant advice based on the matched symptoms.  

---

## 🤖 System Architecture
Medic-AI employs a **multi-agent system** to handle user queries. Each agent has a specific role, ensuring a modular and efficient workflow.

- **Classifier Agent** 🧩  
  - First point of contact.  
  - Analyzes and extracts symptoms from raw text.  
  - Categorizes symptoms into predefined categories (e.g., *respiratory, neurological, digestive*).  

- **Matcher Agent** 🔍  
  - Takes the classified symptoms.  
  - Searches the **local CSV database** to find the closest match.  
  - Returns possible conditions related to the symptoms.  

- **Adviser Agent** 💡  
  - Generates safe, clear, and responsible advice.  
  - Always starts with a **disclaimer**.  
  - Advice is based on the condition found in the local dataset.  

---

## 💻 Technology Stack
- **Backend**: Python, FastAPI  
- **Frontend**: Streamlit  
- **Core Libraries**: Pandas, Scikit-learn (or other ML libraries as needed)  

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python **3.8 or higher**  
- `pip` (Python package installer)  

### 📥 Installation
Clone the repository:
```bash
git clone https://github.com/your-username/Medic-AI.git
cd Medic-AI
```

```bash
pip install -r requirements.txt
```

### How to run

```bash
uvicorn api.main_api:app --reload
streamlit run app.py
```


### ⚠️ Disclaimer
This tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.

Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
Never disregard professional medical advice or delay in seeking it because of something you have read on this application.
