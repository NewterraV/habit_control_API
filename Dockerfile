FROM python:3.11

WORKDIR /app

# Установка зависимостей
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
COPY . .

