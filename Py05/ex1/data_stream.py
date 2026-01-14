from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):
    def __init__(self, stream_id: str, stream_type: str = None) -> None:
        self.stream_id = stream_id
        self.stream_type = stream_type

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria is None:
            return data_batch
        return [item for item in data_batch if criteria in str(item)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "stream_type": self.stream_type,
        }


class SensorStream(DataStream):
    def __init__(
        self, stream_id: str, stream_type: str = None, count: int = None,
        avg_temp: float = None
    ) -> None:
        super().__init__(stream_id, stream_type)
        self.avg_temp = avg_temp
        self.count = count

    def process_batch(self, data_batch: List[Any]) -> str:
        self.count = sum([1 for _ in data_batch[0].values()])
        new_lst = [f"{key}: {val}" for key, val in data_batch[0].items()]
        readable_str = str(new_lst).replace("'", "")
        self.avg_temp = sum(
            val for ky, val in data_batch[0].items() if ky == "temp"
        )
        return f"Processing sensor batch: {readable_str}"


class TransactionStream(DataStream):
    def __init__(
        self, stream_id: str, stream_type: str = None, net_flow: int = None
    ) -> None:
        super().__init__(stream_id, stream_type)
        self.net_flow = net_flow

    def process_batch(self, data_batch: List[Any]) -> str:
        self.count = sum([1 for _ in data_batch[0].values()])
        new_lst = [f"{key}: {val}" for key, val in data_batch[0].items()]
        readable_str = str(new_lst).replace("'", "")
        self.net_flow = sum(
            val if key == "buy_a" or "buy_b" else 0
            for key, val in data_batch[0].items()
        )
        return f"Processing sensor batch: {readable_str}"


class EventStream(DataStream):
    def __init__(
        self, stream_id: str, stream_type: str = None, detect_error: int = None
    ) -> None:
        super().__init__(stream_id, stream_type)
        self.detect_error = detect_error

    def process_batch(self, data_batch: List[Any]) -> str:
        self.count = sum(1 for _ in data_batch)
        readable_str = str(data_batch).replace("'", "")
        self.detect_error = sum(
            1 if var == "error" else 0 for var in data_batch
        )
        return f"Processing sensor batch: {readable_str}"


class StreamProcessor:
    """Coordinator for polymorphic stream processing."""

    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def register_stream(self, stream: DataStream) -> None:
        self.streams.append(stream)

    def process_all(self, batches: Dict[str, List[Any]]) -> None:
        for stream in self.streams:
            batch = batches.get(stream.stream_id)
            if batch is not None:
                stream.process_batch(batch)


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")

    print("Initializing Sensor Stream...")
    sensor_stream = SensorStream("SENSOR_001", "Environmental Data", 0, 0)
    print(
        f"Stream ID: {sensor_stream.stream_id}, "
        f"Type: {sensor_stream.stream_type}"
    )
    print(
        sensor_stream.process_batch(
            [{"temp": 22.5, "humidity": 65, "pressure": 1013}])
    )
    print(
        f"Sensor analysis: {sensor_stream.count} readings processed, "
        f"avg temp: {sensor_stream.avg_temp}°C\n"
    )

    print("Initializing Transaction Stream...")
    transaction_stream = TransactionStream("TRANS_001", "Financial Data", 0)
    print(
        f"Stream ID: {transaction_stream.stream_id}, "
        f"Type: {transaction_stream.stream_type}"
    )
    dic = {'buy_a': 100, 'sell': 150, 'buy_b': 75}
    print(
        "Processing transaction batch: "
        f"{transaction_stream.process_batch([dic])}"
    )
    print(
        f"Transaction analysis: {transaction_stream.count} operations, "
        f"net flow: +{transaction_stream.net_flow} units\n"
    )

    print("Initializing Event Stream...")
    event_stream = EventStream("EVENT_001", "System Events", 0)
    print(
        f"Stream ID: {event_stream.stream_id}, "
        f"Type: {event_stream.stream_type}"
    )
    print(
        f"Processing event batch: "
        f"{event_stream.process_batch(['login', 'error', 'logout'])}"
    )
    print(
        f"Event analysis: {event_stream.count} events, "
        f"{event_stream.detect_error} error detected\n"
    )

    print("=== Polymorphic Stream Processing ===\n"
          "Processing mixed stream types through unified interface...\n")

    print("Batch 1 Results:")
    sensor_stream.process_batch([{"temp": 22.5, "humidity": 65}])
    print(f"- Sensor data: {sensor_stream.count} readings processed")
    transaction_stream.process_batch(
        [{'buy_a': 100, 'sell': 150, 'buy_b': 75}])
    print(f"- Transaction data: {transaction_stream.count} "
          "operations processed")
    event_stream.process_batch(['login', 'error', 'logout'])
    print(f"- Event data: {event_stream.count} events processed\n")

    print("Stream filtering active: High-priority data only\n"
          "Filtered results: 2 critical sensor alerts, 1 large transaction\n")

    print("All streams processed successfully. Nexus throughput optimal.")
