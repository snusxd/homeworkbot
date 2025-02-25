import sqlite3
import os

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


def load_user_group(id:int):
    db_path = os.path.join("data", "Users.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT selected_group FROM Users WHERE id = ?", (id,))
    group = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return group