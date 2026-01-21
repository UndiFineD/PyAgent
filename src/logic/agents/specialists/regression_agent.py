# Copyright 2026 PyAgent Authors
# RegressionAgent: Predictive Trend and Relationship Specialist - Phase 319 Enhanced

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import json
import re
import math
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from src.core.base.base_agent import BaseAgent
from src.core.base.base_utilities import as_tool

__version__ = VERSION

class RegressionType(Enum):
    LINEAR = "linear"
    POLYNOMIAL = "polynomial"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    MOVING_AVERAGE = "moving_average"

@dataclass
class RegressionResult:
    """Stores regression analysis results."""
    regression_type: RegressionType
    coefficients: List[float]
    r_squared: float
    predictions: List[float]
    residuals: List[float]

class RegressionAgent(BaseAgent):
    """
    Agent specializing in predicting continuous values and analyzing relationships
    between variables (e.g., predicting code complexity growth, performance trends).
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._model_cache: Dict[str, RegressionResult] = {}
        self._prediction_history: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Regression Agent. You predict trends and quantify relationships. "
            "You look for linear and non-linear patterns in time-series and cross-sectional data. "
            "You provide confidence intervals and model diagnostics."
        )

    @as_tool
    async def predict_future_state(
        self, 
        history: List[float], 
        steps: int = 1,
        method: str = "linear"
    ) -> Dict[str, Any]:
        """Predicts the next values in a sequence using the specified method."""
        if len(history) < 2:
            return {"predictions": history, "error": "Need at least 2 data points"}
        
        regression_type = RegressionType(method) if method in [m.value for m in RegressionType] else RegressionType.LINEAR
        
        if regression_type == RegressionType.LINEAR:
            result = self._linear_regression(history, steps)
        elif regression_type == RegressionType.POLYNOMIAL:
            result = self._polynomial_regression(history, steps, degree=2)
        elif regression_type == RegressionType.EXPONENTIAL:
            result = self._exponential_regression(history, steps)
        elif regression_type == RegressionType.MOVING_AVERAGE:
            result = self._moving_average(history, steps, window=3)
        else:
            result = self._linear_regression(history, steps)
        
        # Record prediction
        self._prediction_history.append({
            "history_length": len(history),
            "steps": steps,
            "method": regression_type.value,
            "predictions": result["predictions"]
        })
        
        return result

    @as_tool
    async def analyze_correlation(
        self, 
        var_a: List[float], 
        var_b: List[float]
    ) -> Dict[str, Any]:
        """Calculates correlation and relationship metrics between two variables."""
        if len(var_a) != len(var_b):
            return {"error": "Variables must have same length"}
        
        n = len(var_a)
        if n < 2:
            return {"error": "Need at least 2 data points"}
        
        # Means
        mean_a = sum(var_a) / n
        mean_b = sum(var_b) / n
        
        # Variances and covariance
        var_a_sq = sum((x - mean_a) ** 2 for x in var_a)
        var_b_sq = sum((x - mean_b) ** 2 for x in var_b)
        covar = sum((a - mean_a) * (b - mean_b) for a, b in zip(var_a, var_b))
        
        # Pearson correlation
        denom = math.sqrt(var_a_sq * var_b_sq)
        correlation = covar / denom if denom > 0 else 0
        
        # Spearman rank correlation
        ranks_a = self._rank(var_a)
        ranks_b = self._rank(var_b)
        d_sq_sum = sum((ra - rb) ** 2 for ra, rb in zip(ranks_a, ranks_b))
        spearman = 1 - (6 * d_sq_sum) / (n * (n**2 - 1)) if n > 1 else 0
        
        # Interpretation
        strength = "strong" if abs(correlation) > 0.7 else "moderate" if abs(correlation) > 0.4 else "weak"
        direction = "positive" if correlation > 0 else "negative" if correlation < 0 else "none"
        
        return {
            "pearson_correlation": round(correlation, 4),
            "spearman_correlation": round(spearman, 4),
            "covariance": round(covar / n, 4),
            "interpretation": {
                "strength": strength,
                "direction": direction
            },
            "sample_size": n
        }

    @as_tool
    async def fit_model(
        self,
        x: List[float],
        y: List[float],
        model_type: str = "linear"
    ) -> Dict[str, Any]:
        """Fits a regression model to the data."""
        if len(x) != len(y):
            return {"error": "x and y must have same length"}
        
        n = len(x)
        if n < 2:
            return {"error": "Need at least 2 data points"}
        
        regression_type = RegressionType(model_type) if model_type in [m.value for m in RegressionType] else RegressionType.LINEAR
        
        if regression_type == RegressionType.LINEAR:
            # Fit linear: y = a + b*x
            mean_x = sum(x) / n
            mean_y = sum(y) / n
            
            numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
            denominator = sum((xi - mean_x) ** 2 for xi in x)
            
            b = numerator / denominator if denominator > 0 else 0
            a = mean_y - b * mean_x
            
            # Predictions and residuals
            predictions = [a + b * xi for xi in x]
            residuals = [yi - pi for yi, pi in zip(y, predictions)]
            
            # R-squared
            ss_res = sum(r ** 2 for r in residuals)
            ss_tot = sum((yi - mean_y) ** 2 for yi in y)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            result = RegressionResult(
                regression_type=regression_type,
                coefficients=[a, b],
                r_squared=r_squared,
                predictions=predictions,
                residuals=residuals
            )
            
            cache_key = f"linear_{n}"
            self._model_cache[cache_key] = result
            
            return {
                "model_type": "linear",
                "equation": f"y = {round(a, 4)} + {round(b, 4)} * x",
                "intercept": round(a, 4),
                "slope": round(b, 4),
                "r_squared": round(r_squared, 4),
                "std_error": round(math.sqrt(ss_res / (n - 2)) if n > 2 else 0, 4),
                "sample_size": n
            }
        
        return {"error": f"Model type {model_type} not fully implemented"}

    @as_tool
    async def detect_trend(self, data: List[float]) -> Dict[str, Any]:
        """Detects the trend in a time series."""
        n = len(data)
        if n < 3:
            return {"trend": "insufficient_data", "error": "Need at least 3 points"}
        
        # Linear trend
        x = list(range(n))
        fit = await self.fit_model(x, data, "linear")
        slope = fit.get("slope", 0)
        
        # Mann-Kendall trend test (simplified)
        s = 0
        for i in range(n):
            for j in range(i + 1, n):
                if data[j] > data[i]:
                    s += 1
                elif data[j] < data[i]:
                    s -= 1
        
        # Determine trend
        if s > 0 and slope > 0:
            trend = "increasing"
        elif s < 0 and slope < 0:
            trend = "decreasing"
        else:
            trend = "stable"
        
        # Trend strength
        max_s = n * (n - 1) / 2
        trend_strength = abs(s) / max_s if max_s > 0 else 0
        
        return {
            "trend": trend,
            "slope": round(slope, 4),
            "trend_strength": round(trend_strength, 4),
            "mann_kendall_s": s,
            "r_squared": fit.get("r_squared", 0),
            "first_value": data[0],
            "last_value": data[-1],
            "change_pct": round((data[-1] - data[0]) / abs(data[0]) * 100, 2) if data[0] != 0 else None
        }

    @as_tool
    async def forecast_with_confidence(
        self,
        history: List[float],
        steps: int = 3,
        confidence: float = 0.95
    ) -> Dict[str, Any]:
        """Provides forecasts with confidence intervals."""
        n = len(history)
        if n < 3:
            return {"error": "Need at least 3 data points for confidence intervals"}
        
        # Fit model and get predictions
        x = list(range(n))
        fit = await self.fit_model(x, history, "linear")
        
        slope = fit.get("slope", 0)
        intercept = fit.get("intercept", history[-1])
        
        # Predict future values
        forecasts = []
        for step in range(1, steps + 1):
            point = intercept + slope * (n - 1 + step)
            forecasts.append(point)
        
        # Calculate standard error
        predictions = [intercept + slope * i for i in range(n)]
        residuals = [y - p for y, p in zip(history, predictions)]
        std_error = math.sqrt(sum(r ** 2 for r in residuals) / (n - 2)) if n > 2 else 0
        
        # Z-score for confidence level (simplified)
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)
        
        # Build forecast with intervals
        forecast_details = []
        for step, point in enumerate(forecasts, 1):
            # Prediction interval widens with distance
            interval_width = z * std_error * math.sqrt(1 + 1/n + (step ** 2) / sum((i - n/2) ** 2 for i in range(n)))
            forecast_details.append({
                "step": step,
                "point_forecast": round(point, 4),
                "lower_bound": round(point - interval_width, 4),
                "upper_bound": round(point + interval_width, 4)
            })
        
        return {
            "forecasts": forecast_details,
            "confidence_level": confidence,
            "model_r_squared": fit.get("r_squared", 0),
            "std_error": round(std_error, 4)
        }

    def _linear_regression(self, history: List[float], steps: int) -> Dict[str, Any]:
        """Simple linear regression prediction."""
        n = len(history)
        x = list(range(n))
        
        mean_x = sum(x) / n
        mean_y = sum(history) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, history))
        denominator = sum((xi - mean_x) ** 2 for xi in x)
        
        slope = numerator / denominator if denominator > 0 else 0
        intercept = mean_y - slope * mean_x
        
        predictions = [intercept + slope * (n + i) for i in range(steps)]
        
        return {
            "predictions": [round(p, 4) for p in predictions],
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "method": "linear"
        }

    def _polynomial_regression(self, history: List[float], steps: int, degree: int = 2) -> Dict[str, Any]:
        """Polynomial regression (simplified quadratic)."""
        n = len(history)
        
        # Fit quadratic: use simple finite differences
        if n >= 3:
            # Estimate second derivative
            accel = (history[-1] - 2 * history[-2] + history[-3])
            slope = history[-1] - history[-2]
            
            predictions = []
            last = history[-1]
            for i in range(steps):
                last = last + slope + accel * (i + 1)
                predictions.append(last)
        else:
            return self._linear_regression(history, steps)
        
        return {
            "predictions": [round(p, 4) for p in predictions],
            "method": "polynomial",
            "degree": degree
        }

    def _exponential_regression(self, history: List[float], steps: int) -> Dict[str, Any]:
        """Exponential growth/decay prediction."""
        if any(h <= 0 for h in history):
            return self._linear_regression(history, steps)
        
        # Convert to log space for linear fit
        log_history = [math.log(h) for h in history]
        linear_result = self._linear_regression(log_history, steps)
        
        # Convert predictions back
        log_preds = linear_result["predictions"]
        predictions = [math.exp(p) for p in log_preds]
        
        return {
            "predictions": [round(p, 4) for p in predictions],
            "growth_rate": round(math.exp(linear_result["slope"]) - 1, 4),
            "method": "exponential"
        }

    def _moving_average(self, history: List[float], steps: int, window: int = 3) -> Dict[str, Any]:
        """Moving average prediction."""
        if len(history) < window:
            window = len(history)
        
        last_avg = sum(history[-window:]) / window
        predictions = [last_avg] * steps
        
        return {
            "predictions": [round(p, 4) for p in predictions],
            "window": window,
            "method": "moving_average"
        }

    def _rank(self, data: List[float]) -> List[int]:
        """Compute ranks for Spearman correlation."""
        sorted_indices = sorted(range(len(data)), key=lambda i: data[i])
        ranks = [0] * len(data)
        for rank, idx in enumerate(sorted_indices, 1):
            ranks[idx] = rank
        return ranks
