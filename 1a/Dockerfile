
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY process_pdfs.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "process_pdfs.py"]