from websocket.connection_store import connection_store
from message_broker.event_entity import EventEntity


class EventDispatcher:
    @staticmethod
    async def dispatch(event: EventEntity):
        payload = event.model_dump()
        payload.pop("targets", None)

        if "*" in event.targets:
            await connection_store.broadcast(payload)
            return

        for public_id in event.targets:
            sockets = await connection_store.get(public_id)
            for ws in sockets:
                await ws.send_json(payload)


event_dispatcher = EventDispatcher()