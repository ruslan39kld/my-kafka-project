# Использую более новую версию Python для улучшения производительности - Руслан39КЛД
FROM python:3.10.2

# Задаю рабочую директорию
WORKDIR /app

# Устанавливаю сначала зависимости для кэширования слоя Docker - Руслан39КЛД
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирую исходный код приложения
COPY . .

# Добавляю информацию о необходимости переменных окружения - Руслан39КЛД
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Определяю команду для запуска приложения с улучшенной обработкой ошибок - Руслан39КЛД
CMD ["python", "-u", "app/main.py"]
