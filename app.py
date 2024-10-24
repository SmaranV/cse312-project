from flask import Flask, request, render_template
from util.routing_functions import verify_login, register_user

app = Flask(__name__)


# should serve the homepage template/index.html
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/landing')
def landing_page():
    return render_template('landing.html')

@app.post('/login')
def login():
    return verify_login()

@app.post('/register')
def register():
    return register_user()