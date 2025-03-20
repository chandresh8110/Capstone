FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SERVICE_PORT=8001

# Make the init script executable
RUN chmod +x init.sh

# Use the init script as entrypoint
CMD ["./init.sh"] 