from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
from apps.app import twiity

def make_app():
    CORS(app)
    app.register_blueprint(twiity)
    return app


if __name__ == '__main__':
    make_app().run(host='0.0.0.0',debug=True,port=9009)

