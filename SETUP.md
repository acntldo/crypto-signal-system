# ⚙️ Project Setup Overview

This document provides a high-level guide for running the Crypto Signal Intelligence System.

The system is divided into two parts:
- Backend (FastAPI + Machine Learning Model)
- Frontend (React Dashboard UI)

Both must be running at the same time for the system to work properly.

---

## 🧠 System Flow
1. Backend loads trained ML model
2. Frontend sends symbol request (e.g. BTCUSDT)
3. Backend processes data and returns prediction
4. Frontend displays signal and analytics dashboard

---

## 📌 Requirements
- Python 3.10+
- Node.js 16+
- npm
- Virtual environment support (venv)

---

## 📊 Project Structure
- backend → API and ML model
- frontend → React dashboard UI
- data → historical crypto dataset
- model.pkl → trained ML model

---

## ⚠️ Important Notes
- Backend must be running before using frontend
- Dataset file must exist in the data folder
- Model file must be trained or already provided
