# Milestone Project 3 - ***Open Cookbook***

**By Pawel Wodyk**

<hr>

***Open Cookbook*** is a data-driven web application, designed to allow user to freely access and store recipes online. It provides clean and consistent design allowing user to easily navigate the website and access all of its functionality.  

The site uses the python flask framework and heavy relies on flask templating system. All the data on the site is pulled from MongoDB database and rendered using templates and jinja. Pictures are stored directly on the server to ensure they are always available[*](#hrokufilesystem). Styling of the website was  

Note: ***The Recipes added to the database are for demonstrational purposes only***. 
Please note that recipes could have missing ingredients or steps, and keep in mind that some data was modified during testing, especially the **food allergies**  **DO NOT** contain actual food allergies information.

Images for the recipes do not represent the recipes and are also only for a demonstrational purposes

Links to full recipes are available in [Resources Used and Credits](#credits) section 

### Status: [DEPLOYED on *heroku*](http://open-cookbook-milestone.herokuapp.com/)

<hr>

## Database Schema

```
recipes : Collection
__
  |
  |
  |__ _id : ObjectId              ## Primary Key
  |
  |__ name : String
  |
  |__ author : String
  |
  |__ description : String
  |
  |__ *cuisine : String           ## foreign key
  |
  |__ *category : String          ## foreign key
  |
  |__ prep_time : String
  |
  |__ servings : String
  |
  |__ calories : String
  |
  |__ is_vegiterian : Boolean
  |
  |__ is_lactose_free : Boolean
  |
  |__ is_gluten_free : Boolean
  |
  |__ ingredients : Array
  |  |
  |  |__ [n] : Object
  |     |
  |     |__ ingredient_name : String
  |     |__ ingredient_amount : String
  |     |__ ingredient_unit : String
  |
  |__ preperation : Array
  |  |
  |  |__ [n] : String
  |
  |__ picture : String
  |
  |__ reviews : Object
  |  |
  |  |__ avg_score : Integer
  |  |__ total_score : Integer
  |  |__ reviews : Array
  |     |
  |     |__ [n] : Object
  |        |
  |        |__ name : String
  |        |__ date : Date
  |        |__ rating : String
  |        |__ description : String
  |
  |__ views : Integer
  |
  |__ created_on : Date
  |
  |__ ( modified_on : Date )      ## Not enforced by program


categories : Collection
__
  |
  |__ _id : ObjectId            ## Primary Key
  |
  |__ name : String


cuisines : Collection
__
  |
  |__ _id : ObjectId            ## Primary Key
  |
  |__ name : String


         _______________________________________
        |             ~ Legend ~                |
        |                                       |
        |       |__ name : String               |
        |           ^key    ^ Value type        |
        |                                       |
        |       ##  - comments                  |
        |       [n] - index value               |
        |       ()  - optional fields           |
        |_______________________________________|

```

<hr>

## UX

The ***Open Cookbook*** page was designed to be minimalistic and intuitive to navigate page that, at the same time, provide the user with visually appealing elements to increase the feeling of hunger just by browsing through the page. For this reason I decided to make the page relay heavy on the photos of the food. Each recipe is represented by the photo that is the main focus on each of the pages.

The user is welcomed on the *home page* by the carousel of 5 most viewed recipes on the site. The carousel is designed to be the main part of the page and scale with the screen size. On the *recipes page* the user see the list of all recipes with a short summary of the recipe details consisting of recipe's name, author and description. With the main focus on the background image of each recipe. When clicked on any of the recipes the user is taken to the detailed view on which the main focus is the recipe photo near the top of the screen and the detailed information on the recipe just below that. The *recipe page* pattern is replicated on *delate recipe page* and *edit recipe page*, to give all pages unified and coherent look. Especially on the *edit recipe page* where, with few exceptions, I made each field match the data on the *recipe page*. The only page that do not feature any image is *add recipe page* since no image is loaded yet.

I decided to place the dashboard on the home page to allow users to view top recipes in each category in the clear and easy manner. Also if they are interested in more recipes they can see how many recipes in total are available, and go directly to the filtered view of the given category.

### Responsive Design

Each page is responsive, utilizing the bootstrap rows and columns to space the items as well as CSS3 Flex Layout.

The carousel on the home page has set max-height on bigger screen sizes which could prove to be problematic on the newer formats like 4K or ultra wide displays. Also the carouses hight on mobile phones has default bootstrap setting of dynamic height which I decided to leave since fully utilize all the limited space on the mobile devices.

### User stories

This website was designed with this Users in mind:

### UX Design Documentation:

1. I want to find something new to cook 
    - site feature easy to navigate and access recipes.
    - the detailed recipe view provides all the necessary information to prepare desired meal.
    - The most recommended recipes are featured on the home page and in the dashboard so you can view them directly from the home page.
    - the site provide the review option for the users to share they thoughts and options on the particular recipe.

2. I am looking for a recipe I can prepare for Family Dinner, preferably something Italian or Mediterranean
    - each group and cuisine has its dedicated and easily accessible views from the menu bar at the top of the page or from the dashboard on the home page.
    - The site also allows user to use sort and search features assist them with finding recipes they need.

3. I want to share my recipes with the world
    - the site allows users to upload their recipes on the website and store it in the database. 
    - You can read all the reviews at the bottom of each of your recipes to see how people like your recipe.
    - You can also use search feature to search for your name to see all your recipes and sort them by reviews, score or views to see how well are they doing.
    - If your recipe become very popular with the users you will see it on the

<hr>

## Features

### Existing Features

- **Feature 1** - Page is fully Data Driven and dynamic - all the recipes that are added to the database will be instantly available to all users.

- **Feature 2** - Carousel on the home page shows the filtered view of the top recipes.  Top recipes are determined by the average score (descending) and by secondary sorting parameter of views (descending).

- **Feature 3** - Dashboard on the home page provide the list of all top recipes in their group, with the link to filtered view of all recipes in the given group. The amount of displayed recipes per dashboard group has been limited to prevent long loading time of the home page.

- **Feature 4** - Users can access filtered view for each category and cuisine from each page via drop down menus on the navigation bar or from the home page via dashboard.

- **Feature 5** - Recipes page and all pages that use its template (i.e. both filtered pages and search results page) allow user to sort the viewed recipes by:
    - most views
    - newest
    - oldest
    - most reviewed
    - best score

- **Feature 6** - User can search for the recipes using the search input on the navigation bar. The searched fields are *recipe.name*, *recipe.author*, and *recipe.description*.

    The program uses the python code to search for the keyword, after data is pulled in full form the database instead of providing the searched keyword in the mongo command. This is done on purpose to allow searching for only one word, or sequence of characters within each field. This gives user more flexibility.   

- **Feature 7** - Add recipe page allows user to add the recipe to the database and store its image on the server. 

- **Feature 8** - Each page have detailed view that shows all the information provided by the user as well as some information generated by the program like creation and edition date, and the data generated by other users like reviews and number of views.

- **Feature 9** - Each recipe could be edited and all the data provided in the process of adding the recipe can be modified and updated.

- **Feature 10** - User can also choose to delete the recipe from database from the recipe view page. Before the deletion request to the database the user is shown the recipe again and prompted to confirm the deletion.

- **Feature 11** - The user can upload image file of the recipe as long as it is under 512Kb.

### Features Left to Implement

- **User Veryfication** - at this moment the site do not provide any form of identification. This may be problematic as each user can edit and delate every single recipe. The basis for verifying the user are implemented on the recipe page but at this time always return `True`.

- **Compressing uploaded images** - as stated in the [UX design section](#UX) the site relies heavy on the images uploaded by the users to showcase the recipes. This could potentially overwhelm the server storage capacities. The files are currently limited to 512 Kb per image but the build-in file compression would prove to be beneficial for a long run. 

- **Deletion of unused images** - at the moment when the data is removed it is deleted from the database only and do not delete file from the server. All the data has to be manually deleted. Automating this process would be of most importance to prevent server storage space from being overwhelmed by the files.

- **<span id="hrokufilesystem">Images storage on separate file server</span>** - At this time the website uses storage on the heroku server for files. The Heroku server uses [ephemeral filesystem](https://help.heroku.com/K1PPS2WM/why-are-my-file-uploads-missing-deleted) so the files would not be permanently stored. This is acceptable for purposes of this project but for full usability it needs to implement use of external file storage server.

<hr>

## Technologies Used

- [Python 3.7](https://www.python.org/) 
    - [Flask 1.0.2](http://flask.pocoo.org/)  
    - [Jinja2](http://jinja.pocoo.org/)
    - [Flask PyMongo 2.3.0](https://api.mongodb.com/python/current/)
    
    The program is based on Python 3.7 and Flask 1.0.2 framework. It uses Jinja2 for modeling a html templates. And uses Pymongo for communication with Mongo database.

- [MongoDB Atlas](https://www.mongodb.com/)
    
    Used MongoDB to store the information online

- [Heroku](https://www.heroku.com/home)
    
    Used for deployment

- HTML5 & CSS3
    
    Backbone of the website

- [Bootstrap 4.3](https://getbootstrap.com/) 

    Used for styling the website, and to provide functionality for Carousel, Accordion collapsing and Navigation bar collapsing menu on the smaller screens sizes.

- [Font Awesome 5.9](https://fontawesome.com/)
    
    Used for icons on the website and in the page icon

- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
    
    Used for providing dynamic operation on the front end 
    i.e. dynamically adding ingredients and steps without the need to query a server and reload the page.

<hr>

## Testing

All the major features were tested before they were committed to the Git repository.

All testing was completed manually

### Testing Process

1. Testing Responsive Design at screen sizes between 
    
    1. Testing Home Page
        - Testing Carousel scaling with the screen size
        - Testing Menu element 
        - Testing the elements in the accordion element scaling
    
    2. Moving to the Recipes site
        - Testing recipes cards
        - Testing sort button dropdown

    3. Opening the add recipe page
        - Checking each field 
            - The Upload files label is overflowing to the next line for the screen size width under 384px  
    
    4. Moving to Recipe detailed page view
        - Testing scaling of the jumbotron section
        - Testing of the recipe details scaling 
        - Testing adding the recipe on different screen sizes
            - noticed that the recipes after the first one are duplicating the data from the fist recipe. Will investigate later.
    
    5. Testing Edit page
        - testing each field
        - testing adding new recipes
        - testing adding new steps
        - testing fixed menu at  the bottom of the page

    6. Testing Delete Page

    7. Briefly checking the filtered views and the search results as those pages use the recipes page template and therefore should behave exactly the same

    - No problems with page scaling, which is mostly based on bootstrap. The problem with the overflowing label should be easy to fix and the problem with reviews is unrelated to responsive design.


2. Testing Carousel on the home page
    
    1. The five recipes on the home page were checked against mongodb which confirm the correct recipes are being displayed
    
    2. The buttons for next and previous recipe were tested
    
    3. Buttons under carousel label were tested

    4. Testing does clicking on the carousel link to the recipe

    - No problems with the carouse were detected.


3. Testing Dashboard.

    1. Tested arrow pointer to the dashboard (under the *View all recipes* button)

    2. Tested opening and closing of accordion element for each Category, Cuisine and each group from the Dietary Requirements.

    3. Tested Does the link to recipe in each group works as expected (tested two per grouping)

    4. Tested *View all recipes in the group* button. and confirmed that the amount of recipes beside indicate total amount of recipes

    5. Tested does the *add recipe* button in the alert box that appears when there are no recipes) works as expected. Also Tested couple of empty groups against the database to see are they accurate
        ```
        > db.recipes.find({},{'_id':0,'category':1})
        { "category" : "5cfecd091c9d440000d4649d" }
        { "category" : "5cfecc7b1c9d440000d46499" }
        { "category" : "5cfecd091c9d440000d4649d" }
        { "category" : "5cfecd091c9d440000d4649d" }
        { "category" : "5cfecd091c9d440000d4649d" }
        { "category" : "5cfecc611c9d440000d46498" }
        { "category" : "5cfecd141c9d440000d4649e" }
        > db.categories.find()
        { "_id" : ObjectId("5cfecc611c9d440000d46498"), "name" : "Breakfast" }
        { "_id" : ObjectId("5cfecc7b1c9d440000d46499"), "name" : "Lunch" }
        { "_id" : ObjectId("5cfecc961c9d440000d4649a"), "name" : "Dinner" }
        { "_id" : ObjectId("5cfeccaa1c9d440000d4649b"), "name" : "Dessert" }
        { "_id" : ObjectId("5cfeccba1c9d440000d4649c"), "name" : "Starter" }
        { "_id" : ObjectId("5cfecd091c9d440000d4649d"), "name" : "Main" }
        { "_id" : ObjectId("5cfecd141c9d440000d4649e"), "name" : "Beverage" }
        { "_id" : ObjectId("5cfecd9a1c9d440000d464a0"), "name" : "Salad" }
        ```

    - Dashboard is working correctly and all the links seems to point to right recipes. 


4. Testing the All recipes view
    
    1. Tested 3 links to recipes, confirmed that they point to the right recipe.

    2. Tested sorting button for different views against the database using the following commands and comparing them with the results on the page
        ```
        > r = cookbook.recipes
        > r.find({}, {"_id":0, "name":1, "views":1}).sort({"views":-1})
        { "name" : "The new Spaghetti Carbonara recipe",                "views" : 25 }
        { "name" : "Ultimate spaghetti carbonara recipe",               "views" : 23 }
        { "name" : "The Best Spaghetti Bolognese Recipe",               "views" : 15 }
        { "name" : "Home-Style Chicken Curry",                          "views" : 10 }
        { "name" : "Singapore Noodles",                                 "views" : 8 }
        { "name" : "Sandwich With Eggs",                                "views" : 4 }
        { "name" : "Test the recipe with the Empty File Upload field",  "views" : 4 }
        > r.find({}, {"_id":0, "name":1, "created_on":1}).sort({"created_on":-1})
        { "name" : "Test the recipe with ...",  "created_on" : ISODate("2019-06-14T23:06:27.917Z") }
        { "name" : "Sandwich With Eggs",        "created_on" : ISODate("2019-06-14T22:42:36.054Z") }
        { "name" : "Ultimate spaghetti ...",    "created_on" : ISODate("2019-06-12T15:07:11.382Z") }
        { "name" : "Singapore Noodles",         "created_on" : ISODate("2019-04-12T20:07:11.382Z") }
        { "name" : "The Best Spaghetti ...",    "created_on" : ISODate("2019-03-12T20:07:11.382Z") }
        { "name" : "Home-Style Chicken ...",    "created_on" : ISODate("2018-06-12T20:07:11.382Z") }
        { "name" : "The new Spaghetti ...",     "created_on" : ISODate("2018-01-10T20:07:11.382Z") }
        r.find({}, {"_id":0, "name":1, "reviews.total_number":1}).sort({"reviews.total_number":-1})
        { "name" : "Ultimate spaghetti ...",    "reviews" : { "total_number" : 3 } }
        { "name" : "The new Spaghetti ...",     "reviews" : { "total_number" : 1 } }
        { "name" : "The Best Spaghetti ...",    "reviews" : { "total_number" : 0 } }
        { "name" : "Singapore Noodles",         "reviews" : { "total_number" : 0 } }
        { "name" : "Home-Style Chicken Curry",  "reviews" : { "total_number" : 0 } }
        { "name" : "Sandwich With Eggs",        "reviews" : { "total_number" : 0 } }
        { "name" : "Test the recipe ...",       "reviews" : { "total_number" : 0 } }
        r.find({}, {"_id":0, "name":1, "reviews.avg_score":1}).sort({"reviews.avg_score":-1})
        { "name" : "Ultimate spaghetti ...",    "reviews" : { "avg_score" : 5 } }
        { "name" : "The new Spaghetti ...",     "reviews" : { "avg_score" : 5 } }
        { "name" : "The Best Spaghetti ...",    "reviews" : { "avg_score" : 0 } }
        { "name" : "Singapore Noodles",         "reviews" : { "avg_score" : 0 } }
        { "name" : "Home-Style Chicken ...",    "reviews" : { "avg_score" : 0 } }
        { "name" : "Sandwich With Eggs",        "reviews" : { "avg_score" : 0 } }
        { "name" : "Test the recipe with...",   "reviews" : { "avg_score" : 0 } }
        ```
    3. Tested the Add recipe page is pointing to correct page

    - All tests passed

5. Testing Adding Recipes

    1. Added recipe with image

    2. Attempt submit the form with empty fields

    3. Attempt removing first step, and first ingredient
    
    4. Added recipe without image

    5. Testing entering the text into numeric fields (Preperation time, servings Calories, Amount)

    - All test were passed, in case of submitting the form without the image the default image was chosen. And the form did not accept neither empty fields or text data in the numeric fields, highlighting the fields correctly.

6. Testing Editing the recipe
    
    1. Modify each field and click the checkbooks

    2. Attempt adding the new steps and new ingredients

    3. Submit the change

    - changes are represented on the recipe and in the database
    ```
    > r.find({"_id":ObjectId("5d054ad29e4274a87be6ed66")})
    { "_id" : ObjectId("5d054ad29e4274a87be6ed66"), "name" : "Test", "author" : "Test", "description" : "Test", "prep_time" : "1", "servings" : "2", "calories" : "3", "cuisine" : "5cfecbd01c9d440000d46497", "category" : "5cfecd9a1c9d440000d464a0", "is_vegiterian" : false, "is_lactose_free" : false, "is_gluten_free" : false, "ingredients" : [ { "ingredient_name" : "first ingredient", "ingredient_amount" : "500", "ingredient_unit" : "quater" }, { "ingredient_name" : "second ingredient", "ingredient_amount" : "100", "ingredient_unit" : "glass" }, { "ingredient_name" : "third ingredient", "ingredient_amount" : "200", "ingredient_unit" : "tsp" } ], "preperation" : [ "Step One" ], "views" : 1, "created_on" : ISODate("2019-06-15T19:45:22.795Z"), "reviews" : { "avg_score" : 0, "total_number" : 0, "reviews" : [ ] }, "picture" : "default.jpg" }
    > r.find({"_id":ObjectId("5d054ad29e4274a87be6ed66")})
    { "_id" : ObjectId("5d054ad29e4274a87be6ed66"), "name" : "None", "author" : "None", "description" : "None", "prep_time" : "10", "servings" : "20", "calories" : "30", "cuisine" : "5cfecba61c9d440000d46494", "category" : "5cfeccba1c9d440000d4649c", "is_vegiterian" : true, "is_lactose_free" : true, "is_gluten_free" : true, "ingredients" : [ { "ingredient_name" : "first None", "ingredient_amount" : "500", "ingredient_unit" : "quater" }, { "ingredient_name" : "second None", "ingredient_amount" : "100", "ingredient_unit" : "glass" } ], "preperation" : [ "Step None" ], "views" : 1, "created_on" : ISODate("2019-06-15T19:45:22.795Z"), "reviews" : { "avg_score" : 0, "total_number" : 0, "reviews" : [ ] }, "picture" : "default.jpg", "modified_on" : ISODate("2019-06-15T19:47:18.022Z") }
    ```

7. Testing Removing the recipe

    1. Press delete the recipe but then press cancel

    2. Completely deleting the recipe

    - deletion works as expected permanently removing the data from the database

8. Testing adding review

    1. testing adding review 

    - the test failed the application seems to be adding the last review as a new review with exactly the same date, probable cause is that I made a mistake in passing the value of the previous recipe instead of the one acquired from a website form.
    ```
    > r.find({"_id":ObjectId("5d0546399e4274a87be6ed64")}, {"_id":0, "reviews":1})
    { "reviews" : { "avg_score" : 5, "total_number" : 3, "reviews" : [ { "name" : "test", "rating" : "5", "description" : "test", "date" : ISODate("2019-06-15T19:31:44.877Z") }, { "name" : "test", "rating" : "5", "description" : "test", "date" : ISODate("2019-06-15T19:31:44.877Z") }, { "name" : "test", "rating" : "5", "description" : "test", "date" : ISODate("2019-06-15T19:31:44.877Z") } ] } }
    ```

8. Testing the navigation bar
    
    1. Tested home and logo links points to index page

    2. Tested that the categories and cuisines links point to filtered view

    3. Tested the search functionality by searching author, full name of the recipe, part of the recipe name and some string from the description

    4. While on the search page I confirmed that the sorting is working on this page as well

    - Everything is working as expected


### Testing Conclusion

    I completed the test and found only one major bug/issue. I have reviewed my code and the problem appears to comefrom using the same name during the itteration of the for loop as the variable I was passing to the pymongo query. This caused the last review to be always added to the database. Which would explain why I was able to add the new review when there was none and then when trying to add the new one the bug would happend. 
    
    In relation to the minor issue of the text of the file label overflowing outside the element, I decided to use the bootstrap *text-truncate* to prevent it.
    
    This concluded my tests upon updating the run.py file the issue with the duplicating reviews was solved. as shown below:
    ```
    > r.find({"_id":ObjectId("5d0546399e4274a87be6ed64")}, {"_id":0, "reviews":1})
    { "reviews" : { "avg_score" : 4, "total_number" : 4, "reviews" : [ { "name" : "test", "rating" : "5", "description" : "test", "date" : ISODate("2019-06-15T19:31:44.877Z") }, { "name" : "test", "rating" : "5", "description" : "test", "date" : ISODate("2019-06-15T19:31:44.877Z") }, { "name" : "test", "rating" : "5", "description" : "test", "date" : ISODate("2019-06-15T19:31:44.877Z") }, { "rating" : "1", "name" : "Pawel", "description" : "Some short message", "date" : ISODate("2019-06-15T19:58:50.663Z") } ] } }
    ```

<hr>

## Deployment

The app is deployed on heroku server under: http://open-cookbook-milestone.herokuapp.com

### System Variables

- **MONGO_URI** - holds the link to your local (or remote) instance of mongo database. 

    Defaults to local server MongoDB `'mongodb://localhost:27017/cookbook'`

- **MONGO_DBNAME** - holds the name of your database, It needs to match the name of the mongo database for the program to run correctly.

    Defaults to: `'cookbook'`

- **SECRET_KEY** - not mandatory to set but should be set up on the server side if deploying page online.

    Defaults to `'fallbacksecretvalue123'`

**Following variables should not be changed in most circumstances**

- **UPLOAD_FOLDER** - indicates where program should store the uploaded files. It provides an easy way for changing the location of the `static/img` folder on your server e.g. in case it uses different filesystem, however please keep in mind that the program is set up to look for the images in the `static/img` folder and therefore changing it will prevent the new files from being displayed.

    Defaults to `'.//static//img'`

- **PAGE_TITLE** - Stores name of the site displayed in the taskbar.

    Defaults to `'Open Cookbook'`

### Deployment Process

The program was deployed on Heroku server.

Steps used to deploy application to Heroku

1. create requirements.txt file
    ```
    sudo pip freeze -l > requirements.txt
    ```

2. create runtime.txt
    ```
    echo python-3.7.3 > runtime.txt
    ```

3. Create Procfile
    ```
    echo web: python run.py > Procfile
    ```

4. Create the application in heroku 
    ```
    heroku apps:create --region=eu <name of the application>
    ```

5. Initialize git repository, set up the remote and push master to heroku
    ```
    git init
    git remote add heroku <URL to heroku git returned in the previous step>
    git push -u heroku master
    ``` 

6. Set up server variables
    ```
    heroku config:set IP="0.0.0.0" PORT="5000" MONGO_URI="<link to mongo database>" MONGO_DBNAME="cookbook" UPLOAD_FOLDER="./static/img"
    ```

7. run the dyno
    ```
    heroku ps:scale web=1
    ```

This steps assume that the heroku cli and git cli are installed on the machine.


### Steps for Local Deployment
    
To deploy the application locally you need to have Python 3.7 installed on your local machine. If you wish to use the mongodb local server you it also need to installed locally.

Download the application from GitHub on to your Computer. 

Install required packages from requirements.txt file with command:
```
sudo pip install -r requirements.txt 
```

Once the required packages and their requirements are installed you need to add following global variables to your system as specified in the above section System Variables.

Run the application 
```
python run.py
```
     
<hr>


## <span id="credits">Resources Used and Credits<span>

### Page Content

Recipes were sourced from the [BBC Good Food](https://www.bbcgoodfood.com/)
* [Ultimate spaghetti carbonara recipe](https://www.bbcgoodfood.com/recipes/1052/ultimate-spaghetti-carbonara)
* [The best spaghetti Bolognese recipe](https://www.bbcgoodfood.com/recipes/1502640/the-best-spaghetti-bolognese)
* [Home-style chicken curry](https://www.bbcgoodfood.com/recipes/1993658/homestyle-chicken-curry)
* [Singapore noodles](https://www.bbcgoodfood.com/recipes/2040655/singapore-noodles)


### Images

* [Photo by Krista Stucchio on Unsplash](https://unsplash.com/photos/2CZ0Zpuj-gU)
    - Author: [Krista Stucchio](https://unsplash.com/@kristastucchio)
    - Licence: https://unsplash.com/license
* [Photo by Bruna Branco on Unsplash](https://unsplash.com/photos/t8hTmte4O_g)
    - Author: [Bruna Branco](https://unsplash.com/@brunabranco)
    - Licence: https://unsplash.com/license
* [Photo by Mgg Vitchakorn on Unsplash](https://unsplash.com/photos/uKrsWihnRRM)
    - Author: [Mgg Vitchakorn](https://unsplash.com/@mggbox)
    - Licence: https://unsplash.com/license
* [Photo by Joseph Gonzalez on Unsplash](https://unsplash.com/photos/fdlZBWIP0aM)
    - Author: [Joseph Gonzalez](https://unsplash.com/@miracletwentyone)
    - Licence: https://unsplash.com/license


### Guides / Instructions / Code Samples

* [Flask Documentation: Uploading Files](http://flask.pocoo.org/docs/1.0/patterns/fileuploads/#uploading-files)
    - the code for uploading the files was taken from Flask documentation in full and modified.
* [Bootstrap: Blog Template](https://getbootstrap.com/docs/4.3/examples/blog/)
    - Most of the website is based on this template

