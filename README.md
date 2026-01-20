# 🧠 SecondBrain OS

**Decision Integrity & Cognitive Bias Auditing System**

A production-ready GenAI system that audits human decisions for bias, emotional distortion, and value alignment.
**Strictly Non-Prescriptive**: This system analyzes and reflects but NEVER advises.

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- OpenAI API Key (or compatible LLM provider)

### 2. Environment Setup

Create a `.env` file in the `backend/` directory:
```bash
# inside backend/.env
OPENAI_API_KEY=sk-...
```

### 3. Install Dependencies
```bash
# Backend
pip install -r backend/requirements.txt

# Frontend
pip install -r frontend/requirements.txt
```

---

## 🏃‍♂️ Running the System

You need to run the Backend and Frontend in separate terminals.

### Terminal 1: Backend (API)
Run from the project root (`SB OS`):
```bash
uvicorn backend.main:app --reload --port 8000
```
*The API will be available at http://localhost:8000*

### Terminal 2: Frontend (UI)
```bash
cd frontend
streamlit run app.py
```
*The UI will open in your browser at http://localhost:8501*

---

## 🧩 Modules Overview

1.  **Decision Decomposition**: Breaks decision into objective, constraints, assumptions, and risks.
2.  **Bias Detection**: Scans for Confirmation Bias, Loss Aversion, Overconfidence, etc.
3.  **Counterfactual Simulation**: Generates Best/Worst/Likely scenarios.
4.  **Integrity Checker**: Checks alignment with your stated values.
5.  **Report Generator**: Synthesizes a final audit report with "reflection questions" only.

## ⚠️ Integrity Constraints

- **No Advice**: The system is engineered to never say "You should" or "I recommend".
- **Decision Auditing**: Focuses on *how* you think, not *what* to choose.
