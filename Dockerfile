# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend files
COPY frontend/ ./frontend/

# Copy dataset
COPY ecommerce-dataset/ ./ecommerce-dataset/

# Create a simple web server for frontend
RUN pip install http-server

# Expose port
EXPOSE 5000

# Create startup script
RUN echo '#!/bin/bash\n\
cd /app/backend\n\
python app.py &\n\
cd /app/frontend\n\
python -m http.server 8000 &\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# Set the default command
CMD ["/app/start.sh"] 