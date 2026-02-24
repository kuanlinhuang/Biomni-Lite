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

# Copy entrypoint script (after pip install to maximise layer cache reuse)
COPY serve.py ./

# Create workspace directory for data and outputs
RUN mkdir -p /workspace/data

# Environment variables (override at runtime)
ENV ANTHROPIC_API_KEY=""
ENV OPENAI_API_KEY=""
ENV GEMINI_API_KEY=""
ENV GROQ_API_KEY=""
ENV BIOMNI_PATH="/workspace/data"

WORKDIR /workspace

# Default: verify installation and print usage hints
CMD ["python", "-c", "from biomni.agent import A1; from biomni.agent.ad1 import AD1; print('Biomni-Lite ready.\\n  General biomedical : A1()\\n  Alzheimer\\'s Disease: AD1()\\nExample: A1().go(\\'your query\\')  |  AD1().go(\\'your query\\')')"]
