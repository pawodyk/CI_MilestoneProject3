import os

from datetime import datetime as dt
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME', 'cookbook')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/cookbook')
app.secret_key = os.getenv("SECRET_KEY", "fallbacksecretvalue123")


mongo = PyMongo(app)

page_title = os.getenv("PAGE_TITLE", "Open Cookbook")

units = ["g", "mg","kg","ml","l","tsp","tbsp","cup","glass","whole","half","quater","slice"]
# aceptable_sort_types = ['newest', 'oldest', 'views', 'revies', 'score']



@app.context_processor
def inject_categories():
    categories_mongo = mongo.db.categories.find()
    
    return dict(categories_list=categories_mongo)
    
@app.context_processor
def inject_cuisne():
    cuisines_mongo = mongo.db.cuisines.find()

    return dict(cuisines_list=cuisines_mongo)



@app.route("/")
def home():
    top_recipes = [recipe for recipe in mongo.db.recipes.find().sort('views', -1).limit(5)]
    
    display_limit = 6
    
    categories = mongo.db.categories.find()
    cuisines = mongo.db.cuisines.find()
    
    categories_list = []
    cuisines_list = []
    requirements_list = []
    
    for category in categories:
        category_name = category['name']
        category_id = category['_id']
        
        recipes_list = [ r for r in mongo.db.recipes.find({'category': str(category_id)}, {'name', 'author', 'description', 'picture', '_id', 'views'}).sort('views', -1).limit(display_limit) ]
        recipes_count = mongo.db.recipes.find({'category': str(category_id)}).count()
        
        categories_list.append({'id': category_id, 'name': category['name'], 'recipes': recipes_list, 'total_recipes': recipes_count})
        
    for cuisine in cuisines:
        cuisine_name = cuisine['name']
        cuisine_id = cuisine['_id']
        
        recipes_list = [ r for r in mongo.db.recipes.find({'cuisine': str(cuisine_id)}, {'name', 'author', 'description', 'picture', '_id', 'views'}).sort('views', -1).limit(display_limit) ]
        recipes_count = mongo.db.recipes.find({'cuisine': str(cuisine_id)}).count()
        
        cuisines_list.append({'id': cuisine_id, 'name': cuisine['name'], 'recipes': recipes_list, 'total_recipes': recipes_count})
        
    vegiterian = [ r for r in mongo.db.recipes.find({'is_vegiterian': True}, {'name', 'author', 'description', 'picture', '_id', 'views'}).sort('views', -1).limit(display_limit) ]
    lactosefree = [ r for r in mongo.db.recipes.find({'is_lactose_free': True}, {'name', 'author', 'description', 'picture', '_id', 'views'}).sort('views', -1).limit(display_limit) ]
    glutenfree = [ r for r in mongo.db.recipes.find({'is_gluten_free': True}, {'name', 'author', 'description', 'picture', '_id', 'views'}).sort('views', -1).limit(display_limit) ]
    
    requirements_list.append({'name': 'Vegiterian', 'recipes': vegiterian})
    requirements_list.append({'name': 'Lactose Free', 'recipes': lactosefree})
    requirements_list.append({'name': 'Gluten Free', 'recipes': glutenfree})
    
    return render_template('index.html', 
                            title=page_title,
                            top_recipes=top_recipes,
                            categories=categories_list,
                            cuisines=cuisines_list,
                            requirements=requirements_list)


@app.route("/recipes")
def recipes():
    sort = request.args.get('sort', ' views')
    print(sort)
    
    sort_type = 'views'
    sort_order = -1
    if sort != 'views':
        if sort == 'new':
            sort_type = 'created_on'
            sort_order = -1
        elif sort == 'old':
            sort_type = 'created_on'
            sort_order = 1
        elif sort == 'review':
            sort_type = 'reviews.total_number'
            sort_order = -1
        elif sort == 'score':
            sort_type = 'reviews.avg_score'
            sort_order = -1
    
    recipes = mongo.db.recipes.find().sort(sort_type, sort_order)
    recipes_list = [recipe for recipe in recipes]
    
    for recipe in recipes_list:
        print(recipe['name'], recipe['reviews']['total_number'], recipe['reviews']['avg_score'])
    
    return render_template('recipes.html', 
                            title='%s | Recipes' % page_title,
                            recipes_list=recipes_list)
                            
                            
@app.route("/recipes/filterby/category/<category_id>")
def recipes_by_category(category_id):
    recipes = mongo.db.recipes.find({'category': category_id})
    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    category_name = category['name']
    
    recipes_list = [recipe for recipe in recipes]
    
    return render_template('recipes.html', 
                            title='{0} | Recipes for {1}'.format(page_title, category_name),
                            category_name=category_name,
                            recipes_list= recipes_list)


