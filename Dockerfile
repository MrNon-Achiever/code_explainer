# Dockerfile for Simplified Codebase-to-Course Generator
# Multi-stage build for smaller final image

# Stage 1: Build stage
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Stage 2: Production stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy from builder
COPY --from=builder /app .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Create output directory
RUN mkdir -p /app/output

# Expose port for Streamlit (if needed)
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command - run CLI help
CMD ["python", "main.py", "--help"]

# Alternative commands:
# CMD ["python", "main.py", "/path/to/codebase"]
# CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
