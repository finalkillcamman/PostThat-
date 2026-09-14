FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY core ./core

ENV PYTHONPATH=/app/core

CMD ["python", "backend/app.py"]
