from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, recipe
from datetime import datetime
dateFormat = "%m/%d/%Y %I:%M %p"


@app.route('/recipes')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', current_user=user.User.getById({'id': session['user_id']}), all_recipes=recipe.Recipe.get_all_recipes_with_user())
    return redirect('/')
