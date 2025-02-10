FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY leichtesprache/ ./leichtesprache/

# Expose Gradio port
EXPOSE 7860

# Configure Gradio to listen on all interfaces
ENV GRADIO_SERVER_NAME=0.0.0.0

# Start
CMD ["python3", "app.py"]
