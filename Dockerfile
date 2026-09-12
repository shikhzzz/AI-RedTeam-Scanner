FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Do NOT bake secrets into the image. Pass the key at runtime:
#   docker run --env-file .env <image> python -m src.cli run experiments/exp1_baseline.yaml
CMD ["python", "-m", "src.cli"]
