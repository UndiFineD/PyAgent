# Time Series Forecasting

Predicting future values based on historical data (Stock prices, Weather, Server load).

## 1. Classical Methods

*   **ARIMA (AutoRegressive Integrated Moving Average)**: The gold standard for decades. Models data based on its own past values (lags) and past forecast errors.
*   **Exponential Smoothing**: Giving more weight to recent observations.

## 2. Deep Learning Methods

*   **RNNs/LSTMs**: Naturally suited for sequences, but struggle with very long dependencies and are slow to train (sequential).
*   **TCN (Temporal Convolutional Networks)**: Using 1D convolutions with "dilation" to look far back in time. Parallelizable.
*   **Transformers (Informer, Autoformer)**:
    *   Standard Attention is $O(N^2)$, which is too expensive for long time series.
    *   **Informer**: Uses "ProbSparse" attention to reduce complexity to $O(N \log N)$.
    *   **PatchTST**: Treats time series patches as tokens, achieving state-of-the-art results.

## 3. Key Concepts

*   **Seasonality**: Repeating patterns (Daily, Weekly, Yearly).
*   **Stationarity**: Statistical properties (mean, variance) do not change over time. Most DL models handle non-stationary data better than ARIMA.
*   **Multivariate**: Using multiple variables (e.g., predicting Sales using Price + Weather + Holiday) simultaneously.
