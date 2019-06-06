import os
from flask import Flask, render_template, url_for, redirect, request


app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello World!"
    
    
app.run(
    host=os.getenv('IP', '127.0.0.1'), 
    port=int(os.getenv('PORT', "5500")), 
    debug=True)