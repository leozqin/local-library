FROM python:3.12-alpine
COPY main.py requirements.txt lib.py /app/
RUN pip install uv
WORKDIR /app

RUN uv pip install -r requirements.txt --system
CMD uvicorn main:app --port 80 --host 0.0.0.0
