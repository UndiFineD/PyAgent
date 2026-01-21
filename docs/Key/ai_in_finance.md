# AI in Finance (FinTech)

The financial sector was one of the earliest adopters of Machine Learning, utilizing it for high-speed decision-making, risk assessment, and security.

## Key Application Areas

### 1. Algorithmic Trading (High-Frequency Trading)
*   **Task**: Executing buy/sell orders at speeds and volumes impossible for humans.
*   **Models**: Time-series forecasting (LSTMs, Transformers), Reinforcement Learning (agents learning to maximize profit while minimizing risk).
*   **Impact**: Increased market liquidity, but also risks of "Flash Crashes" caused by cascading algorithm failures.

### 2. Fraud Detection & Anti-Money Laundering (AML)
*   **Task**: Identifying suspicious transactions in real-time.
*   **Models**: Anomaly Detection (Isolation Forests, Autoencoders), Graph Neural Networks (to track money flow between accounts).
*   **Impact**: Saving billions in losses. GNNs are particularly good at detecting "smurfing" (breaking large transactions into small ones) and organized crime rings.

### 3. Credit Scoring & Underwriting
*   **Task**: Assessing the creditworthiness of a borrower.
*   **Models**: Gradient Boosted Trees (XGBoost, LightGBM), Explainable AI (SHAP values).
*   **Impact**: Expanding access to credit for "thin-file" customers by using alternative data (utility bills, rental history) instead of just FICO scores.
*   **Constraint**: Highly regulated (Fair Lending laws). Models must be explainable; "black box" denials are illegal in many jurisdictions.

### 4. Risk Management
*   **Task**: Calculating Value at Risk (VaR) and stress-testing portfolios.
*   **Models**: Monte Carlo simulations accelerated by AI, Predictive Analytics.
*   **Impact**: Helping banks maintain capital requirements and survive economic downturns.

### 5. Customer Service (Robo-Advisors)
*   **Task**: Providing personalized investment advice and automated portfolio rebalancing.
*   **Models**: NLP (Chatbots), Optimization algorithms (Modern Portfolio Theory).
*   **Impact**: Democratizing wealth management with lower fees.

## Challenges

*   **Explainability**: Regulators require clear reasons for decisions (e.g., why was a loan denied?).
*   **Non-Stationarity**: Financial markets change constantly (regime shifts). A model trained on 2019 data might fail in 2020 (COVID) or 2022 (Inflation).
*   **Adversarial Attacks**: Fraudsters actively try to reverse-engineer the fraud detection models.
