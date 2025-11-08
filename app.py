import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g, abort
from pathlib import Path

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-me'
    app.config['DATABASE'] = str(Path(app.root_path) / 'instance' / 'blog.db')

    # Ensure instance dir exists (for SQLite db)
    Path(app.root_path, 'instance').mkdir(parents=True, exist_ok=True)

    # ---- DB helpers ----
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(app.config['DATABASE'])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf-8'))
        db.commit()

    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database by running schema.sql."""
        init_db()
        print('Initialized the database.')

    # ---- Routes ----
    @app.route('/')
    def index():
        db = get_db()
        posts = db.execute('SELECT id, title, body, created FROM post ORDER BY created DESC').fetchall()
        return render_template('index.html', posts=posts)

    @app.route('/post/<int:post_id>')
    def post_detail(post_id):
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = ?', (post_id,)).fetchone()
        if post is None:
            abort(404)
        return render_template('post.html', post=post)

    @app.route('/create', methods=('GET','POST'))
    def create():
        if request.method == 'POST':
            title = request.form.get('title','').strip()
            body = request.form.get('body','').strip()

            if not title:
                flash('Title is required.', 'error')
            else:
                db = get_db()
                db.execute('INSERT INTO post (title, body) VALUES (?, ?)', (title, body))
                db.commit()
                flash('Post created!', 'success')
                return redirect(url_for('index'))

        return render_template('create.html')

    @app.route('/edit/<int:post_id>', methods=('GET','POST'))
    def edit(post_id):
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = ?', (post_id,)).fetchone()
        if post is None:
            abort(404)

        if request.method == 'POST':
            title = request.form.get('title','').strip()
            body = request.form.get('body','').strip()

            if not title:
                flash('Title is required.', 'error')
            else:
                db.execute('UPDATE post SET title = ?, body = ? WHERE id = ?', (title, body, post_id))
                db.commit()
                flash('Post updated!', 'success')
                return redirect(url_for('post_detail', post_id=post_id))

        return render_template('edit.html', post=post)

    @app.route('/delete/<int:post_id>', methods=('POST',))
    def delete(post_id):
        db = get_db()
        db.execute('DELETE FROM post WHERE id = ?', (post_id,))
        db.commit()
        flash('Post deleted.', 'success')
        return redirect(url_for('index'))



@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

    return app

# Expose app for `flask --app app run`
app = create_app()