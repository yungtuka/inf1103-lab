FROM python:3.11-slim
WORKDIR /app
COPY product.py inventory.py main.py inventory.json ./
CMD ["python", "main.py"]
