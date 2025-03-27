import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "Users.db")

def create_database_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("CREATE TABLE Users (id INTEGER PRIMARY KEY, selected_group TEXT)")
    
    connection.commit()
    connection.close()

def save_user_data(id: int, group: str):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM Users WHERE id = ?", (id,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE Users SET selected_group = ? WHERE id = ?", (group, id))
    else:
        cursor.execute("INSERT INTO Users (id, selected_group) VALUES (?, ?)", (id, group))

    connection.commit()
    connection.close()

def add_user(id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    user = cursor.execute("SELECT id FROM Users WHERE id = ?", (id,)).fetchone()

    if not user:
        cursor.execute("INSERT INTO Users (id, selected_group) VALUES (?, ?)", (id, None))

    connection.commit()
    connection.close()


def load_user_group(id:int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT selected_group FROM Users WHERE id = ?", (id,))
    result = cursor.fetchone()
    
    if result is None:
        group = None
    else:
        group = result[0]
    
    connection.close()
    return group