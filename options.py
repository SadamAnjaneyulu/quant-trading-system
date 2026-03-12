import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

class OptionsAnalyzer:

    def __init__(self, risk_free_rate=0.07):
        self.rf = risk_free_rate

    def black_scholes(self, S, K, T, sigma, option_type="call"):
        if T <= 0:
            return max(S - K, 0) if option_type == "call" else max(K - S, 0)
        d1 = (np.log(S/K) + (self.rf + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == "call":
            return S*norm.cdf(d1) - K*np.exp(-self.rf*T)*norm.cdf(d2)
        return K*np.exp(-self.rf*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

    def implied_volatility(self, market_price, S, K, T, option_type="call"):
        try:
            def objective(sigma):
                return self.black_scholes(S, K, T, sigma, option_type) - market_price
            return brentq(objective, 0.001, 10.0)
        except:
            return None

    def calculate_greeks(self, S, K, T, sigma, option_type="call"):
        d1 = (np.log(S/K) + (self.rf + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        delta  = norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1
        gamma  = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta  = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                  - self.rf * K * np.exp(-self.rf*T) * norm.cdf(d2))
        vega   = S * norm.pdf(d1) * np.sqrt(T)
        return {
            "delta": round(delta, 4),
            "gamma": round(gamma, 6),
            "theta": round(theta/365, 4),
            "vega" : round(vega/100, 4)
        }

    def scan_options(self, S, T, your_sigma, option_chain):
        signals = []
        for opt in option_chain:
            K            = opt["strike"]
            market_price = opt["market_price"]
            otype        = opt["type"]
            model_price  = self.black_scholes(S, K, T, your_sigma, otype)
            iv           = self.implied_volatility(market_price, S, K, T, otype)
            gap          = market_price - model_price
            gap_pct      = (gap / model_price) * 100 if model_price > 0 else 0
            greeks       = self.calculate_greeks(S, K, T, your_sigma, otype)

            if gap_pct > 15:
                signal = "SELL 🔴"
                reason = f"Overpriced by {gap_pct:.1f}%"
            elif gap_pct < -15:
                signal = "BUY  🟢"
                reason = f"Underpriced by {abs(gap_pct):.1f}%"
            else:
                signal = "SKIP ⚪"
                reason = "Fairly priced"

            signals.append({
                "strike"      : K,
                "type"        : otype.upper(),
                "market_price": market_price,
                "model_price" : round(model_price, 2),
                "gap"         : round(gap, 2),
                "market_iv"   : f"{iv*100:.1f}%" if iv else "N/A",
                "your_iv"     : f"{your_sigma*100:.1f}%",
                "signal"      : signal,
                "reason"      : reason,
                "greeks"      : greeks
            })
        return signals
