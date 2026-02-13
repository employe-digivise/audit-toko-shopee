# Use python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if exists, otherwise manual install
# (For simplicity we manually install here since requirements.txt covers other things)
RUN pip install flask jinja2

# Copy the application code
COPY . .

# Create outputs directory
RUN mkdir -p outputs

# Expose the requested port
EXPOSE 1101

# Run the server
CMD ["python", "execution/serve_report.py"]
