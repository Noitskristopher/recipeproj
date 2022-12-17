from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, recipe
from datetime import datetime
dateFormat = "%m/%d/%Y"
dateAndTimeFormat = "%m/%d/%Y %I:%M %p"


@app.route('/recipes/new')
def create_recipe_page():
    if 'user_id' in session:
        return render_template('/recipes(create).html', current_user=user.User.getById({'id': session['user_id']}))
    return redirect('/')


@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' in session:
        if recipe.Recipe.validate_recipes(request.form):
            data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'instruction': request.form['instruction'],
                'datemade': request.form['datemade'],
                'underthirty': request.form['underthirty'],
                'user_id': session['user_id']
            }
            print(data)
            recipe.Recipe.save(data)
            return redirect('/recipes')
        return redirect('/recipes/new')
    return redirect('/')


@app.route('/recipes/<int:recipe_id>')
def show_one_recipe(recipe_id):
    return render_template('recipes(view).html', this_recipe=recipe.Recipe.get_one({'id': recipe_id}), all_recipe=recipe.Recipe.get_all_recipes_with_user(), current_user=user.User.getById({'id': session['user_id']}), dtf=dateFormat)


@app.route('/recipes/delete/<int:recipe_id>')
def delete(recipe_id):
    if 'user_id' in session:
        recipe.Recipe.delete({'id': recipe_id})
        return redirect('/recipes')
    return redirect('/')


@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' in session:
        return render_template('recipes(edit).html', thisRecipe=recipe.Recipe.getById({"id": recipe_id}))
    return redirect('/')


@app.route('/recipes/edited/<int:recipe_id>', methods=['POST'])
def edited_recipe(recipe_id):
    if 'user_id' in session:
        if recipe.Recipe.validate_recipes(request.form):
            data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'instruction': request.form['instruction'],
                'datemade': request.form['datemade'],
                'underthirty': request.form['underthirty'],
                'id': recipe_id
            }
            recipe.Recipe.edit(data)
            return redirect('/recipes')
        return redirect(f'/recipes/edit/{recipe_id}')
    return ('/')
