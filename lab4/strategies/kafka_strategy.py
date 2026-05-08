import json

from kafka import KafkaProducer

from strategies.output_strategy import OutputStrategy


class KafkaOutputStrategy(OutputStrategy):
    """Concrete strategy — publishes records to a Kafka topic."""

    def __init__(self, config: dict) -> None:
        self._bootstrap_servers = config["bootstrap_servers"]
        self._topic = config["topic"]
        self._producer: KafkaProducer | None = None

    def open(self) -> None:
        self._producer = KafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
        )
        print(f"[Kafka] Connected to {self._bootstrap_servers}, topic={self._topic!r}")

    def write(self, record: dict) -> None:
        self._producer.send(self._topic, record)

    def close(self) -> None:
        if self._producer:
            self._producer.flush()
            self._producer.close()
            print("[Kafka] Producer closed.")
