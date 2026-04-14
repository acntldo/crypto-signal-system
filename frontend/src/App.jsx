import { useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import "./App.css";

function App() {
  const [data, setData] = useState(null);
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [loading, setLoading] = useState(false);
  const [chartData, setChartData] = useState([]);

  const runInference = async () => {
    setLoading(true);

    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/predict?symbol=${symbol}`
      );

      setData(res.data);

      setChartData((prev) => [
        ...prev.slice(-20),
        {
          name: res.data.date,
          price: res.data.price
        }
      ]);
    } catch (err) {
      setData({ error: "API_ERROR" });
    }

    setLoading(false);
  };

  const formatPrice = (price) => {
    if (!price) return "-";
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD"
    }).format(price);
  };

  return (
    <div className="hud">

      {/* ================= TOP BAR ================= */}
      <div className="hud-top">
        <div>CRYPTO INTELLIGENCE TERMINAL</div>

        <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
          <option value="BTCUSDT">BTCUSDT</option>
          <option value="ETHUSDT">ETHUSDT</option>
          <option value="SOLUSDT">SOLUSDT</option>
        </select>

        <button onClick={runInference} disabled={loading}>
          {loading ? "RUNNING..." : "RUN INFERENCE"}
        </button>
      </div>

      {/* ================= GRID ================= */}
      <div className="hud-grid">

        {/* ================= SIGNAL ENGINE ================= */}
        <div className="module center">
          <h3>SIGNAL ENGINE</h3>

          {data && (
            <>
              <div className={`signal-core ${data.signal}`}>
                {data.signal}
              </div>

              <div className="price-line">
                PRICE:{" "}
                <span className="price-value">
                  {formatPrice(data.price)}
                </span>
              </div>

              {/* NEW: MARKET SNAPSHOT */}
              <div className="mini-box">
                MARKET SNAPSHOT
                <div>VOLATILITY: {data.volatility || "0.00"}</div>
                <div>
                  TREND:{" "}
                  {data.signal === "BUY"
                    ? "BULLISH"
                    : data.signal === "SELL"
                    ? "BEARISH"
                    : "NEUTRAL"}
                </div>
              </div>

              <div className="small-block">
                SYMBOL: {data.symbol}
              </div>
            </>
          )}
        </div>

        {/* ================= PRICE MOVEMENT ================= */}
        <div className="module">
          <h3>PRICE MOVEMENT</h3>

          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={chartData}>
              <XAxis dataKey="name" hide />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="price" stroke="#38bdf8" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* ================= SYSTEM STATUS ================= */}
        <div className="module">
          <h3>SYSTEM STATUS</h3>

          <div className="list">

            <div className="system-model">
              MODEL: HIST-GRADIENT-BOOSTING
            </div>

            <div className="system-feature">
              FEATURES: 15 INDICATORS ACTIVE
            </div>

            <div className="system-mode">
              MODE: LIVE INFERENCE
            </div>

            {/* NEW METRICS */}
            <div className="system-feature">
              ACCURACY: ~63% VALIDATED
            </div>

            <div className="system-feature">
              DATASET: 2020–2025 OHLC HISTORY
            </div>

            <div className="system-feature">
              ENGINE: MOMENTUM + TREND MODEL
            </div>

            {data && (
              <div className="system-model">
                LAST SIGNAL: {data.signal} @ {data.date}
              </div>
            )}

            {data && (
              <div>
                RAW OUTPUT: {data.raw_prediction}
              </div>
            )}

          </div>
        </div>

      </div>
    </div>
  );
}

export default App;