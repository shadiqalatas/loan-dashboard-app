# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app and data
COPY app.py .
COPY data/LuxuryLoanPortfolio.csv ./data/

# Expose the port Dash runs on
EXPOSE 8050

# Command to run the app
CMD ["python", "app.py"]
