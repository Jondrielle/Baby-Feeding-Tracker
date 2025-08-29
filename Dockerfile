# Include docker image
FROM python:3.11-slim

# Set directory 
WORKDIR /app

# Copy only your backend code and requirements file
COPY backend /app/backend
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]


