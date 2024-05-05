from kafka import KafkaProducer

from core.data_models import CandlesModel

_DEFAULT_URL = 'http://localhost:9092'


def create_kafka_sender():
    producer = KafkaProducer(bootstrap_servers=_DEFAULT_URL)

    async def send_candle(candle: CandlesModel):
        producer.send('candles', candle.serialize())
        producer.close()

    return send_candle
