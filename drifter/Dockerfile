FROM python:3.12.3-slim

WORKDIR /app

COPY main.py .
COPY settings.py .

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "80"]
