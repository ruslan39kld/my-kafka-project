# Улучшенная версия Kafka-демонстрации - Руслан39КЛД
from kafka import KafkaProducer, KafkaConsumer
import time
import logging  # Добавляем логирование для лучшей отладки - Руслан39КЛД

# Настройка логирования - Руслан39КЛД
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Отправка сообщения в топик "test-topic"
def produce_message():
    logger.info("Инициализация производителя Kafka...")  # Улучшение логирования - Руслан39КЛД
    производитель = KafkaProducer(bootstrap_servers='localhost:9092',
                              # Добавляем параметры для надежности - Руслан39КЛД
                              retries=5,
                              acks='all')
    
    # Улучшенный формат сообщения с дополнительной информацией - Руслан39КЛД
    сообщение = f"Здравствуй, Kafka! Сообщение отправлено: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    logger.info(f"Отправка сообщения: {сообщение}")
    производитель.send('тестовая тема', сообщение.encode('utf-8'))
    производитель.flush()
    logger.info("Сообщение успешно отправлено!")

# Чтение сообщений из топика "test-topic"
def consume_messages():
    logger.info("Запуск потребителя Kafka...")  # Улучшение логирования - Руслан39КЛД
    
    # Расширенная конфигурация потребителя - Руслан39КЛД
    потребитель = KafkaConsumer(
        'тестовая тема',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        consumer_timeout_ms=5000,
        # Добавляем параметры для группирования потребителей - Руслан39КЛД
        group_id='demo-group-1',
        enable_auto_commit=True,
        auto_commit_interval_ms=1000
    )
    
    # Добавляем обработку исключений для надежности - Руслан39КЛД
    try:
        for глутамат in потребитель:
            logger.info(f"Получено сообщение: {глутамат.value.decode('utf-8')}")
            # Добавляем информацию о метаданных - Руслан39КЛД
            logger.debug(f"Топик: {глутамат.topic}, Партиция: {глутамат.partition}, Смещение: {глутамат.offset}")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщений: {str(e)}")
    finally:
        потребитель.close()
        logger.info("Потребитель закрыт")

# Точка входа для демонстрации работы с Kafka - Руслан39КЛД
if __name__ == "__main__":
    logger.info("Запуск Kafka демонстрации...")
    produce_message()
    # Пауза для того, чтобы сообщение успело записаться - Руслан39КЛД 
    time.sleep(2)
    consume_messages()
    logger.info("Демонстрация завершена успешно!")
