FROM python

WORKDIR /app

COPY app.py .

RUN pip install openai flask dotenv telegram python-telegram-bot logging

EXPOSE 5000

RUN python3 app.py
