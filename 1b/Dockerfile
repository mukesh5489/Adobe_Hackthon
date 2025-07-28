FROM python:3.10-slim

WORKDIR /app

COPY src/ src/
COPY data/ data/
COPY requirements.txt .
COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run main.py
CMD ["python", "main.py", "data/collection2/"]
