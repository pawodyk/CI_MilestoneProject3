import os
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME', 'cookbook')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/cookbook')

mongo = PyMongo(app)

page_title = "Open Cookbook"

units = ["g", "mg","kg","ml","l","t. spoon","tb. spoon","cup","glass","whole","half","quater","slice"]

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
    
    
    ## TODO - change to is_lactose_free and is_gluten_free ##
    data_out['is_vegiterian']   = True if 'is_vegiterian'in request.form    else False
    data_out['is_lactose_free']     = True if 'is_lactose_free' in request.form     else False
    data_out['is_gluten_free']      = True if 'is_gluten_free' in request.form      else False
    
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
    # cuisine_id = recipe['cuisine']
    
    # cuisine = mongo.db.cuisine.find_one({'_id':ObjectId(cuisine_id)})
    
    # recipe['cuisine_name'] = cuisine['cuisine_name']
    
    return render_template('recipe.html',
                            title='{0} | {1}'.format(page_title, recipe["name"]),
                            recipe=recipe)

@app.route("/recipes/<recipe_id>/edit")
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    return render_template('edit_recipe.html',
                            title='{0} | Editing: {1}'.format(page_title, recipe["name"]),
                            recipe=recipe,
                            units=units)
    

@app.route("/recipes/<recipe_id>/edit/post", methods=["POST"])
def edit_recipe_post():
    return 


if __name__ == "__main__":    
    app.run(host=os.environ.get('IP', '127.0.0.1'), 
            port=int(os.environ.get('PORT', 5000)), 
            debug=True)