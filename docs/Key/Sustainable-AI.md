# Sustainable AI (Green AI)

## The Environmental Impact of AI
Training large AI models is incredibly energy-intensive.
*   **Carbon Footprint**: Training a single large LLM can emit as much carbon as five cars over their lifetimes.
*   **Water Consumption**: Data centers consume millions of gallons of water for cooling.
*   **E-Waste**: Rapid hardware cycles lead to discarded GPUs and servers.

## Red AI vs. Green AI
*   **Red AI**: Buying performance by using massive compute power. The trend of "bigger is better" (more parameters, more data).
*   **Green AI**: Research focused on achieving similar results with less compute, smaller models, and more efficient data.

## Techniques for Sustainability

### 1. Efficient Architectures
*   Using **Sparse Models** (MoE) that only activate a fraction of parameters per token.
*   **Linear Attention** mechanisms (like Mamba/RWKV) that scale better than quadratic Transformers.

### 2. Model Compression
*   **Quantization**: Running 4-bit models reduces memory and energy usage by 4-8x compared to FP16.
*   **Distillation**: Using a small student model for inference instead of the giant teacher.

### 3. Carbon-Aware Computing
*   **Time-Shifting**: Scheduling training jobs to run when the local power grid is powered by renewables (e.g., solar at noon, wind at night).
*   **Location-Shifting**: Training in regions with low carbon intensity (e.g., Quebec or Norway with hydro power) rather than coal-heavy regions.

### 4. Hardware Efficiency
*   Using specialized hardware (TPUs/LPUs) that offer more TOPS/Watt (Trillions of Operations Per Second per Watt) than general GPUs.

## Metrics
*   **FLOPS**: Floating Point Operations (total compute work).
*   **PUE (Power Usage Effectiveness)**: Efficiency of the data center cooling/infrastructure.
*   **tCO2e**: Total tonnes of CO2 equivalent emissions.
