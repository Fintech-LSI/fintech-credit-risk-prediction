FROM python:3.9-slim

WORKDIR /app

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files and application code
COPY model/random_forest_model.pkl model/
COPY model/scaler.pkl model/
COPY credit_service.py .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "credit_service.py"]