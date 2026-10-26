from message_broker.event_entity import EventEntity
from sse.connection_store import connection_store

BROADCAST_TARGET = "*"


class EventDispatcher:
    @staticmethod
    def dispatch(event: EventEntity) -> None:
        payload = event.model_dump(exclude={"targets"})

        if BROADCAST_TARGET in event.targets:
            connection_store.broadcast(payload)
            return

        for public_id in event.targets:
            connection_store.send(public_id, payload)


event_dispatcher = EventDispatcher()
