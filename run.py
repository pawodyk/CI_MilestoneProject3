import os
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME', 'cookbook')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/cookbook')

mongo = PyMongo(app)

page_title = "Open Cookbook"

units = ["g", "mg","kg","ml","l","tsp","tbsp","cup","glass","whole","half","quater","slice"]

@app.route("/")
def home():
    return render_template('index.html', 
                            title=page_title)


@app.route("/recipes")
def recipes():
    return render_template('recipes.html', 
                            title='%s | Recipes' % page_title,
                            recipes_list=mongo.db.recipes.find())


@app.route("/recipes/add")
def add_recipe():
    categories = mongo.db.categories.find()
    cuisines = mongo.db.cuisines.find()
    return render_template('add_recipe.html',
                            title='%s | Add Recipe' % page_title,
                            cuisines=cuisines,
                            categories=categories,
                            units=units)


@app.route("/recepies/add/post", methods=["POST"])
def add_recipe_post():
    # data_in = request.form.to_dict()
    data_out = {}
    # [ print(x, data_in[x]) for x in data_in ] ##print data for debuging
    
    ingredients = []
    steps = []
    
    ingredients_num = int( request.form['ingredient_counter'] )
    for i in range(1, ingredients_num + 1):
        ingredient = {} 
        ingredient['ingredient_name']   = request.form['ingredient%s_name' % i].lower()
        ingredient['ingredient_amount'] = request.form['ingredient%s_amount' % i]
        ingredient['ingredient_unit']   = request.form['ingredient%s_unit' % i]
        ingredients.append(ingredient)
    
    steps_num = int( request.form['steps_counter'] )
    for step_no in range(1, steps_num + 1):
        steps.append(request.form['recipe_step_%s' % step_no])
            
    data_out['name']        = request.form['name'].title()
    data_out['author']      = request.form['author'].title()
    data_out['description'] = request.form['description'].capitalize()
    data_out['prep_time']   = request.form['prep_time']
    data_out['servings']    = request.form['servings']
    data_out['calories']    = request.form['calories']
    data_out['cuisine']     = request.form['cuisine']
    data_out['category']    = request.form['category']
    
    data_out['is_vegiterian']   = True if 'is_vegiterian'in request.form    else False
    data_out['is_lactose_free'] = True if 'is_lactose_free' in request.form else False
    data_out['is_gluten_free']  = True if 'is_gluten_free' in request.form  else False
    
    #data_out[''] = request.form['']
    data_out['ingredients'] = ingredients
    data_out['preperation'] = steps
    
    data_out['picture'] = "default.jpg"
    
    # print("*****")
    # print("in", data_in)
    # print("*****")
    # print("out", data_out)
    # print("*****")
    
    mongo.db.recipes.insert_one(data_out)
    return redirect( url_for('recipes') )
    

@app.route("/recipes/<recipe_id>")
def display_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    cuisine_id = recipe['cuisine']
    category_id = recipe['category']
    
    
    cuisine = mongo.db.cuisines.find_one({'_id':ObjectId(cuisine_id)})
    category = mongo.db.categories.find_one({'_id':ObjectId(category_id)})
    
    recipe['cuisine_name'] = cuisine['name']
    recipe['category_name'] = category['name']
    
    return render_template('recipe.html',
                            title='{0} | {1}'.format(page_title, recipe["name"]),
                            is_owner = True, ## in the future to be used to verify the user, currentlly set to accept all users
                            recipe=recipe)


@app.route("/recipes/<recipe_id>/review/post", methods=["POST"])
def review_recipe_post(recipe_id):
    review = request.form.to_dict()
    
    mongo.db.recipes.update_one(
        {'_id': ObjectId(recipe_id)},
        {
            '$push': { 
                'reviews': review
            }
        }
    )
    return redirect(url_for('display_recipe', recipe_id=recipe_id))
    


@app.route("/recipes/<recipe_id>/edit")
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    categories = mongo.db.categories.find()
    cuisines = mongo.db.cuisines.find()
    return render_template('edit_recipe.html',
                            title='{0} | Editing: {1}'.format(page_title, recipe["name"]),
                            units=units,
                            recipe=recipe,
                            categories=categories,
                            cuisines=cuisines)
    

@app.route("/recipes/<recipe_id>/edit/post", methods=["POST"])
def edit_recipe_post(recipe_id):
    
    ingredients = []
    steps = []
    
    ingredients_num = int( request.form['ingredient_counter'] )
    for i in range(1, ingredients_num + 1):
        ingredient = {} 
        ingredient['ingredient_name']   = request.form['ingredient%s_name' % i]
        ingredient['ingredient_amount'] = request.form['ingredient%s_amount' % i]
        ingredient['ingredient_unit']   = request.form['ingredient%s_unit' % i]
        ingredients.append(ingredient)
    
    steps_num = int( request.form['steps_counter'] )
    for step_no in range(1, steps_num + 1):
        steps.append(request.form['recipe_step_%s' % step_no])
    
    mongo.db.recipes.update_one(
        {'_id': ObjectId(recipe_id)},
        {
            '$set': {
                'name': request.form.get('name'),
                'author': request.form.get('author'),
                'description': request.form.get('description'),
                'prep_time': request.form.get('prep_time'),
                'servings': request.form.get('servings'),
                'calories': request.form.get('calories'),
                'cuisine': request.form.get('cuisine'),
                'category': request.form.get('category'),
                'is_vegiterian':    True if 'is_vegiterian'in request.form    else False,
                'is_lactose_free':  True if 'is_lactose_free' in request.form else False,
                'is_gluten_free':   True if 'is_gluten_free' in request.form  else False,
                'ingredients': ingredients,
                'preperation': steps
            }
        }
    )
    
    return redirect(url_for('display_recipe', recipe_id=recipe_id))


@app.route("/recipes/<recipe_id>/confirm-deletion")
def delete_recipe(recipe_id):
    return render_template('delete_recipe.html', 
                            recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)}))


@app.route("/recipes/<recipe_id>/deleted")
def delete_recipe_confirmed(recipe_id):
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return redirect(url_for('recipes'))
    

if __name__ == "__main__":    
    app.run(host=os.environ.get('IP', '127.0.0.1'), 
            port=int(os.environ.get('PORT', 5000)), 
            debug=True)