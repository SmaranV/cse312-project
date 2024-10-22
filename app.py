from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    # count = get_hit_count()
    return 'Hello World!'