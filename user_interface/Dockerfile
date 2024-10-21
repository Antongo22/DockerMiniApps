# Используйте официальный образ Python
FROM python:3.10-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте зависимости и код приложения
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Задайте команду для запуска приложения
CMD ["python", "app.py"]
