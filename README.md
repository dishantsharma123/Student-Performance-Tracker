# Student Performance Tracker (Flask + SQLite)

A simple web app to track students and their grades across subjects.

## Features
- Add students (unique roll numbers)
- Add grades per subject (0–100 validation)
- View student details with average
- Delete students and grades
- Reports page for class averages and subject toppers
- SQLite database (auto-created)

## Quick Start (Local)
```bash
# 1) Create & activate virtual environment (optional but recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run
python app.py
# App will start at http://127.0.0.1:5000
```

## Project Structure
```
student_tracker/
│── app.py
│── models.py
│── requirements.txt
│── Procfile
│── templates/
│    ├── base.html
│    ├── index.html
│    ├── add_student.html
│    ├── add_grade.html
│    ├── view_student.html
│    └── reports.html
```

## Deployment (Render/Heroku)
- Ensure `requirements.txt` and `Procfile` exist.
- **Render** (recommended): Create a new Web Service, connect repo, set Start Command to `gunicorn app:app`.
- **Heroku**:
  ```bash
  heroku create
  git add .
  git commit -m "deploy student tracker"
  git push heroku main
  heroku ps:scale web=1
  ```

## Notes
- Database file `student.db` is created automatically on first run.
- To reset data, delete `student.db` and restart the app.
