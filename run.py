import os

from datetime import datetime as dt
from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename


"""APPLICATION CONFIGURATATION AND INITIALIZATION"""
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME', 'cookbook')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/cookbook')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './/static//img')
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 ## since i do not use any compression I decided to decrease the aceptable image size to 0.5 Mb
app.secret_key = os.getenv("SECRET_KEY", "fallbacksecretvalue123")

mongo = PyMongo(app)


"""GLOBAL VARIABLES"""
page_title = os.getenv("PAGE_TITLE", "Open Cookbook") ## defines the title of the page
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png']) ## defines extensions that are permited
dashboard_display_limit = 6 ## determines how many recipes are displayed in each section on the dashboard

units = ["g", "mg","kg","ml","l","tsp","tbsp","cup","glass","whole","half","quater","slice"]
# aceptable_sort_types = ['newest', 'oldest', 'views', 'revies', 'score']


"""HELPER METHODS"""
"""code from flask deocumentation responsible for ensuring that files upladed by the user are only in the allowed format"""
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""helper method returns the infomation needed to for the pymongo sort query"""
def sort_method(sort):
    
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
            
    return [sort_type, sort_order]


"""GENERAL WEBSITE FUNCTIONS"""
"""inject the data needed by the base, edit_recipe and add_recipe template"""
@app.context_processor
def inject_categories():
    """upload categories so they can be used the templates"""
    categories_list = [category for category in mongo.db.categories.find()]
    return dict(categories_all=categories_list)
    
@app.context_processor
def inject_cuisnes():
    """upload cuisines so they can be used the templates"""
    cuisines_list = [cuisine for cuisine in mongo.db.cuisines.find()]
    return dict(cuisines_all=cuisines_list)


"""render home page, set up the data used in the carauses and dashboard generation"""
@app.route("/")
def home():
    ### pull the top 5 recipes to display in the carusel 
    top_recipes = [recipe for recipe in mongo.db.recipes.find().sort([('reviews.score', -1), ('views', -1)]).limit(5)]
    
    ## create lists for categories and cuisines
    categories = [category for category in mongo.db.categories.find()]
    cuisines = [cuisine for cuisine in mongo.db.cuisines.find()]
    
    dashboard_list = []
    categories_list = []
    cuisines_list = []
    requirements_list = []
    
    dashboard_list.append({'id': 'categories', 'heading': 'Categories', 'search_key': 'category', 'list': categories})
    dashboard_list.append({'id': 'cuisines','heading': 'Cuisines', 'search_key': 'cuisine', 'list': cuisines})
    
    
    for outer in dashboard_list:
        items_list = []
        for inner in outer['list']:
            item_name = inner['name']
            item_id = inner['_id']
            item_url = "/recipes/filterby/{0}/{1}".format(outer['search_key'], item_id)
            
            recipes_list = [ recipe for recipe in mongo.db.recipes.find( 
                {outer['search_key']: str(item_id)},                           
                {'name', 'author', 'description', 'picture', '_id', 'views'}    ##extracts only values that are needed by the dashboard
            )
            .sort('views', -1)                                                  ## sorts the recipes by views
            .limit(dashboard_display_limit) ]                                   ## limit the number of recipes to be displyed
            
            
            recipes_count = mongo.db.recipes.find( {outer['search_key']: str(item_id)} ).count() ## counts total number of recipes
            
            items_list.append( {'id': item_id, 'name': item_name, 'url': item_url, 'recipes': recipes_list, 'total_recipes': recipes_count} )
            
        outer['list'] = items_list ## change the list to updated data list
            
    
        
    vegiterian = [ r for r in mongo.db.recipes.find({'is_vegiterian': True}, {'name', 'author', 'description', 'picture', '_id', 'views'}).sort('views', -1).limit(dashboard_display_limit) ]
    lactosefree = [ r for r in mongo.db.recipes.find({'is_lactose_free': True}, {'name', 'author', 'description', 'picture', '_id', 'views'}).sort('views', -1).limit(dashboard_display_limit) ]
    glutenfree = [ r for r in mongo.db.recipes.find({'is_gluten_free': True}, {'name', 'author', 'description', 'picture', '_id', 'views'}).sort('views', -1).limit(dashboard_display_limit) ]
    
    requirements_list.append({'name': 'Vegiterian', 'recipes': vegiterian})
    requirements_list.append({'name': 'Lactose Free', 'recipes': lactosefree})
    requirements_list.append({'name': 'Gluten Free', 'recipes': glutenfree})
    
    dashboard_list.append({'heading': 'Diatary Requirements and Food Allergies', 'list': requirements_list})
    
    return render_template('index.html', 
                            title=page_title,
                            top_recipes=top_recipes,
                            dashboard=dashboard_list)


"""renders the list of all the recipes"""
@app.route("/recipes")
def recipes():
    sort = sort_method(request.args.get('sort', ' views'))
    
    recipes = mongo.db.recipes.find().sort(sort[0], sort[1])
    recipes_list = [recipe for recipe in recipes]
    
    return render_template('recipes.html', 
                            title='%s | Recipes' % page_title,
                            recipes_list=recipes_list)
                            

"""renders the list of recipes filtered by the category"""
@app.route("/recipes/filterby/category/<category_id>")
def recipes_by_category(category_id):
    sort = sort_method(request.args.get('sort', ' views'))
    
    recipes = mongo.db.recipes.find({'category': category_id}).sort(sort[0], sort[1])
    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    category_name = category['name']
    
    recipes_list = [recipe for recipe in recipes]
    
    return render_template('recipes.html', 
                            title='{0} | Recipes for {1}'.format(page_title, category_name),
                            category_name=category_name,
                            recipes_list= recipes_list)


"""renders the list of recipes filtered by the cuisine"""
@app.route("/recipes/filterby/cuisine/<cuisine_id>")
def recipes_by_cuisine(cuisine_id):
    sort = sort_method(request.args.get('sort', ' views'))
    
    recipes = mongo.db.recipes.find({'cuisine': cuisine_id}).sort(sort[0], sort[1])
    cuisine = mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)})
    cuisine_name = cuisine['name']
    
    recipes_list = [recipe for recipe in recipes]
    
    return render_template('recipes.html', 
                            title='{0} | Recipes from {1} Cuisine'.format(page_title, cuisine_name),
                            cuisine_name=cuisine_name,
                            recipes_list=recipes_list)


"""takes the query data for search and pass it to search function"""
@app.route("/recipes/search/post", methods=["POST"])
def search_post():
    query = request.form['query'].lower()
    
    return redirect(url_for('search', query=query))


"""completes the search opperation and renders search results"""
@app.route("/recipes/search/<query>")
def search(query):
    sort = sort_method(request.args.get('sort', ' views'))
    
    results = []
    
    search_list = mongo.db.recipes.find().sort(sort[0], sort[1])
    
    #checks is the query in the following fileds: name, description, author
    for item in search_list:
        found = False
        for key, value in item.items():
            if key == 'name'or key == 'description' or key == 'author':
                if value.lower().find(query) > -1:
                    found = True
        
        #if data was found it is appended to the results list
        if found:
            results.append(item)
    
    return render_template('recipes.html',
                            title='%s | Search Results' % page_title,
                            recipes_list=results)


"""renders the teplate for adding the recipe"""
@app.route("/recipes/add")
def add_recipe():

    return render_template('add_recipe.html',
                            title='%s | Add Recipe' % page_title,
                            units=units)


"""handles the data passed from the form in add_recipe page
    very important function as it is responsible for seting up a schema structure
    and ensuring the data is in the correct fields"""
@app.route("/recepies/add/post", methods=["POST"])
def add_recipe_post():
    
    ### declaring empty containers to hold a data
    data_out = {}
    ingredients = []
    steps = []
    
    ### handles itteration throug all the ingrediants,
    ### the ingrediendt are dynamicly added to the page so the total number of ingredients is not hard coded
    ### the data is then added to the directory so it could be added to mongodb as a bson object
    ingredients_num = int( request.form['ingredient_counter'] )
    for i in range(1, ingredients_num + 1):
        ingredient = {} 
        ingredient['ingredient_name']   = request.form['ingredient%s_name' % i].lower()
        ingredient['ingredient_amount'] = request.form['ingredient%s_amount' % i]
        ingredient['ingredient_unit']   = request.form['ingredient%s_unit' % i]
        ingredients.append(ingredient)
    
    ### handles itteration throug all the steps,
    ### similarlly to ingredients the steps are dynamicly added
    ### but since the data structure is an array the information is just appended to the list
    steps_num = int( request.form['steps_counter'] )
    for step_no in range(1, steps_num + 1):
        steps.append(request.form['recipe_step_%s' % step_no])
    
    ### handles the data assignment to the appropriate fields
    ### for simplicity the form input names match the database fields names
    data_out['name']        = request.form['name'].title()
    data_out['author']      = request.form['author'].title()
    data_out['description'] = request.form['description'].capitalize()
    data_out['prep_time']   = request.form['prep_time']
    data_out['servings']    = request.form['servings']
    data_out['calories']    = request.form['calories']
    data_out['cuisine']     = request.form['cuisine']
    data_out['category']    = request.form['category']
    
    ### extract and assignes data from checkboxes
    data_out['is_vegiterian']   = True if 'is_vegiterian'in request.form    else False
    data_out['is_lactose_free'] = True if 'is_lactose_free' in request.form else False
    data_out['is_gluten_free']  = True if 'is_gluten_free' in request.form  else False
    
    ### adds the data structures for ingredients and steps to the appropraitate fields
    data_out['ingredients'] = ingredients
    data_out['preperation'] = steps
    
    ### set up other fields that are not set by the form but are important for data cohesion
    data_out['views'] = 0
    data_out['created_on'] = dt.utcnow()
    data_out['reviews'] = {'avg_score': 0, 'total_number': 0, 'reviews': []}
    

    """sample file upload taken from the flask documentation and modified"""
    # check if the post request has the file part
    if 'file' not in request.files:
        print('###','No file part','###')
        data_out['picture'] = 'default.jpg'
    else:    
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('###','No selected file','###')
            data_out['picture'] = 'default.jpg'
            
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data_out['picture'] = file.filename
    
    ### inserts data to the mongo database and redirects user to the list of recipes
    mongo.db.recipes.insert_one(data_out)
    return redirect( url_for('recipes') )
    

"""handles all the data used to render the template for each recipe"""
@app.route("/recipe/<recipe_id>")
def display_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    cuisine_id = recipe['cuisine']
    category_id = recipe['category']
    
    
    cuisine = mongo.db.cuisines.find_one({'_id':ObjectId(cuisine_id)}, {'name'})
    category = mongo.db.categories.find_one({'_id':ObjectId(category_id)}, {'name'})
    
    ### for simplicity the cuisine name and category name are directlly inserted into recipe list
    recipe['cuisine_name'] = cuisine['name']
    recipe['category_name'] = category['name']
    
    timestamp = recipe['created_on']
    recipe['created_on_str'] = timestamp.strftime('%d/%m/%Y')
    
    ### modified_on is not a mandatory field so i check for its existance
    if 'modified_on' in recipe:
        timestamp = recipe['modified_on']
        recipe['modified_on_str'] = timestamp.strftime('%d/%m/%Y') #('%d/%m/%Y %H:%M')
    
    """ Simple proces for verifing that this is an unique visit in this session """
    if not session: 
        session['viewed'] = []
    
    if recipe_id not in session['viewed']:
        li = session['viewed']
        li.append(recipe_id)
        session['viewed'] = li
        mongo.db.recipes.update_one(
            { '_id': ObjectId(recipe_id)},
            { '$inc': { 'views': 1 } }
        )
        recipe['views'] += 1 # append the views in the list so the user sees that his visit is included in the views important for the newly added recipes
    
    
    return render_template('recipe.html',
                            title='{0} | {1}'.format(page_title, recipe["name"]),
                            is_owner = True, ## in the future to be used to verify the user, currentlly set to allow all users edit privelages, to prevent edits set to False
                            recipe=recipe)

"""handles the process of posting the review"""
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
                'reviews.reviews': review ##push the review to the list
            }
        }
    )
    
    return redirect(url_for('display_recipe', recipe_id=recipe_id))
    

"""renders the page for edit_recipe"""
@app.route("/recipe/<recipe_id>/edit")
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})

    return render_template('edit_recipe.html',
                            title='{0} | Editing: {1}'.format(page_title, recipe["name"]),
                            units=units,
                            recipe=recipe)
    
    
"""handles the data provided by the user in edit recipe fileds"""
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


"""renders the confirmation page for delation operation"""
@app.route("/recipe/<recipe_id>/confirm-deletion")
def delete_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    cuisine_id = recipe['cuisine']
    category_id = recipe['category']
    
    cuisine = mongo.db.cuisines.find_one({'_id':ObjectId(cuisine_id)}, {'name'})
    category = mongo.db.categories.find_one({'_id':ObjectId(category_id)}, {'name'})
    
    recipe['cuisine_name'] = cuisine['name']
    recipe['category_name'] = category['name']
    
    return render_template('delete_recipe.html', 
                            recipe=recipe)


"""sends the delate operation to the server"""
@app.route("/recipe/<recipe_id>/deleted")
def delete_recipe_confirmed(recipe_id):
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return redirect(url_for('recipes'))
    


"""MAIN FUNCTION"""
if __name__ == "__main__": 
    app.run(host=os.environ.get('IP', '127.0.0.1'), 
            port=int(os.environ.get('PORT', 5000)), 
            debug=True)