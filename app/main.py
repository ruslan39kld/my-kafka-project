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
