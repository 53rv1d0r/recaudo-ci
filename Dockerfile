# Imagen del servicio API
FROM python:3.12-slim

WORKDIR /workspace
COPY app/ ./app/
COPY tests/ ./tests/

RUN pip install --no-cache-dir pytest

EXPOSE 8000
CMD ["python", "-m", "app.main"]