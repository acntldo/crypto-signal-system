import pandas as pd

df = pd.read_csv("data/top_100_cryptos_with_correct_network.csv")

# Filter only BTC
df = df[df["symbol"] == "BTCUSDT"]

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Sort by time
df = df.sort_values("date")

print(df.head())
print(df.shape)
