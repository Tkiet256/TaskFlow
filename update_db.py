import sqlite3

db = sqlite3.connect("instance/task.db")

db.execute("ALTER TABLE tasks ADD COLUMN start_time TEXT")
db.execute("ALTER TABLE tasks ADD COLUMN end_time TEXT")
db.execute("ALTER TABLE tasks ADD COLUMN link TEXT")

db.commit()
db.close()

print("Database updated successfully!")