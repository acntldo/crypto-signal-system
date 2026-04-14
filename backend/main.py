from fastapi import FastAPI
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🔥 LOADING BACKEND MAIN.PY FROM:", __file__)

# =========================
# SAFE PATH HANDLING
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "backend", "model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "top_100_cryptos_with_correct_network.csv")

# =========================
# LOAD MODEL
# =========================
model = joblib.load(MODEL_PATH)

# =========================
# HOME ROUTE
# =========================
@app.get("/")
def home():
    return {"message": "Crypto Signal API is running"}

# =========================
# PREDICT ROUTE
# =========================
from fastapi import Query

@app.get("/predict")
def predict(symbol: str = "BTCUSDT"):
    try:
        df = pd.read_csv(DATA_PATH)

        df = df[df["symbol"] == symbol].copy()

        if df.empty:
            return {"error": "No data found for symbol"}

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        # ensure numeric
        for col in ["open","high","low","close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # =========================
        # FEATURE ENGINEERING (FULL 15 FEATURES)
        # =========================

        df["return"] = df["close"].pct_change()

        df["ma7"] = df["close"].rolling(7).mean()
        df["ma14"] = df["close"].rolling(14).mean()
        df["ma30"] = df["close"].rolling(30).mean()

        ema12 = df["close"].ewm(span=12, adjust=False).mean()
        ema26 = df["close"].ewm(span=26, adjust=False).mean()
        df["ema_diff"] = ema12 - ema26

        df["volatility"] = df["return"].rolling(7).std()

        df["momentum_3"] = df["close"] - df["close"].shift(3)
        df["momentum_7"] = df["close"] - df["close"].shift(7)
        df["momentum_14"] = df["close"] - df["close"].shift(14)

        # RSI
        delta = df["close"].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / (loss + 1e-9)
        df["rsi"] = 100 - (100 / (1 + rs))

        # lag features
        df["lag_1"] = df["close"].shift(1)
        df["lag_2"] = df["close"].shift(2)
        df["lag_3"] = df["close"].shift(3)
        df["lag_7"] = df["close"].shift(7)
        df["lag_14"] = df["close"].shift(14)

        df = df.dropna()

        # EXACT SAME FEATURES AS TRAINING
        features = [
            "return",
            "ma7","ma14","ma30",
            "ema_diff",
            "volatility",
            "momentum_3","momentum_7","momentum_14",
            "rsi",
            "lag_1","lag_2","lag_3","lag_7","lag_14"
        ]

        latest = df.iloc[-1]

        X = np.array([latest[features].astype(float).values])

        pred = model.predict(X)[0]

        return {
            "symbol": symbol,
            "signal": "BUY" if pred == 1 else "HOLD",
            "raw_prediction": int(pred),
            "price": float(latest["close"]),
            "date": str(latest["date"])
        }

    except Exception as e:
        return {"error": str(e)}