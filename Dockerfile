FROM python:3.12-alpine
COPY main.py requirements.txt lib.py /app/
WORKDIR /app

RUN pip install -r requirements.txt
CMD uvicorn main:app