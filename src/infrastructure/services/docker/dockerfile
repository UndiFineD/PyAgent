# Multi-stage Dockerfile for PyAgent Swarm
# Supports CPU and GPU (Ollama) execution modes

# Stage 1: Base builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: CPU Runtime
FROM python:3.11-slim AS cpu-runtime

WORKDIR /app

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYAGENT_MODE=CPU

# Default command
CMD ["python", "src/infrastructure/dev/scripts/run_fleet_self_improvement.py"]

# Stage 3: GPU Runtime (Ollama fallback)
FROM python:3.11-slim AS gpu-runtime

WORKDIR /app

# Install runtime dependencies for Ollama
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama binary
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama \
    && chmod +x /usr/bin/ollama

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYAGENT_MODE=GPU
ENV OLLAMA_HOST=0.0.0.0

# Expose Ollama port
EXPOSE 11434

# Start Ollama and application
COPY <<EOF /app/entrypoint.sh
#!/bin/bash
ollama serve &
sleep 5
python src/infrastructure/dev/scripts/run_fleet_self_improvement.py
EOF

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
