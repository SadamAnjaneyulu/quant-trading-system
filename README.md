# 📈 Quantitative Trading System

A professional quant trading dashboard built with Python — featuring real-time NSE market data, options mispricing scanner, portfolio optimizer, and bond risk analyzer.

🔗 **Live Demo:** [Click to Open Dashboard](https://anji-quant-trading.streamlit.app)

---

## 🚀 Features

### 📊 Portfolio Optimizer
- Mean-variance optimization (Markowitz framework)
- Maximizes Sharpe Ratio across Indian equities
- Identifies minimum risk portfolio
- Interactive pie chart of optimal weights

### 🔍 Options Mispricing Scanner
- Black-Scholes pricing model
- Compares model price vs live market price
- Calculates Implied Volatility for each strike
- Generates BUY / SELL / SKIP signals
- Full Greeks (Delta, Gamma, Theta, Vega)

### 🏦 Bond Risk Analyzer
- Bond pricing with coupon discounting
- Duration & Modified Duration calculation
- Convexity analysis
- Interest rate shock scenarios (-3% to +3%)
- Interactive rate shock bar chart

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web dashboard |
| yFinance | Market data (NSE stocks) |
| Plotly | Interactive charts |
| SciPy | Optimization + statistics |
| NumPy / Pandas | Data processing |

---

## ▶️ Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/quant-trading-system
cd quant-trading-system

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard.py
```

---

## 📐 Models Used

- **Black-Scholes-Merton** — European option pricing
- **Markowitz Mean-Variance** — Portfolio optimization
- **Modified Duration + Convexity** — Bond risk measurement
- **Implied Volatility** — Reverse BSM calculation

---

## 👤 Author

**Sadam Anjaneyulu (Anji)**  
Final Year B.Tech Computer Science — VIT-AP  
🔗 [LinkedIn](https://linkedin.com/in/anjaneyulusadam)  
📧 Open to: Data Analyst | Quant Analyst | Fintech Roles  
📍 Andhra Pradesh | Open to Relocation

---

## 📌 Key Learnings

This project was built while studying:
- Quantitative Finance (Black-Scholes, BSM derivation)
- Portfolio Theory (Efficient Frontier, Sharpe Ratio)
- Fixed Income (Duration, Convexity, Bond pricing)
- Derivatives (Options Greeks, Implied Volatility)
