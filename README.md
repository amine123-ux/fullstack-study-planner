# Full-Stack Study Planner

A responsive study-task web app with a Flask backend, server-rendered HTML templates, CSS, and a SQLite database.

## Features
- Add tasks with course, due date, and estimated duration
- Mark tasks complete and delete tasks
- Store data in SQLite across app restarts
- Show task count and remaining estimated study minutes
- Validate form input and display success/error messages
- Responsive layout for desktop and mobile

## Tech
Python, Flask, SQLite, SQL, HTML, CSS, Jinja templates, `unittest`.

## Setup
Python 3.10+ recommended.
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python app.py
```
Open `http://127.0.0.1:5000` in your browser. The database is created automatically.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Security and design notes
- SQL statements use parameter placeholders rather than concatenating user input.
- HTML is rendered through Jinja templates, which escape ordinary template variables by default.
- For a real deployment, set a strong `STUDY_PLANNER_SECRET`, add CSRF protection, and run behind a production WSGI server. The default secret is for local development only.

## Ideas for improvement
- Add edit-task functionality and filters by course or due date
- Add a weekly workload chart
- Add user accounts only after learning authentication and password hashing
- Add database migrations and pagination for larger task lists

## Resume bullet examples — only after you run and understand the project
- Built a full-stack study planner using Flask, SQLite, HTML, and CSS to create, complete, and delete study tasks with persistent storage.
- Designed a relational task table and SQL queries to calculate remaining study time and display task summaries.
- Added input validation, responsive layouts, and automated tests for task creation, invalid input, completion, and deletion.
