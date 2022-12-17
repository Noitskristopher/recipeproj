from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
from datetime import datetime
bcrypt = Bcrypt(app)
dateFormat = "%m/%d/%Y %I:%M %p"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    # validate user input
    if user.User.validate_create(request.form):
        # user has unique email
        # secure the password via bcrypt
        # print(request.form['password'])
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        # if valid save to db
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        # store the user in session
        session['user_id'] = user.User.save(data)
        # redirect to /home or dashboard
        return redirect('/recipes')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = user.User.getByEmail(data)
    if user_in_db:
        # validate user input
        if bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            # store the user in session
            session['user_id'] = user_in_db.id
            # redirect to /home or dashboard
            return redirect("/recipes")
    flash("Invalid Credentials", 'loginError')
    return redirect('/')


@app.route('/logout')
def logout():
    # clear session
    session.clear()
    # redirect to root route
    return redirect('/')
