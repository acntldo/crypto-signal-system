# 🧠 Backend Setup (FastAPI + ML Model)
This section explains how to run the backend server that powers the machine learning prediction system.

---

## 📌 What the backend does
- Loads trained ML model (HistGradientBoostingClassifier)
- Processes crypto market data
- Generates BUY / HOLD / SELL signals
- Exposes API endpoints for frontend communication

---

## 📂 Backend structure
- main.py → FastAPI server
- train.py → model training script
- model.pkl → saved ML model
- data folder → historical dataset

---

## ⚙️ Setup steps

### 1. Environment setup
Create a virtual environment inside the backend folder.

---

### 2. Install dependencies
Install required Python packages listed in requirements.txt.

---

### 3. Run the backend server
Start the FastAPI application using Uvicorn.

---

## 🌐 API endpoints
- / → API status check
- /predict → returns trading signal for selected crypto symbol

---

## 📊 Output example
The backend returns:
- symbol
- signal (BUY / HOLD / SELL)
- price
- date
- volatility
- raw model prediction

---

## ⚠️ Notes
- Model file must exist before running API
- If prediction fails, check dataset path and feature consistency
