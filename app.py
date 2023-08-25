from flask import Flask, Response, make_response, render_template, send_file, stream_with_context,request,jsonify
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index():  
    return render_template("index.html")

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route("/me", methods=['POST'])
def me_api():
    return {
        "username": 'user.username',
        "theme": 'user.theme',
        'datetime': datetime.now()
    }