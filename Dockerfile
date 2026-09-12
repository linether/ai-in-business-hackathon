FROM python:3.12-slim

WORKDIR /app

# Deps first so code changes don't reinstall the world.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

ENV PYTHONPATH=/app/src PYTHONUNBUFFERED=1
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/health').read()" || exit 1

# One worker: the box has 1.6 GB and there is no local model to keep warm.
CMD ["uvicorn", "complaintguard.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
