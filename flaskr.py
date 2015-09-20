__author__ = 'Duc'

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# application

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/index')
def index():
    cur = g.db.execute('select id, title, description from entries order by id desc')
    a = cur.fetchall()
    entries = [dict(id=row[0],title=row[1], description=row[2]) for row in a]
    print entries
    return render_template('index.html',entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, description, text) values (?, ?, ?)',
                 [request.form['title'],request.form['description'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return render_template('show_entries.html', error=error)
    return render_template('login.html', error=error)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts/')
def posts():
    cur = g.db.execute("select id, title, description, text from entries")
    a = cur.fetchall()
    entries = [dict(id=row[0],title=row[1], description=row[2], text=row[3]) for row in a]
    return render_template('post.html',entries=entries)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/posts/<id>')
def singlePost(id):
    cur = g.db.execute("select title, description, text from entries where id = %s" %id)
    a = cur.fetchall()
    entries = [dict(title=row[0], description=row[1], text=row[2]) for row in a]
    return render_template('post.html', entries=entries)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')