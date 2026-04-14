import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import HistGradientBoostingClassifier
import joblib

# LOAD DATA
df = pd.read_csv("data/top_100_cryptos_with_correct_network.csv")

df = df[df["symbol"] == "BTCUSDT"]
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# FEATURES 
# Returns
df["return"] = df["close"].pct_change()

# Moving averages (trend context)
df["ma7"] = df["close"].rolling(7).mean()
df["ma14"] = df["close"].rolling(14).mean()
df["ma30"] = df["close"].rolling(30).mean()
df["ma_diff"] = df["ma7"] - df["ma30"]

# Volatility regime
df["volatility"] = df["close"].pct_change().rolling(7).std()
df["high_low_range"] = (df["high"] - df["low"]) / df["close"]

# Momentum (multi-scale)
df["momentum_3"] = df["close"] - df["close"].shift(3)
df["momentum_7"] = df["close"] - df["close"].shift(7)
df["momentum_14"] = df["close"] - df["close"].shift(14)

# Lag structure
for lag in [1, 2, 3, 7, 14]:
    df[f"lag_{lag}"] = df["close"].shift(lag)

# TARGET 
# 3-day future trend
df["future_price"] = df["close"].shift(-3)

df["future_return"] = (df["future_price"] - df["close"]) / df["close"]

def label(x):
    if x > 0.015:
        return 1
    elif x < -0.015:
        return 0
    else:
        return 0  # treat neutral as 0

df["target"] = label
df["target"] = df["future_return"].apply(lambda x: 1 if x > 0.015 else 0)

# CLEAN
df = df.dropna()

features = [
    "return",
    "ma7",
    "ma14",
    "ma30",
    "ma_diff",
    "volatility",
    "high_low_range",
    "momentum_3",
    "momentum_7",
    "momentum_14",
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_7",
    "lag_14"
]

X = df[features]
y = df["target"]

print("\nClass distribution:")
print(y.value_counts())

# TIME SPLIT
split = int(len(df) * 0.8)

X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# MODEL
model = HistGradientBoostingClassifier(
    max_depth=8,
    learning_rate=0.03,
    max_iter=500
)

model.fit(X_train, y_train)

# EVALUATION
pred = model.predict(X_test)

print("\n\nClassification Report:\n")
print(classification_report(y_test, pred))

acc = (pred == y_test).mean()
print("\nAccuracy:", acc)

# SAVE
joblib.dump(model, "backend/model.pkl")
print("\nModel saved!")