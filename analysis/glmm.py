"""Random-intercept logistic GLMM fitted by maximum likelihood with Gauss-Hermite quadrature.

    logit P(y_ij = 1) = X_ij beta + u_j,   u_j ~ N(0, sigma^2)

statsmodels has no frequentist binomial GLMM, and R/lme4 is not installed, so this small,
dependency-free implementation is used. It is checked against statsmodels' GLM (sigma -> 0)
and against simulated data with known parameters in analysis/validate.py.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import optimize, special, stats


@dataclass
class GLMMResult:
    params: pd.Series
    bse: pd.Series
    sigma: float
    loglik: float
    cov: np.ndarray
    converged: bool
    n_obs: int
    n_groups: int
    separation_warning: bool

    def summary(self) -> pd.DataFrame:
        z = self.params / self.bse
        return pd.DataFrame({"coef": self.params, "se": self.bse, "z": z,
                             "p": 2 * stats.norm.sf(np.abs(z)),
                             "ci_lo": self.params - 1.96 * self.bse, "ci_hi": self.params + 1.96 * self.bse,
                             "OR": np.exp(self.params)})

    def wald(self, names_or_L) -> tuple[float, int, float]:
        """Joint Wald test that the given coefficients (or rows of L) are zero."""
        if isinstance(names_or_L, (list, tuple)) and isinstance(names_or_L[0], str):
            L = np.zeros((len(names_or_L), len(self.params)))
            for i, n in enumerate(names_or_L):
                L[i, list(self.params.index).index(n)] = 1
        else:
            L = np.atleast_2d(names_or_L)
        b = L @ self.params.values
        V = L @ self.cov[:-1, :-1] @ L.T
        chi2 = float(b @ np.linalg.solve(V, b))
        return chi2, L.shape[0], float(stats.chi2.sf(chi2, L.shape[0]))


def fit_glmm(X: pd.DataFrame, y, groups, n_quad=25, ridge=1e-6, start=None) -> GLMMResult:
    Xv = np.asarray(X, float)
    y = np.asarray(y, float)
    g_codes, g_uni = pd.factorize(np.asarray(groups))
    G, p = len(g_uni), Xv.shape[1]
    nodes, weights = np.polynomial.hermite.hermgauss(n_quad)
    logw = np.log(weights / np.sqrt(np.pi))
    # one-hot sparse sum via bincount
    def group_sum(v):  # v: (n, Q) -> (G, Q)
        return np.stack([np.bincount(g_codes, v[:, q], minlength=G) for q in range(v.shape[1])], axis=1)

    def nll_grad(theta):
        beta, log_s = theta[:p], theta[p]
        s = np.exp(log_s)
        eta = Xv @ beta
        u = np.sqrt(2) * s * nodes                         # (Q,)
        lin = eta[:, None] + u[None, :]                    # (n, Q)
        ll_i = y[:, None] * lin - np.logaddexp(0, lin)     # Bernoulli log-lik
        ll_gq = group_sum(ll_i) + logw[None, :]            # (G, Q)
        ll_g = special.logsumexp(ll_gq, axis=1)            # (G,)
        post = np.exp(ll_gq - ll_g[:, None])               # posterior weights over nodes
        resid = y[:, None] - special.expit(lin)            # (n, Q)
        w_i = post[g_codes]                                # (n, Q)
        g_beta = Xv.T @ (w_i * resid).sum(axis=1)
        g_logs = np.sum(w_i * resid * u[None, :])
        nll = -ll_g.sum() + ridge * beta @ beta
        grad = -np.append(g_beta, g_logs) + np.append(2 * ridge * beta, 0)
        return nll, grad

    theta0 = np.append(np.zeros(p) if start is None else start, np.log(0.5))
    res = optimize.minimize(nll_grad, theta0, jac=True, method="BFGS", options={"maxiter": 2000, "gtol": 1e-5})
    theta = res.x
    # numerical Hessian from the analytic gradient
    H = np.zeros((p + 1, p + 1))
    for k in range(p + 1):
        h = 1e-4 * max(1.0, abs(theta[k]))
        e = np.zeros(p + 1)
        e[k] = h
        H[:, k] = (nll_grad(theta + e)[1] - nll_grad(theta - e)[1]) / (2 * h)
    H = (H + H.T) / 2
    try:
        cov = np.linalg.inv(H)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(H)
    se = np.sqrt(np.clip(np.diag(cov), 0, None))
    names = list(X.columns)
    sep = bool(np.any(np.abs(theta[:p]) > 15) or np.any(se[:p] > 50))
    return GLMMResult(pd.Series(theta[:p], names), pd.Series(se[:p], names), float(np.exp(theta[p])),
                      float(-res.fun), cov, bool(res.success), len(y), G, sep)


def predict_logit(res: GLMMResult, X: pd.DataFrame) -> np.ndarray:
    """Conditional prediction for a typical prompt variant (u = 0)."""
    return np.asarray(X[res.params.index], float) @ res.params.values
