"""GPUman interface."""
import sys
import pdb
from flask import Flask, session, redirect, url_for, request, render_template, flash
from models import User, UsageRequest, Admin
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exists
from sqlalchemy.orm.exc import NoResultFound
from settings import DB_URL, Key
# from gevent.wsgi import WSGIServer

app = Flask(__name__)
app.secret_key = Key
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
db_session = Session()


@app.route('/')
def index():
    """Login/Dashboard."""
    if 'admin' in session:
        # Add admin Dashboard
        pass
    elif 'user' in session:
        # Add user Dashboard
        pass
    flash("Please login to continue")
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
    """Logout."""
    session.pop('user', None)
    session.pop('admin', None)
    flash("You have successfully logged out")
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = None
        # Check if user exists
        try:
            user = db_session.query(User).filter(User.username == username).one()
        except NoResultFound:
            flash("User does not exist")
            return redirect(url_for('login'))
        # Check the password
        if not user.validate_password(password):
            flash("Wrong password")
            return redirect(url_for('login'))
        # Login session
        session['user'] = user.id_
        # Check if user is admin
        if db_session.query(exists().where(Admin.user_id == user.id_)).scalar():
            session['admin'] = True
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        faculty = request.form["faculty"]
        if password != confirm_password:
            flash("Passwords don't match")
            return redirect(url_for('register'))
        if db_session.query(exists().where(User.username == username)).scalar():
            flash("User already exists")
            return redirect(url_for('register'))
        new_user = User(username, password, name, email, faculty)
        db_session.add(new_user)
        db_session.commit()
        flash("You have successfully registered, please login")
        return redirect(url_for('login'))


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage:\n\tpython app.py [host address] [port]\n")
        sys.exit(0)

    IP_addr = sys.argv[1]
    port = sys.argv[2]
    try:
        app.run(host=IP_addr, debug=True, port=int(port))
    # http_server = WSGIServer((IP_addr, int(port)), app)
    # print("Server running on http://{}:{}".format(IP_addr, port))
    # try:
    #     http_server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting server")
        sys.exit(0)
