from flask import Flask, render_template, url_for, request,\
    flash, session, redirect, abort, g, make_response
import sqlite3
import os
#config
DATABASE = 'tmp/Flask.db'
DEBUG = True
SECRET_KEY = 'fdgdfgdfggf786hfg6hfg6h7f'


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "Flask.db")))


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def index():
    # db = get_db()
    return render_template('index.html', menu=menu)


@app.route("/login")
def loginn():
    log = ""
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')

    res = make_response(f"<h1>Authentication form</h1><p>Logged: {log}</p>")
    res.set_cookie("logged", "yes")
    return res


menu = [{'name': 'install', 'url': 'install-flask'},
        {'name': 'first app', 'url': 'first-app'},
        {'name': 'contact', 'url': 'contact'}]


# @app.route("/")
# def index():
#     print(url_for("index"))
#     return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    print(url_for("about"))
    return render_template('about.html', title='About this site', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"User: {username}"


@app.route("/contact", methods=['POST', 'GET'])
def contact():

    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash("successfully", category='success')
        else:
            flash("error", category='error')
    return render_template('contact.html', title='Contact', menu=menu)


@app.errorhandler(404)
def pagenotfound(error):
    return render_template('p404.html', title='Page not found', menu=menu)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'selfedu' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Authentication', menu=menu)


if __name__ == "__main__":
    app.run(debug=True)

# with app.test_request_context():
#     print(url_for("index"))
#     print(url_for("about"))
#     print(url_for("profile", username="selfedu"))