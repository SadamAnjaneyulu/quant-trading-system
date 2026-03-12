import numpy as np

class BondAnalyzer:

    def analyze(self, face_value, coupon_rate, market_rate, years):
        C         = face_value * coupon_rate
        cashflows = [C] * years
        cashflows[-1] += face_value

        price    = sum(cf/(1+market_rate)**t for t, cf in enumerate(cashflows, 1))
        weighted = sum(t*(cf/(1+market_rate)**t) for t, cf in enumerate(cashflows, 1))
        duration     = weighted / price
        mod_duration = duration / (1 + market_rate)
        convexity    = sum(t*(t+1)*(cf/(1+market_rate)**t)
                          for t, cf in enumerate(cashflows, 1)) / (price * (1+market_rate)**2)

        return {
            "price"       : round(price, 2),
            "duration"    : round(duration, 2),
            "mod_duration": round(mod_duration, 2),
            "convexity"   : round(convexity, 2)
        }

    def rate_shock_analysis(self, face_value, coupon_rate, market_rate, years):
        base      = self.analyze(face_value, coupon_rate, market_rate, years)
        scenarios = []
        for shock in [-0.03, -0.02, -0.01, 0, +0.01, +0.02, +0.03]:
            new_rate     = market_rate + shock
            new_result   = self.analyze(face_value, coupon_rate, new_rate, years)
            price_change = ((new_result["price"] - base["price"]) / base["price"] * 100)
            scenarios.append({
                "rate_change" : f"{shock*100:+.0f}%",
                "new_rate"    : f"{new_rate*100:.1f}%",
                "new_price"   : new_result["price"],
                "price_change": round(price_change, 2)
            })
        return base, scenarios
