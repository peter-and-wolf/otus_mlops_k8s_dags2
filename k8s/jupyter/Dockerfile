FROM python:3.12.3-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install notebook evidently mlflow

COPY test-evidently.ipynb .

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]