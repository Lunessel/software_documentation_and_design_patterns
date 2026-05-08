import json

import redis

from strategies.output_strategy import OutputStrategy


class RedisOutputStrategy(OutputStrategy):
    """Concrete strategy — stores records in Redis as JSON strings."""

    def __init__(self, config: dict) -> None:
        self._host = config["host"]
        self._port = config["port"]
        self._db = config.get("db", 0)
        self._key_prefix = config.get("key_prefix", "record:")
        self._client: redis.Redis | None = None
        self._counter = 0

    def open(self) -> None:
        self._client = redis.Redis(host=self._host, port=self._port, db=self._db)
        self._client.ping()
        self._counter = 0
        print(f"[Redis] Connected to {self._host}:{self._port} db={self._db}")

    def write(self, record: dict) -> None:
        key = f"{self._key_prefix}{self._counter}"
        self._client.set(key, json.dumps(record, ensure_ascii=False))
        self._counter += 1

    def close(self) -> None:
        if self._client:
            self._client.close()
            print(f"[Redis] Wrote {self._counter} keys with prefix {self._key_prefix!r}")
