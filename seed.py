import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "instance" / "blog.db"

def main():
    if not DB.exists():
        raise SystemExit("Database not found. Run: flask --app app init-db")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.executemany(
        "INSERT INTO post (title, body) VALUES (?, ?)",
        [
            ("Welcome to the Flask Blog", "This is your first post. Edit or delete it!"),
            ("Second Post", "Flask + SQLite CRUD example. It just works."),
            ("Tips", "Use commit messages for each tutorial part and keep your repo clean."),
        ],
    )
    con.commit()
    con.close()
    print("Seeded 3 posts.")

if __name__ == "__main__":
    main()