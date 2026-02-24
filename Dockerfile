FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for bioinformatics tools (optional, lighter than full env)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY pyproject.toml README.md LICENSE ./
COPY biomni/ ./biomni/

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[all]"

# Create workspace directory for data and outputs
RUN mkdir -p /workspace/data

# Environment variables (override at runtime)
ENV ANTHROPIC_API_KEY=""
ENV OPENAI_API_KEY=""
ENV GEMINI_API_KEY=""
ENV GROQ_API_KEY=""
ENV BIOMNI_PATH="/workspace/data"

WORKDIR /workspace

# Default: verify installation
CMD ["python", "-c", "from biomni.agent import A1; print('Biomni-Lite ready. Use A1() to start an agent.')"]
