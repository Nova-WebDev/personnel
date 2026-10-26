from sse.event_stream import EventStream


class ConnectionStore:
    def __init__(self):
        self.streams: dict[str, set[EventStream]] = {}

    def add(self, stream: EventStream) -> None:
        self.streams.setdefault(stream.public_id, set()).add(stream)

    def remove(self, stream: EventStream) -> None:
        streams = self.streams.get(stream.public_id)
        if streams is None:
            return

        streams.discard(stream)
        if not streams:
            self.streams.pop(stream.public_id, None)

    def send(self, public_id: str, payload: dict) -> None:
        for stream in tuple(self.streams.get(public_id, ())):
            stream.offer(payload)

    def broadcast(self, payload: dict) -> None:
        for streams in tuple(self.streams.values()):
            for stream in tuple(streams):
                stream.offer(payload)

    def close_all(self) -> None:
        for streams in tuple(self.streams.values()):
            for stream in tuple(streams):
                stream.close()

    def total(self) -> int:
        return sum(len(streams) for streams in self.streams.values())


connection_store = ConnectionStore()
