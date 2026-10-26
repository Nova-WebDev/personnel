from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_url: str

    event_channel: str = "events"
    public_key_path: str = "key/public_key.pem"

    stream_queue_size: int = 100
    heartbeat_interval: float = 15.0
    client_retry_ms: int = 3000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() # type: ignore
