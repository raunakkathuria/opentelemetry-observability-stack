FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create logs directory
RUN mkdir -p /app/logs

COPY dummy_data_generator.py .

CMD ["python", "dummy_data_generator.py"]
