import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
NS_URL = os.getenv("NS_URL")
SCHOOL_ID = int(os.getenv("SCHOOL_ID"))

GROUP_CREDENTIALS = {
    "Инфотех (1)": {
        "login": os.getenv("LOGIN_INFOTECH1"),
        "password": os.getenv("PASSWORD_INFOTECH1")
    },
    "Инфотех (2)": {
        "login": os.getenv("LOGIN_INFOTECH2"),
        "password": os.getenv("PASSWORD_INFOTECH2")
    },
    "Химбио": {
        "login": os.getenv("LOGIN_HIMBIO"),
        "password": os.getenv("PASSWORD_HIMBIO")
    }
}