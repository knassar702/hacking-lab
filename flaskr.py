__author__ = 'Khaled Nassar'

# all the imports
import sqlite3,time,datetime
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash,make_response
from contextlib import closing

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'
name = 'Hacking-Blog'
now = datetime.datetime.today()
date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
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

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
# defining function 
  return render_template("404.html") 
@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/home')
@app.route('/home.html')
def index():
    cur = g.db.execute('select id, title, description, date from entries order by id desc limit 8')
    a = cur.fetchall()
    entries = [dict(id=row[0],title=row[1], description=row[2],d=row[3]) for row in a]
    print entries
    response=make_response(render_template('index.html',entries=entries,Name=name))
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
@app.route('/posts')
def posts():
    cur = g.db.execute('select id, title, description, date from entries order by id desc')
    a = cur.fetchall()
    entries = [dict(id=row[0],title=row[1], description=row[2],d=row[3]) for row in a]
    return render_template('index.html',entries=entries,Name=name)
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, description, text, date) values (?, ?, ?, ?)',
                 [request.form['title'],request.form['description'], request.form['text'],str(date)])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))
@app.route('/login/ok/<int:id>',methods=['POST'])
def ok(id):
    if session['logged_in'] == True:
        g.db.execute("UPDATE entries SET title = ?,description = ?,text=? WHERE id= ? ",[request.form['title'],request.form['description'],request.form['text'],id])
        g.db.commit()
        return redirect(url_for('index'))    
@app.route('/login/edite/<int:id>')
def edite(id):
    error= None
    if session['logged_in'] == True:
        cur = g.db.execute('select id, title, description, date, text from entries where id = {}'.format(id))
        a = cur.fetchall()
        id=str(id)
        entries = [dict(id=row[0],title=row[1], description=row[2],text=row[4]) for row in a]
        return render_template('edite.html',Name=name,entries=entries)
@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = g.db.execute('select id, title, description, date from entries order by id desc')
    a = cur.fetchall()
    entries = [dict(id=row[0],title=row[1], description=row[2],d=row[3]) for row in a]
    error = None
    response=make_response(render_template('login.html',error=error))
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.set_cookie('username', 'flask', secure=True, httponly=True)
    response.set_cookie('snakes', '3', max_age=600)
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return render_template('show_entries.html', error=error,entries=entries)
    return response

@app.route('/about')
def about():
    return render_template('about.html',Name=name)
@app.route('/contact')
def contact():
    return render_template('contact.html',Name=name)

@app.route('/posts/<int:id>')
def singlePost(id):
    cur = g.db.execute("select id,title, description, text, date from entries where id = %s" %id)
    a = cur.fetchall()
    entries = [dict(id=row[0],title=row[1], description=row[2], text=row[3],d=row[4]) for row in a]
    id=str(id)
    return render_template('post.html',entries=entries,Name=name)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
