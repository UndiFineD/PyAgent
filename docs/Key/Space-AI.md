# Space AI

Space exploration presents one of the most challenging environments for AI: high radiation, extreme latency, limited compute power, and zero margin for error. AI is enabling a new era of autonomous exploration and earth observation.

## Key Application Areas

### 1. Autonomous Rovers & Landers
*   **Task**: Navigating unknown terrain on Mars or the Moon without real-time human control (due to light-speed delay).
*   **Models**: Computer Vision (SLAM - Simultaneous Localization and Mapping), Path Planning (A*), Reinforcement Learning.
*   **Impact**: NASA's Perseverance rover uses AI (AutoNav) to drive faster and avoid obstacles. The Ingenuity helicopter used onboard control loops.

### 2. Earth Observation (Satellite Imagery)
*   **Task**: Analyzing petabytes of data sent down by satellites.
*   **Models**: CNNs, Vision Transformers, Segmentation models.
*   **Impact**:
    *   **Disaster Response**: Mapping floods and wildfires in real-time.
    *   **Agriculture**: Predicting crop yields and detecting pests.
    *   **Economic Monitoring**: Counting cars in parking lots or oil tanks to estimate economic activity.

### 3. Space Debris Tracking
*   **Task**: Tracking thousands of pieces of "space junk" to prevent collisions with active satellites (Kessler Syndrome).
*   **Models**: Kalman Filters, Deep Learning for orbit prediction.
*   **Impact**: Protecting the ISS and GPS infrastructure.

### 4. Astronomy & Exoplanet Discovery
*   **Task**: Finding patterns in noisy telescope data (Kepler, TESS, James Webb).
*   **Models**: Time-series analysis, Anomaly Detection.
*   **Impact**: Discovering thousands of exoplanets by detecting the tiny dip in brightness as a planet passes in front of a star. Classifying galaxies.

### 5. On-Board Edge AI
*   **Task**: Processing data *on the satellite* to reduce bandwidth. Instead of sending down 1000 cloudy images, send down the 1 clear image.
*   **Hardware**: Radiation-hardened FPGAs and specialized AI chips.
*   **Impact**: Massive reduction in downlink costs and latency.

## Challenges

*   **Radiation**: High-energy particles can flip bits in memory (Single Event Upsets), causing model failure. Hardware must be hardened.
*   **Power & Heat**: Spacecraft have very limited solar power and cannot easily dissipate heat (no air for fans).
*   **Latency**: Communication with Mars takes 4-24 minutes one way. The AI must be fully autonomous.
