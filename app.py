from flask import Flask, request, render_template
from util.routing_functions import verify_login, logout_user, register_user

app = Flask(__name__)


# should serve the homepage template/index.html
@app.route('/')
def hello():
    # TODO: check for auth token. aka if user logged in
    # continue to homepage if auth token exists
    # if user isn't logged in, send them to landing page
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

@app.post('/logout')
def logout():
    return logout_user()


# Set cookies for all responses
@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response