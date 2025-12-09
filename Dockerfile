FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../../AppData/Local/Temp .

CMD ["python", "src\bot_tg\async_bot_main.py"]
