FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs

CMD ["sh", "-c", "python src/bot_tg/async_bot_main.py > /app/logs/output.log 2>&1"]
