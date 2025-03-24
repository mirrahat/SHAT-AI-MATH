# Use a lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all app files
COPY . .

# Expose port
EXPOSE 8000

# Run the app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
