import sqlite3
import os

def create_database_file():
    os.makedirs("data", exist_ok=True)
    db_path = os.path.join("data", "Users.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Users (id, selected_group)")

    connection.commit()
    connection.close()

def save_user_data(id: int, group: str):
    db_path = os.path.join("data", "Users.db")

    connection = sqlite3.connect(db_path)
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
    db_path = os.path.join("data", "Users.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    user = cursor.execute("SELECT id FROM Users WHERE id = ?", (id,)).fetchone()

    if not user:
        cursor.execute("INSERT INTO Users (id, selected_group) VALUES (?, ?)", (id, None))

    connection.commit()

def load_user_group(id:int):
    db_path = os.path.join("data", "Users.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT selected_group FROM Users WHERE id = ?", (id,))
    group = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    #?
    return group