@app.route("/recipes/filterby/cuisine/<cuisine_id>")
def recipes_by_cuisine(cuisine_id):
    recipes = mongo.db.recipes.find({'cuisine': cuisine_id})
    cuisine = mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)})
    cuisine_name = cuisine['name']
    
    recipes_list = [recipe for recipe in recipes]
    
    return render_template('recipes.html', 
                            title='{0} | Recipes from {1} Cuisine'.format(page_title, cuisine_name),
                            cuisine_name=cuisine_name,
                            recipes_list=recipes_list)


app.route("/recipes/filterby/cuisine/<cuisine_id>")
def recipes_by_cuisine(cuisine_id):
    recipes = mongo.db.recipes.find({'cuisine': cuisine_id})
    cuisine = mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)})
    cuisine_name = cuisine['name']
    
    print(sort_method)
    
    recipes_list = [recipe for recipe in recipes]
    
    return render_template('recipes.html', 
                            title='{0} | Recipes from {1} Cuisine'.format(page_title, cuisine_name),
                            cuisine_name=cuisine_name,
                            recipes_list=recipes_list)

@app.route("/recipes/search", methods=["GET", "POST"])
def search_post():
    results = []
    query = request.form['query'].lower()
    
    search_list = mongo.db.recipes.find({}, {'_id' ,'name', 'description', 'author', 'picture'})
    
    for item in search_list:
        found = False
        for key, value in item.items():
            if key == 'name'or key == 'description' or key == 'author':
                if value.lower().find(query) > -1:
                    found = True
        
        if found:
            results.append(item)
    
    return render_template('recipes.html',
                            title='%s | Search Results' % page_title,
                            recipes_list=results)


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
    
    
    data_out['views'] = 0
    data_out['created_on'] = dt.utcnow()
    data_out['reviews'] = {'avg_score': 0, 'total_number': 0, 'reviews': []}
    
    data_out['picture'] = "default.jpg"
    
    # print("*****")
    # print("in", data_in)
    # print("*****")
    # print("out", data_out)
    # print("*****")
    
    mongo.db.recipes.insert_one(data_out)
    return redirect( url_for('recipes') )
    

@app.route("/recipe/<recipe_id>")
def display_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    cuisine_id = recipe['cuisine']
    category_id = recipe['category']
    
    
    cuisine = mongo.db.cuisines.find_one({'_id':ObjectId(cuisine_id)})
    category = mongo.db.categories.find_one({'_id':ObjectId(category_id)})
    
    recipe['cuisine_name'] = cuisine['name']
    recipe['category_name'] = category['name']
    
    timestamp = recipe['created_on']
    recipe['created_on_str'] = timestamp.strftime('%m/%d/%Y')
        
    if 'modified_on' in recipe:
        timestamp = recipe['modified_on']
        recipe['modified_on_str'] = timestamp.strftime('%m/%d/%Y') #('%m/%d/%Y %H:%M')
    
    """ Simple proces for verifing that this is an unique visit in this session """
    if not session: 
        session['viewed'] = []
    
    if recipe_id not in session['viewed']:
        li = session['viewed']
        li.append(recipe_id)
        session['viewed'] = li
        mongo.db.recipes.update(
            { '_id': ObjectId(recipe_id)},
            { '$inc': { 'views': 1 } }
        )
        recipe['views'] += 1
    
    return render_template('recipe.html',
                            title='{0} | {1}'.format(page_title, recipe["name"]),
                            is_owner = True, ## in the future to be used to verify the user, currentlly set to allow all users edit privelages
                            recipe=recipe)


@app.route("/recipe/<recipe_id>/review/post", methods=["POST"])
def review_recipe_post(recipe_id):
    review = request.form.to_dict()
    review['date'] = dt.utcnow()
    
    
    all_reviews = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}, {'reviews'})
    
    
    size = len(all_reviews['reviews']['reviews']) + 1
    score = 0
    for review in all_reviews['reviews']['reviews']:
        score += int(review['rating'])
        
    score = (score + int(review['rating'])) // size
    
    
    
    mongo.db.recipes.update_one(
        {'_id': ObjectId(recipe_id)},
        {
            '$set': {
                'reviews.avg_score': score,
                'reviews.total_number': size  
            },
                
            '$push': { 
                'reviews.reviews': review
            }
        }
    )
    return redirect(url_for('display_recipe', recipe_id=recipe_id))
    


@app.route("/recipe/<recipe_id>/edit")
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
    

@app.route("/recipe/<recipe_id>/edit/post", methods=["POST"])
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
            },
            '$currentDate': {
                'modified_on': { '$type': 'date' }
            }
        }
    )
    
    return redirect(url_for('display_recipe', recipe_id=recipe_id))


@app.route("/recipe/<recipe_id>/confirm-deletion")
def delete_recipe(recipe_id):
    return render_template('delete_recipe.html', 
                            recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)}))


@app.route("/recipe/<recipe_id>/deleted")
def delete_recipe_confirmed(recipe_id):
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return redirect(url_for('recipes'))
    

if __name__ == "__main__": 
    app.run(host=os.environ.get('IP', '127.0.0.1'), 
            port=int(os.environ.get('PORT', 5000)), 
            debug=True)