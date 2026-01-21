# Time Series Foundation Models

Just as LLMs revolutionized NLP, Foundation Models are now transforming Time Series Forecasting. Instead of training a model from scratch for every dataset (like ARIMA or Prophet), these models are pre-trained on massive corpora of time series data and can zero-shot forecast on new domains.

## 1. The Shift: From Local to Global Models

- **Local Models (ARIMA, ETS)**: Fit parameters to a single time series. Good for simple, stable data.
- **Global Deep Models (N-BEATS, TFT)**: Trained on a dataset of many time series. Learn cross-series patterns.
- **Foundation Models**: Trained on *diverse* datasets (finance, weather, energy, traffic) to learn universal temporal dynamics.

## 2. Key Architectures

### Chronos (Amazon)
- **Approach**: Tokenization.
- **Mechanism**: Treats time series forecasting as a language modeling problem.
    1. **Quantization**: Real values are binned and converted into tokens.
    2. **T5 Architecture**: Uses a pre-trained T5 (Transformer) model to predict the next "token" (value bin).
- **Strength**: Leverages the massive scale of NLP pre-training; handles missing data naturally.

### Lag-Llama (Meta/Others)
- **Approach**: LLaMA-based adaptation.
- **Mechanism**: A probabilistic forecasting model based on a decoder-only Transformer.
- **Features**: Uses "lag features" (values from past time steps) as inputs.
- **Output**: Predicts the probability distribution of the next value, allowing for uncertainty estimation (confidence intervals).

### Moirai (Salesforce)
- **Approach**: Universal Masked Encoder.
- **Mechanism**: Handles multi-variate time series with varying frequencies (hourly, daily, yearly) in a single model.
- **Patching**: Similar to Vision Transformers (ViT), it breaks time series into patches.
- **Any-variate Attention**: Can handle any number of input variables.

## 3. Zero-Shot Performance

The defining characteristic of these models is their ability to forecast on unseen datasets without fine-tuning.

- **Generalization**: They recognize patterns like seasonality, trend, and structural breaks across different domains.
- **Cold Start**: Excellent for new products or sensors where no historical data exists yet (by inferring from similar patterns seen during training).

## 4. Comparison with Traditional Methods

| Feature | ARIMA / Prophet | DeepAR / TFT | Foundation Models (Chronos/Moirai) |
| :--- | :--- | :--- | :--- |
| **Training** | Per-series (fast) | Per-dataset (slow) | Pre-trained (inference only) |
| **Data Req** | Low | High | None (Zero-shot) |
| **Accuracy** | High on simple data | High on complex data | Competitive, often SOTA on unseen data |
| **Cost** | Low compute | High compute | High inference cost (Transformer) |

## 5. Future Directions

- **Multi-Modal**: Combining time series with text (e.g., forecasting sales based on news reports).
- **Control**: Not just forecasting, but suggesting actions to influence the future (e.g., supply chain optimization).
