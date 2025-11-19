FROM python:3.10-slim

#ARQUITETURA 32BITS
RUN apt update && \
    apt install -y build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8004
#CMD ["gunicorn", "--bind", "0.0.0.0:8004", "app:app"]
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8004", "app:app"]
