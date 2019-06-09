import os
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
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


@app.route("/recipes/<recipe_id>")
def display_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    return render_template('recipe.html',
                            title='{0} | {1}'.format(page_title, recipe["name"]),
                            recipe=recipe)


@app.route("/recipes/add")
def add_recipe():
    return render_template('add_recepie.html',
                            title='%s | Add Recipes' % page_title)
                            
@app.route("/recepies/post", methods=["POST"])
def post_recipe():
    data_in = request.form.to_dict()
    data_out = {}
    # [ print(x, data_in[x]) for x in data_in ] ##print data for debuging
    
    ingredients = []
    steps = []

    for i in range(0,3):
        ingredient = {} 
        ingredient['ingredient_name']   = request.form['ingredient%s_name' % i]
        ingredient['ingredient_amount'] = request.form['ingredient%s_amount' % i]
        ingredient['ingredient_unit']   = request.form['ingredient%s_unit' % i]
        ingredients.append(ingredient)
        
    for step_no in range(1,4):
        steps.append(request.form['recipe_step_%s' % step_no])
            
    data_out['name']        = request.form['name']
    data_out['author']      = request.form['author']
    data_out['description'] = request.form['description']
    data_out['prep_time']   = request.form['prep_time']
    data_out['servings']    = request.form['servings']
    data_out['calories']    = request.form['calories']
    data_out['cuisine']     = request.form['cuisine']
    data_out['category']    = request.form['category']
    
    data_out['is_vegiterian']   = True if 'is_vegiterian'in request.form    else False
    data_out['has_lactose']     = True if 'has_lactose' in request.form     else False
    data_out['has_gluten']      = True if 'has_gluten' in request.form      else False
    
    #data_out[''] = request.form['']
    data_out['ingredients'] = ingredients
    data_out['preperation'] = steps
    
    # print("*****")
    # print("in", data_in)
    # print("*****")
    # print("out", data_out)
    # print("*****")
    
    mongo.db.recipes.insert_one(data_out)
    return redirect( url_for('recipes') )
    
    # {
    #     "_id":{"$oid":"5cf908061c9d4400000393cf"},
    #     "name":"Spaghetti Carbonara",
    #     "author":"jodoe",
    #     "prep_time":{"$numberInt":"40"},
    #     "servings":{"$numberInt":"8"},
    #     "calories":"400",
    #     "ingredients":[{"ingredient_name":"spaghetti","amount":"500","units":"g"}],
    #     "reviews":[{"name":"jdoe","rating":{"$numberInt":"5"},"description":"My favorite italian dish"},{"name":"tom","rating":{"$numberInt":"3"},"description":"Too little sause, otherwise good recepie."}],
    #     "picture":"carb.jpg",
    #     "preperation":["In a large pot of boiling salted water, cook spaghetti pasta until al dente. Drain well. Toss with 1 tablespoon of olive oil, and set aside. ","Meanwhile in a large skillet, cook chopped bacon until slightly crisp; remove and drain onto paper towels. Reserve 2 tablespoons of bacon fat; add remaining 1 tablespoon olive oil, and heat in reused large skillet. Add chopped onion, and cook over medium heat until onion is translucent. Add minced garlic, and cook 1 minute more. Add wine if desired; cook one more minute","Return cooked bacon to pan; add cooked and drained spaghetti. Toss to coat and heat through, adding more olive oil if it seems dry or is sticking together. Add beaten eggs and cook, tossing constantly with tongs or large fork until eggs are barely set. Quickly add 1/2 cup Parmesan cheese, and toss again. Add salt and pepper to taste (remember that bacon and Parmesan are very salty)","Serve immediately with chopped parsley sprinkled on top, and extra Parmesan cheese at table."],
    #     "description":"A super rich, classic 'bacon and egg' spaghetti dish. Great to serve for company. This recipe also makes an unusual brunch offering."
    # }

    


if __name__ == "__main__":    
    app.run(host=os.getenv('IP', '127.0.0.1'), 
            port=int(os.getenv('PORT', "5000")), 
            debug=True)