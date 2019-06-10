import os
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME', 'cookbook')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/cookbook')

mongo = PyMongo(app)

page_title = "Open Cookbook"

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
    return render_template('add_recipe.html',
                            title='%s | Add Recipe' % page_title)
                            
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
        ingredient['ingredient_name']   = request.form['ingredient%s_name' % i]
        ingredient['ingredient_amount'] = request.form['ingredient%s_amount' % i]
        ingredient['ingredient_unit']   = request.form['ingredient%s_unit' % i]
        ingredients.append(ingredient)
    
    steps_num = int( request.form['steps_counter'] )
    for step_no in range(1, steps_num + 1):
        steps.append(request.form['recipe_step_%s' % step_no])
            
    data_out['name']        = request.form['name']
    data_out['author']      = request.form['author']
    data_out['description'] = request.form['description']
    data_out['prep_time']   = request.form['prep_time']
    data_out['servings']    = request.form['servings']
    data_out['calories']    = request.form['calories']
    data_out['cuisine']     = request.form['cuisine']
    data_out['category']    = request.form['category']
    
    
    ## TODO - change to is_lactose_free and is_gluten_free ##
    data_out['is_vegiterian']   = True if 'is_vegiterian'in request.form    else False
    data_out['has_lactose']     = True if 'has_lactose' in request.form     else False
    data_out['has_gluten']      = True if 'has_gluten' in request.form      else False
    
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
    return render_template('recipe.html',
                            title='{0} | {1}'.format(page_title, recipe["name"]),
                            recipe=recipe)


if __name__ == "__main__":    
    app.run(host=os.environ.get('IP', '127.0.0.1'), 
            port=int(os.environ.get('PORT', 5000)), 
            debug=True)