# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
ENV PORT 8080
CMD ["python", "main.py"]

# Use gunicorn for Flask on Cloud Run
ENTRYPOINT ["gunicorn", "--bind", ":8080", "main:app"]
