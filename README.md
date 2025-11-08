# Flask Blog (SQLite + CRUD)

A minimal blog built with Flask and SQLite. Users can create, view, edit, and delete posts.

## Quickstart

```bash
# 1) Create & activate virtual env
python -m venv .venv
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Initialize database
flask --app app init-db

# 4) Run the server
flask --app app run --debug

# App runs at http://127.0.0.1:5000/
```

## Project Structure
```
.
├─ app.py
├─ schema.sql
├─ instance/        # holds blog.db (created after init)
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ post.html
│  ├─ create.html
│  └─ edit.html
├─ static/
│  └─ style.css
├─ requirements.txt
└─ .gitignore
```

## GitHub
```bash
git init
git add .
git commit -m "Initial Flask blog with CRUD"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Tutorial Parts Checklist

- [x] **Part 1: Flask structure & SQLite**
  - `schema.sql` present
  - `flask --app app init-db` CLI command works
  - `instance/` folder created and ignored by Git
- [x] **Part 2: Flask routes**
  - `/` (index), `/post/<id>`, `/create`, `/edit/<id>`, `/delete/<id>` (POST)
  - 404 handler template
- [x] **Part 3: Displaying posts**
  - `index.html` renders list of posts newest-first
  - `post.html` shows single post
- [x] **Part 4: Creating posts**
  - Form validation (title required)
  - Flash messages
- [x] **Part 5: Updating posts**
  - Edit form pre-filled with post
  - Saves updates and redirects to detail
- [x] **Part 6: Deleting posts**
  - Delete via POST with confirm dialog
  - Redirects to home with flash

## Optional Helpers

- `seed.py` — quick sample data after init:
  ```bash
  flask --app app init-db
  python seed.py
  ```