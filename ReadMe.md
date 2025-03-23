## Шаг 1. Запуск Kafka и ZooKeeper через Docker Compose

1. **Создайте рабочую директорию проекта.**  
   Например, создайте папку `kafka-demo`.

2. **Создайте файл `docker-compose.yml`** внутри этой папки со следующим содержимым:

   ```yaml
   version: '3'
   services:
     zookeeper:
       image: confluentinc/cp-zookeeper:latest
       container_name: zookeeper
       environment:
         ZOOKEEPER_CLIENT_PORT: 2181
         ZOOKEEPER_TICK_TIME: 2000
       ports:
         - "2181:2181"

     kafka:
       image: confluentinc/cp-kafka:latest
       container_name: kafka
       depends_on:
         - zookeeper
       ports:
         - "9092:9092"
       environment:
         KAFKA_BROKER_ID: 1
         KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
         KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
         KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
         KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
   ```

3. **Запустите Docker Compose:**  
   Откройте терминал в папке проекта и выполните команду:

   ```bash
   docker-compose up -d
   ```

   Эта команда поднимет два контейнера – ZooKeeper и Kafka. Проверьте, что контейнеры запущены:

   ```bash
   docker-compose ps
   ```

---

## Шаг 2. Создание простого Python-приложения для работы с Kafka

1. **Создайте папку `app`** в вашем проекте.

2. **Создайте файл `requirements.txt`** с содержимым:

   ```
   kafka-python==2.0.2
   ```

3. **Создайте файл `app/main.py`** с примером кода, который отправляет и читает сообщения из Kafka:

   ```python
   from kafka import KafkaProducer, KafkaConsumer
   import time

   # Отправка сообщения в топик "test-topic"
   def produce_message():
       producer = KafkaProducer(bootstrap_servers='localhost:9092')
       message = b'Hello, Kafka!'
       producer.send('test-topic', message)
       producer.flush()
       print("Сообщение отправлено:", message)

   # Чтение сообщений из топика "test-topic"
   def consume_messages():
       consumer = KafkaConsumer(
           'test-topic',
           bootstrap_servers='localhost:9092',
           auto_offset_reset='earliest',
           consumer_timeout_ms=5000
       )
       for msg in consumer:
           print("Получено сообщение:", msg.value)

   if __name__ == '__main__':
       produce_message()
       time.sleep(2)
       consume_messages()
   ```

4. **Создайте топик в Kafka:**  
   Откройте терминал и выполните команду (если не создаётся автоматически):

   ```bash
   docker exec -it kafka kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
   ```

---

## Шаг 3. Контейнеризация приложения с помощью Docker

1. **Создайте файл `Dockerfile`** в корне проекта:

   ```Dockerfile
   # Используем базовый образ Python
   FROM python:3.9-slim

   # Задаем рабочую директорию
   WORKDIR /app

   # Копируем файлы зависимостей и устанавливаем пакеты
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Копируем исходный код приложения
   COPY . .

   # Определяем команду для запуска приложения
   CMD ["python", "app/main.py"]
   ```

2. **Соберите Docker-образ:**

   Откройте терминал в корне проекта и выполните:

   ```bash
   docker build -t kafka-demo-app .
   ```

3. **Запустите приложение в контейнере:**

   ```bash
   docker run --rm --network host kafka-demo-app
   ```

   *Примечание:*  
   Параметр `--network host` позволяет контейнеру использовать сеть хоста, чтобы он мог обращаться к Kafka по адресу `localhost:9092`.

---

## Шаг 4. Внедрение CI/CD принципов

*Примитивно:*  
1. **Настройте репозиторий кода** (например, на GitHub или GitLab) и разместите туда весь проект.

2. **Создайте файл для CI/CD пайплайна**, например, для GitLab CI – `.gitlab-ci.yml`:

   ```yaml
   stages:
     - build
     - test
     - deploy

   build:
     stage: build
     image: docker:latest
     services:
       - docker:dind
     script:
       - docker build -t kafka-demo-app:$CI_COMMIT_SHORT_SHA .
     only:
       - master

   test:
     stage: test
     image: python:3.9-slim
     script:
       - pip install --no-cache-dir -r requirements.txt
       - python app/main.py
     only:
       - master

   deploy:
     stage: deploy
     image: docker:latest
     script:
       - echo "Здесь можно добавить команды для деплоя в тестовое/продакшн окружение"
     only:
       - master
   ```

3. **При каждом push** в ветку `master` пайплайн будет автоматически:
   - Собрать новый Docker-образ.
   - Запустить тесты (запуск скрипта `main.py`).
   - Выполнить этап деплоя (здесь можно интегрировать автоматический деплой в Kubernetes или обновление Docker Compose).

---

## Шаг 5. Ознакомление с Kubernetes (опционально через Docker Desktop)

1. **Включите Kubernetes в Docker Desktop:**  
   Откройте настройки Docker Desktop и в разделе Kubernetes включите его. Дождитесь запуска локального кластера.

2. **Разверните простые YAML-манифесты для приложения:**

   Создайте файл `kafka-demo-deployment.yaml`:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: kafka-demo-app
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: kafka-demo-app
     template:
       metadata:
         labels:
           app: kafka-demo-app
       spec:
         containers:
         - name: kafka-demo-app
           image: kafka-demo-app:latest
           ports:
           - containerPort: 80
   ```

   Примените манифест:

   ```bash
   kubectl apply -f kafka-demo-deployment.yaml
   ```

3. **Проверьте статус деплоя:**

   ```bash
   kubectl get pods
   kubectl get deployments
   ```

   *Примечание:*  
   Для полноценной интеграции с Kafka нужно будет настроить сервисы и, возможно, StatefulSet для Kafka, но это шаг для продвинутых пользователей. Здесь достаточно показать, что приложение можно деплоить через Kubernetes.

---

## Итог

Этот пошаговый план охватывает все основные темы урока:

- **Потоковая обработка данных с Kafka:**  
  Запуск Kafka и ZooKeeper через Docker Compose, создание топика, отправка и получение сообщений.

- **Контейнеризация:**  
  Создание Dockerfile, сборка и запуск Docker-образа для Python-приложения.

- **CI/CD:**  
  Настройка простого пайплайна для автоматической сборки, тестирования и деплоя приложения.

- **Kubernetes:**  
  (Опционально) Включение Kubernetes в Docker Desktop и деплой простого приложения через YAML-манифесты.

Эти шаги дают базовое представление о том, как создать конвейер, объединяющий все изученные технологии, и послужат отправной точкой для дальнейшего углубленного изучения и экспериментов.