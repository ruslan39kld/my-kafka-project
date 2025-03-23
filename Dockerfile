# Используем базовый образ Python
FROM python:3.10.2

# Задаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Определяем команду для запуска приложения
CMD ["python", "app/main.py"]
