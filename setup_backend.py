import os

base_dir = r"c:\Users\harih\Zensec\backend"
docker_dir = r"c:\Users\harih\Zensec"

os.makedirs(base_dir, exist_ok=True)

main_py = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI(title="ZentraSec API", description="AI-Powered Cybersecurity APIs", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ZentraSec Backend Running", "modules": ["ML Anomaly Detection", "RAG Copilot", "Event Correlation"]}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "database": "connected", "llm": "ready"}

@app.get("/api/v1/analytics/anomaly-score")
def get_anomaly_score(asset_id: str):
    # Simulated Scikit-learn / Isolation Forest response
    return {
        "asset": asset_id,
        "anomaly_score": round(random.uniform(0.1, 0.99), 2),
        "risk_level": "High" if random.random() > 0.5 else "Medium",
        "timestamp": time.time()
    }
"""

req_txt = """fastapi==0.103.2
uvicorn==0.23.2
pydantic==2.4.2
scikit-learn==1.3.1
psycopg2-binary==2.9.9
sqlalchemy==2.0.21
elasticsearch==8.9.0
"""

docker_compose = """version: '3.8'

services:
  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=postgres
      - ES_HOST=elasticsearch
    depends_on:
      - postgres
      - elasticsearch
    
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=zentrasec
      - POSTGRES_PASSWORD=zentrasec_secure
      - POSTGRES_DB=zentrasec_events
    ports:
      - "5432:5432"

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.9.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
"""

backend_dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

frontend_dockerfile = """FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]
"""

with open(os.path.join(base_dir, "main.py"), "w") as f:
    f.write(main_py)
with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
    f.write(req_txt)
with open(os.path.join(base_dir, "Dockerfile"), "w") as f:
    f.write(backend_dockerfile)
with open(os.path.join(docker_dir, "docker-compose.yml"), "w") as f:
    f.write(docker_compose)
with open(os.path.join(docker_dir, "frontend", "Dockerfile"), "w") as f:
    f.write(frontend_dockerfile)

with open(os.path.join(docker_dir, "frontend", "next.config.ts"), "w") as f:
    f.write("import type { NextConfig } from 'next';\\n\\nconst nextConfig: NextConfig = {\\n  output: 'standalone',\\n};\\n\\nexport default nextConfig;\\n")

print("Backend and Docker setup completed.")
