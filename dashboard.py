# dashboard.py — Complete Streamlit App
# Run with: streamlit run dashboard.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.optimize import brentq

# ══════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════
st.set_page_config(
    page_title = "Quant Trading System",
    page_icon  = "📈",
    layout     = "wide"
)

# ══════════════════════════════════════
# STYLING
# ══════════════════════════════════════
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .metric-card {
        background: #1E2329;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #00C49F;
    }
    h1 { color: #00C49F; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# HEADER
# ══════════════════════════════════════
st.title("📈 Quantitative Trading System")
st.markdown("**Portfolio Optimizer • Options Scanner • Bond Risk Analyzer**")
st.markdown("*Built by [Anji](https://linkedin.com/in/anjaneyulusadam) | "
            "Python • Black-Scholes • Markowitz MPT • NSE Data*")
st.divider()

# ══════════════════════════════════════
# SIDEBAR — SETTINGS
# ══════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Settings")

    st.subheader("📊 Market")
    nifty_price = st.number_input("Nifty 50 Price", value=22150, step=50)
    your_sigma  = st.slider("Your Volatility Estimate (%)", 5, 40, 14) / 100
    dte         = st.slider("Days to Expiry", 7, 90, 30)

    st.subheader("📈 Portfolio Stocks")
    st.info("Uses simulated returns based on historical averages")

    st.subheader("🏦 Bond")
    face_val    = st.number_input("Face Value (₹)", value=100000, step=10000)
    coupon_pct  = st.slider("Coupon Rate (%)", 1, 15, 8)
    market_pct  = st.slider("Market Rate (%)", 1, 15, 8)
    bond_years  = st.slider("Tenure (Years)",  1, 30, 10)

    st.divider()
    st.markdown("🔗 [GitHub](https://github.com/anjaneyulusadam) | "
                "[LinkedIn](https://linkedin.com/in/anjaneyulusadam)")

# ══════════════════════════════════════
# HELPER FUNCTIONS (all in one file)
# ══════════════════════════════════════

def get_simulated_returns(seed=42):
    np.random.seed(seed)
    days = 252
    return pd.DataFrame({
        'RELIANCE': np.random.normal(0.00072, 0.0138, days),
        'TCS'     : np.random.normal(0.00049, 0.0125, days),
        'HDFCBANK': np.random.normal(0.00056, 0.0153, days),
        'INFY'    : np.random.normal(0.00067, 0.0135, days),
    })

def optimize_portfolio(returns, rf=0.07):
    mean_ret = returns.mean() * 252
    cov_mat  = returns.cov() * 252
    n        = len(returns.columns)

    def neg_sharpe(w):
        ret   = np.dot(w, mean_ret)
        risk  = np.sqrt(w @ cov_mat @ w)
        return -(ret - rf) / risk

    result = minimize(
        neg_sharpe,
        [1/n]*n,
        method      = "SLSQP",
        bounds      = tuple((0,1) for _ in range(n)),
        constraints = {"type":"eq","fun": lambda w: sum(w)-1}
    )
    w = result.x
    ret  = np.dot(w, mean_ret)
    risk = np.sqrt(w @ cov_mat @ w)
    return dict(zip(returns.columns, w)), ret, risk, (ret-rf)/risk

def black_scholes(S, K, T, sigma, rf=0.07, opt="call"):
    if T <= 0:
        return max(S-K,0) if opt=="call" else max(K-S,0)
    d1 = (np.log(S/K) + (rf + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if opt == "call":
        return S*norm.cdf(d1) - K*np.exp(-rf*T)*norm.cdf(d2)
    return K*np.exp(-rf*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

def get_iv(mkt_price, S, K, T, opt="call"):
    try:
        return brentq(lambda s: black_scholes(S,K,T,s,opt=opt)-mkt_price, 0.001, 10)
    except:
        return None

def get_greeks(S, K, T, sigma, rf=0.07, opt="call"):
    d1 = (np.log(S/K) + (rf+0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    delta = norm.cdf(d1) if opt=="call" else norm.cdf(d1)-1
    gamma = norm.pdf(d1) / (S*sigma*np.sqrt(T))
    theta = (-(S*norm.pdf(d1)*sigma)/(2*np.sqrt(T))
             - rf*K*np.exp(-rf*T)*norm.cdf(d2))
    vega  = S*norm.pdf(d1)*np.sqrt(T)
    return {"Δ Delta":round(delta,4), "Γ Gamma":round(gamma,6),
            "Θ Theta/day":round(theta/365,2), "V Vega/1%vol":round(vega/100,2)}

def analyze_bond(fv, cr, mr, yrs):
    C  = fv * cr
    cf = [C]*yrs
    cf[-1] += fv
    price = sum(c/(1+mr)**t for t,c in enumerate(cf,1))
    dur   = sum(t*(c/(1+mr)**t) for t,c in enumerate(cf,1)) / price
    conv  = sum(t*(t+1)*(c/(1+mr)**t) for t,c in enumerate(cf,1)) / (price*(1+mr)**2)
    return price, dur, dur/(1+mr), conv

# ══════════════════════════════════════
# SECTION 1 — LIVE METRICS BAR
# ══════════════════════════════════════
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Nifty 50",            f"₹{nifty_price:,}")
col2.metric("Your Vol Estimate",   f"{your_sigma*100:.1f}%")
col3.metric("Days to Expiry",      f"{dte} days")
col4.metric("Risk-Free Rate",      "7.0%")
col5.metric("Lot Size (Nifty)",    "75 units")

st.divider()

# ══════════════════════════════════════
# SECTION 2 — PORTFOLIO + OPTIONS SIDE BY SIDE
# ══════════════════════════════════════
left, right = st.columns(2)

# ── LEFT: PORTFOLIO ──────────────────
with left:
    st.subheader("💼 Portfolio Optimizer")
    st.caption("Mean-Variance Optimization | Max Sharpe Ratio")

    returns = get_simulated_returns()
    weights, ret, risk, sharpe = optimize_portfolio(returns)

    pm1, pm2, pm3 = st.columns(3)
    pm1.metric("Annual Return", f"{ret*100:.1f}%")
    pm2.metric("Risk",          f"{risk*100:.1f}%")
    pm3.metric("Sharpe",        f"{sharpe:.2f}")

    # Pie chart
    labels = list(weights.keys())
    vals   = list(weights.values())
    fig_pie = px.pie(
        names  = labels,
        values = vals,
        title  = "Optimal Weights",
        color_discrete_sequence = ["#00C49F","#0088FE","#FFBB28","#FF8042"]
    )
    fig_pie.update_layout(
        paper_bgcolor="#0E1117", font_color="white", height=300,
        margin=dict(t=40,b=0,l=0,r=0)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Weight bars
    for stock, w in weights.items():
        st.progress(float(w), text=f"{stock}: {w*100:.1f}%")

# ── RIGHT: OPTIONS SCANNER ───────────
with right:
    st.subheader("🔍 Options Scanner")
    st.caption(f"Black-Scholes Model | Your σ = {your_sigma*100:.1f}% | Nifty = ₹{nifty_price:,}")

    T = dte / 365
    strikes = range(int(nifty_price*0.97)//500*500,
                    int(nifty_price*1.04)//500*500+500, 500)

    rows = []
    for K in strikes:
        for otype in ["call","put"]:
            model_p = black_scholes(nifty_price, K, T, your_sigma, opt=otype)
            # Simulate market price with some IV skew
            skew    = 1.15 if otype=="put" else 1.05
            mkt_p   = model_p * skew * np.random.uniform(0.9,1.2)
            iv      = get_iv(mkt_p, nifty_price, K, T, otype)
            gap_pct = (mkt_p - model_p)/model_p*100

            if gap_pct > 15:
                signal = "🔴 SELL"
            elif gap_pct < -15:
                signal = "🟢 BUY"
            else:
                signal = "⚪ SKIP"

            rows.append({
                "Type"    : otype.upper(),
                "Strike"  : K,
                "Mkt ₹"   : round(mkt_p, 0),
                "Model ₹" : round(model_p, 0),
                "Gap %"   : f"{gap_pct:+.1f}%",
                "Mkt IV"  : f"{iv*100:.1f}%" if iv else "N/A",
                "Signal"  : signal
            })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True, height=370)

st.divider()

# ══════════════════════════════════════
# SECTION 3 — BOND RISK
# ══════════════════════════════════════
st.subheader("🏦 Bond Risk Analyzer")
st.caption("Duration • Convexity • Rate Shock Scenarios")

price, dur, mod_dur, conv = analyze_bond(
    face_val, coupon_pct/100, market_pct/100, bond_years
)

bm1, bm2, bm3, bm4, bm5 = st.columns(5)
bm1.metric("Bond Price",      f"₹{price:,.0f}")
bm2.metric("Duration",        f"{dur:.2f} yrs")
bm3.metric("Mod Duration",    f"{mod_dur:.2f}")
bm4.metric("Convexity",       f"{conv:.2f}")
bm5.metric("Rate Sensitivity",f"{-mod_dur:.2f}% per 1%↑")

# Rate shock bar chart
shocks   = [-0.03,-0.02,-0.01,0,0.01,0.02,0.03]
changes  = []
for shock in shocks:
    new_p, _, _, _ = analyze_bond(face_val, coupon_pct/100, market_pct/100+shock, bond_years)
    changes.append(round((new_p - price)/price*100, 2))

fig_bond = go.Figure(go.Bar(
    x            = [f"{s*100:+.0f}%" for s in shocks],
    y            = changes,
    marker_color = ["#00C49F" if c>=0 else "#FF4B4B" for c in changes],
    text         = [f"{c:+.2f}%" for c in changes],
    textposition = "outside"
))
fig_bond.update_layout(
    title         = "Bond Price Change Under Interest Rate Shocks",
    height        = 320,
    plot_bgcolor  = "#0E1117",
    paper_bgcolor = "#0E1117",
    font_color    = "white",
    xaxis_title   = "Rate Change",
    yaxis_title   = "Bond Price Change %",
    xaxis_gridcolor="#1E2329",
    yaxis_gridcolor="#1E2329",
)
st.plotly_chart(fig_bond, use_container_width=True)

st.divider()

# ══════════════════════════════════════
# SECTION 4 — GREEKS CALCULATOR
# ══════════════════════════════════════
st.subheader("📐 Greeks Calculator")
st.caption("Sensitivity analysis for any option")

gc1, gc2, gc3, gc4 = st.columns(4)
g_strike = gc1.number_input("Strike Price", value=int(nifty_price), step=100)
g_type   = gc2.selectbox("Option Type", ["call","put"])
g_sigma  = gc3.slider("Volatility (%)", 5, 60, int(your_sigma*100)) / 100
g_dte    = gc4.slider("Days to Expiry", 1, 90, dte)

g_price  = black_scholes(nifty_price, g_strike, g_dte/365, g_sigma, opt=g_type)
greeks   = get_greeks(nifty_price, g_strike, g_dte/365, g_sigma, opt=g_type)

gm1, gm2, gm3, gm4, gm5 = st.columns(5)
gm1.metric("Option Price", f"₹{g_price:.2f}")
for (k,v), col in zip(greeks.items(), [gm2,gm3,gm4,gm5]):
    col.metric(k, str(v))

st.divider()

# ══════════════════════════════════════
# FOOTER
# ══════════════════════════════════════
st.markdown("""
<div style='text-align:center; color:#666; padding:20px'>
    📈 <b>Quant Trading System</b> | Built by <b>Sadam Anjaneyulu (Anji)</b> <br>
    Final Year B.Tech CS — VIT-AP | Open to: Data Analyst • Quant Analyst • Fintech Roles <br>
    🔗 <a href='https://linkedin.com/in/anjaneyulusadam' style='color:#00C49F'>LinkedIn</a> |
    <a href='https://github.com/anjaneyulusadam' style='color:#00C49F'>GitHub</a>
</div>
""", unsafe_allow_html=True)
