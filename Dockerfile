# Multi-stage build for CHESS Project
# Stage 1: Builder
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY integrations/ ./integrations/
COPY cultural_data/ ./cultural_data/
COPY setup.py .
COPY README.md .

# Install the package
RUN pip install --user --no-cache-dir -e .

# Stage 2: Runtime
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH \
    CHESS_ENV=production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY --from=builder /build/src ./src
COPY --from=builder /build/integrations ./integrations
COPY --from=builder /build/cultural_data ./cultural_data

# Copy configuration files
COPY configs/ ./configs/
COPY docs/ ./docs/

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/cache

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "from src.core.board import Board; Board()" || exit 1

# Expose ports
EXPOSE 8000 8080

# Create non-root user for security
RUN useradd -m -u 1000 chess && chown -R chess:chess /app
USER chess

# Default command
CMD ["python", "-m", "src.main"]
