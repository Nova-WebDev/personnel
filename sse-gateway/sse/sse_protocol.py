import json


def format_event(name: str, payload: dict) -> str:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f"event: {name}\ndata: {body}\n\n"


def format_comment(text: str) -> str:
    return f": {text}\n\n"


def format_retry(milliseconds: int) -> str:
    return f"retry: {milliseconds}\n\n"
