import os
from flask import Flask, render_template, url_for, redirect, request, session


app = Flask(__name__)



@app.route("/")
def hello():
    return render_template('index.html', title="Open Cookbook")
    
    
app.run(
    host=os.getenv('IP', '127.0.0.1'), 
    port=int(os.getenv('PORT', "5500")), 
    debug=True)