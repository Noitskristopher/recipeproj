from flask_app import app
import re
from flask_app.config.mysqlConnection import connectToMySQL
from flask import flash, session
from flask_app.models import user
mydb = 'recipes_schema'
# DATE_REGEX = re.compile(r'^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$')


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.datemade = data['datemade']
        self.underthirty = data['underthirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @staticmethod
    def validate_recipes(request):
        is_valid = True
        if len(request['name']) < 1 or len(request['description']) < 1 or len(request['instruction']) < 1 or len(request['datemade']) < 1 or 'underthirty' not in request:
            flash("All Fields Required", 'recipeError')
            is_valid = False
        if len(request['name']) <= 3:
            flash("Name Must Be Longer Than Three Characters", 'recipeError')
            is_valid = False
        if len(request['description']) <= 3:
            flash("Description Must Be Longer Than Three Characters", 'recipeError')
            is_valid = False
        if len(request['instruction']) <= 3:
            flash("Instruction Must Be Longer Than Three Characters", 'recipeError')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO recipes (name, description, instruction, datemade, underthirty, user_id, created_at, updated_at )
        VALUES (%(name)s, %(description)s, %(instruction)s, %(datemade)s, %(underthirty)s, %(user_id)s, NOW(), NOW());'''
        results = connectToMySQL(mydb).query_db(query, data)
        # print(f"results: {results}")
        return results

    @classmethod
    def get_all_recipes_with_user(cls):
        query = '''
        SELECT recipes.*, users.first_name
        FROM recipes
        JOIN users
        ON recipes.user_id = users.id;'''
        results = connectToMySQL(mydb).query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipe.creator = row['first_name']
            all_recipes.append(one_recipe)
        # print(f'allRecipes: {all_recipes}')
        return all_recipes

    @classmethod
    def get_one(cls, data):
        query = '''
        SELECT recipes.*, users.first_name
        FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        this_recipe = cls(results[0])
        # print(f"results: {this_recipe}")
        this_recipe.creator = results[0]['first_name']
        # print(f"results: {this_recipe.creator}")
        return this_recipe

    @classmethod
    def delete(cls, data):
        query = '''
        DELETE FROM recipes WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = '''
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, datemade = %(datemade)s, underthirty = %(underthirty)s
        WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)

    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(mydb).query_db(query, data)
        # print(f"results: {results}")
        return cls(results[0])
