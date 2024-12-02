from flask import Flask, request, render_template
from flask_socketio import SocketIO
from util.routing_functions import verify_login, logout_user, register_user, validate_auth_token, username_for_auth_token, send_post, send_post_history, likePost

app = Flask(__name__)

socketio = SocketIO(app, transports=['websocket'])
# socketio = SocketIO(app)
# should serve the homepage template/index.html
@app.route('/')
def hello():
    # TODO: check for auth token. aka if user logged in
    # continue to homepage if auth token exists
    # if user isn't logged in, send them to landing page
    auth=request.cookies.get('auth_token')
    if validate_auth_token(auth):
        return render_template('index.html',username=username_for_auth_token(auth))
    else:
        return render_template('landing.html')

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

@app.post('/post')
def post_post():
    return send_post()

@app.get('/post')
def get_posts():
    return send_post_history()
@app.post('/likePost')
def like_post():
    return likePost()

# Set cookies for all responses
@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@socketio.on("reaction")
def reaction(data):
    print("reaction: "+data)
    socketio.emit('reaction', data)

@socketio.on('connect')
def handle_connect():
    username = (request.cookies.get('auth_token'))
    if username and username != 'Guest':
        print(f"{username} connected and added to the user list.")
    else:
        print("Guest connected; not adding to the user list.")