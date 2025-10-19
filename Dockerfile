FROM python:3.11-slim
WORKDIR /app
COPY backend/app /app
RUN pip install --no-cache-dir fastapi uvicorn python-multipart python-dotenv
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
