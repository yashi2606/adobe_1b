# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the processing script by default
CMD ["python", "process_pdfs.py"]
