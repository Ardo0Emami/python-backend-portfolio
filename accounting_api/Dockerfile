FROM python:3.11-slim

# -----------------------------
# Runtime environment settings
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------
# Working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# System dependencies
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    # build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Python dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Application source
# -----------------------------
COPY . ./accounting_api

# -----------------------------
# Expose port
# -----------------------------
EXPOSE 8000

# -----------------------------
# Start application
# -----------------------------
CMD ["uvicorn", "accounting_api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
