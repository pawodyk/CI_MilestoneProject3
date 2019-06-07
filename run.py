import os
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)



@app.route("/")
def home():
    return render_template('index.html', 
                            title="Open Cookbook")
    
@app.route("/recipes")
def recipes():
    # data = mongo.db.recipes.find()
    #print(data)
    #for item in data:
    #    print (item)
    return render_template('recipes.html', 
                            title="Open Cookbook | Recipes",
                            recipes_list=mongo.db.recipes.find())
                            

# recipe = mongo.db.recipes.find_one()
# cuisine_id = recipe.cuisine_id
# cuisine_name = mongo.db.cuisines.find_one(cuisine_id)
# new_recipes = []
# for recipe in recipes:
#     new_recipes.append(recipe)
#     recipe['cuisine_name'] = cuisine_name
#     recipe.cuisine_name



if __name__ == "__main__":    
    app.run(
        host=os.getenv('IP', '127.0.0.1'), 
        port=int(os.getenv('PORT', "5000")), 
        debug=True)