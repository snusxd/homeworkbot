import json
import os
import datetime
from typing import Optional

SETTINGS_FILE = "data/settings.json"


def load_settings() -> dict:
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_channel_id() -> Optional[int]:
    data = load_settings()
    cid = data.get("CHANNEL_ID")
    if isinstance(cid, int):
        return cid
    return None


def set_channel_id(channel_id: int):
    data = load_settings()
    data["CHANNEL_ID"] = channel_id
    save_settings(data)


def get_send_time() -> Optional[str]:
    data = load_settings()
    return data.get("SEND_TIME")


def set_send_time(time_str: str):
    data = load_settings()
    data["SEND_TIME"] = time_str
    save_settings(data)

def get_last_bot_message_time() -> Optional[datetime.datetime]:
    data = load_settings()
    val = data.get("LAST_BOT_MESSAGE_TIME")
    if val is None:
        return None
    return datetime.datetime.fromisoformat(val)

def set_last_bot_message_time(dt: datetime.datetime):
    data = load_settings()
    data["LAST_BOT_MESSAGE_TIME"] = dt.isoformat()
    save_settings(data)