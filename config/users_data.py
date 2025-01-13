import json
import os
from typing import Optional

DATA_FILE = "data/users_data.json"

def load_user_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
        except json.JSONDecodeError:
            return {}

def save_user_data(user_data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

def get_user_group(user_id: int) -> Optional[str]:
    data = load_user_data()
    return data.get(str(user_id))

def set_user_group(user_id: int, group_name: str):
    data = load_user_data()
    data[str(user_id)] = group_name
    save_user_data(data)
