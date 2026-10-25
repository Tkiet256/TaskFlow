import sqlite3
import time
import os

DB_PATH = "instance/task.db"

while True:
    os.system("cls" if os.name == "nt" else "clear")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    tasks = conn.execute("""
        SELECT * FROM tasks ORDER BY id DESC
    """).fetchall()

    print("===== TASKFLOW DATABASE =====")

    for task in tasks:
        print(dict(task))

    conn.close()

    time.sleep(1)