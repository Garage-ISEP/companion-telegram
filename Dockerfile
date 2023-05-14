FROM python:alpine

WORKDIR /app

COPY app.py .

RUN pip install openai flask python-dotenv telegram python-telegram-bot

EXPOSE 5000

RUN python3 app.py
