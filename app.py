import sqlite3
from pathlib import Path
from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)

# đường dẫn đến cơ sở dữ liệu SQLite
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / 'instance'
DATABASE = INSTANCE_DIR / 'task.db'


def get_db():
    # lấy kết nối đến database cho request hiện tại
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    # Đóng kết nối đến database khi request kết thúc
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

    schema_path = BASE_DIR / "DataBase" / "schema.sql"

    db = sqlite3.connect(DATABASE)
    try:
        # Chỉ khởi tạo bảng nếu chưa tồn tại
        table = db.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'tasks'
        """).fetchone()

        if table is None:
            db.executescript(
                schema_path.read_text(encoding="utf-8")
            )
            db.commit()
    finally:
        db.close()


@app.route('/')
def index():
    db = get_db()

    tasks = db.execute("""
        SELECT *
        FROM tasks
        ORDER BY completed ASC, id DESC
    """).fetchall()

    tasks = [dict(task) for task in tasks]

    total = len(tasks)
    completed_count = sum(task["completed"] for task in tasks)

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed_count=completed_count
    )

@app.route('/dashboard')
def dashboard():
    return redirect(url_for('index'))

@app.route('/settings')
def settings():
    return redirect(url_for('index'))

@app.route('/help')
def help_page():
    return redirect(url_for('index'))

@app.route("/tasks", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "medium")
    due_date = request.form.get("due_date", "").strip()
    start_time = request.form.get("start_time", "").strip()
    end_time = request.form.get("end_time", "").strip()
    link = request.form.get("link", "").strip()

    if not title:
        return redirect(url_for("index"))

    if priority not in {"low", "medium", "high"}:
        priority = "medium"

    db = get_db()

    if start_time and end_time and end_time <= start_time:
        return redirect(url_for("index"))

    db.execute("""
        INSERT INTO tasks (
            title, description, priority, due_date,
            start_time, end_time, link
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        priority,
        due_date or None,
        start_time or None,
        end_time or None,
        link or None
    ))

    db.commit()

    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    db = get_db()

    db.execute(
        """
        UPDATE tasks
        SET completed = CASE
            WHEN completed = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
        """,
        (task_id,),
    )

    db.commit()

    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    db = get_db()

    db.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),
    )

    db.commit()

    return redirect(url_for("index"))

init_db()
if __name__ == "__main__":
    app.run(debug=True)
