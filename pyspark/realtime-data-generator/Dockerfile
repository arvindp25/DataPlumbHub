FROM python:3.10-slim

WORKDIR /app


COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the correct port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "realtime_generator:app", "--host", "0.0.0.0", "--port", "8080"]