
"""Full-stack study planner: Flask routes + Jinja templates + SQLite."""

import os
import sqlite3
from datetime import date
from pathlib import Path
from flask import (
    Flask, flash, redirect, render_template, request, url_for, g
)


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.update(
        SECRET_KEY=os.environ.get(
            "STUDY_PLANNER_SECRET", "dev-only-change-me"
        ),
        DATABASE=os.environ.get(
            "STUDY_PLANNER_DATABASE",
            str(Path(__file__).with_name("study_planner.db"))
        ),
        TESTING=False,
    )

    if test_config:
        app.config.update(test_config)

    def connect_db():
        db = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row

        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                course TEXT NOT NULL,
                due_date TEXT NOT NULL,
                estimated_minutes INTEGER NOT NULL
                    CHECK (estimated_minutes > 0),
                completed INTEGER NOT NULL DEFAULT 0
                    CHECK (completed IN (0, 1))
            )
        """)

        return db

    def get_db():
        if "database" not in g:
            g.database = connect_db()
        return g.database

    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("database", None)
        if db is not None:
            db.close()

    @app.get("/")
    def index():
        with get_db() as db:
            tasks = db.execute(
                "SELECT * FROM tasks ORDER BY completed, due_date, id"
            ).fetchall()

            totals = db.execute("""
                SELECT COUNT(*) AS task_count,
                       COALESCE(
                           SUM(
                               CASE WHEN completed = 0
                               THEN estimated_minutes ELSE 0 END
                           ), 0
                       ) AS remaining_minutes
                FROM tasks
            """).fetchone()

        return render_template(
            "index.html",
            tasks=tasks,
            totals=totals,
            today=date.today().isoformat()
        )

    @app.post("/tasks")
    def add_task():
        title = request.form.get("title", "").strip()
        course = request.form.get("course", "").strip()
        due_date = request.form.get("due_date", "").strip()
        minutes_text = request.form.get("estimated_minutes", "").strip()

        if not title or not course:
            flash("Task title and course are required.", "error")
            return redirect(url_for("index"))

        try:
            date.fromisoformat(due_date)
            minutes = int(minutes_text)
            if minutes <= 0:
                raise ValueError
        except ValueError:
            flash(
                "Enter a valid due date and a positive number of minutes.",
                "error"
            )
            return redirect(url_for("index"))

        with get_db() as db:
            db.execute(
                """
                INSERT INTO tasks
                    (title, course, due_date, estimated_minutes)
                VALUES (?, ?, ?, ?)
                """,
                (title, course, due_date, minutes)
            )

        flash("Task added.", "success")
        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_id>/complete")
    def complete_task(task_id):
        with get_db() as db:
            cursor = db.execute(
                "UPDATE tasks SET completed = 1 WHERE id = ?",
                (task_id,)
            )

        if cursor.rowcount == 0:
            flash("Task not found.", "error")
        else:
            flash("Completed.", "success")

        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_id>/delete")
    def delete_task(task_id):
        with get_db() as db:
            cursor = db.execute(
                "DELETE FROM tasks WHERE id = ?", (task_id,)
            )

        if cursor.rowcount:
            flash("Task deleted.", "success")
        else:
            flash("Task not found.", "error")

        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(debug=False)
