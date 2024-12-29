# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model and application files
COPY credit_risk_dataset.csv ./credit_risk_dataset.csv
COPY main.ipynb ./main.ipynb
COPY . .

# Convert Jupyter notebook to Python script
RUN pip install jupyter nbconvert && \
    jupyter nbconvert --to script main.ipynb

# Make port 5000 available
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]