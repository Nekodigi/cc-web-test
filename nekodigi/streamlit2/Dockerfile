FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--logger.level=info"]
