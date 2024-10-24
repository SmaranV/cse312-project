from flask import Flask, request, render_template
from util.routing_functions import verify_login, serve_login

app = Flask(__name__)


# should serve the homepage template/index.html
@app.route('/')
def hello():
    return render_template('index.html')


@app.post('/login')
def login():
    return verify_login()