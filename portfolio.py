import numpy as np
from scipy.optimize import minimize

class PortfolioOptimizer:

    def __init__(self, returns, risk_free_rate=0.07):
        self.returns      = returns
        self.rf           = risk_free_rate
        self.mean_returns = returns.mean() * 252
        self.cov_matrix   = returns.cov() * 252
        self.n_assets     = len(returns.columns)
        self.symbols      = list(returns.columns)

    def portfolio_performance(self, weights):
        ret    = np.dot(weights, self.mean_returns)
        risk   = np.sqrt(weights @ self.cov_matrix @ weights)
        sharpe = (ret - self.rf) / risk
        return ret, risk, sharpe

    def find_optimal_portfolio(self):
        def neg_sharpe(weights):
            _, _, sharpe = self.portfolio_performance(weights)
            return -sharpe

        constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
        bounds      = tuple((0, 1) for _ in range(self.n_assets))
        initial     = [1/self.n_assets] * self.n_assets

        result = minimize(neg_sharpe, initial, method="SLSQP",
                          bounds=bounds, constraints=constraints)

        optimal_weights = result.x
        ret, risk, sharpe = self.portfolio_performance(optimal_weights)

        return {
            "weights": dict(zip(self.symbols, optimal_weights)),
            "return" : round(ret * 100, 2),
            "risk"   : round(risk * 100, 2),
            "sharpe" : round(sharpe, 2)
        }

    def find_min_risk_portfolio(self):
        def portfolio_risk(weights):
            return np.sqrt(weights @ self.cov_matrix @ weights)

        constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
        bounds      = tuple((0, 1) for _ in range(self.n_assets))
        initial     = [1/self.n_assets] * self.n_assets

        result = minimize(portfolio_risk, initial, method="SLSQP",
                          bounds=bounds, constraints=constraints)

        weights = result.x
        ret, risk, sharpe = self.portfolio_performance(weights)

        return {
            "weights": dict(zip(self.symbols, weights)),
            "return" : round(ret * 100, 2),
            "risk"   : round(risk * 100, 2),
            "sharpe" : round(sharpe, 2)
        }
