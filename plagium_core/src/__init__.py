from flask import Flask
from src.routes import bp
from dotenv import dotenv_values
from flask_cors import CORS

config = dotenv_values(".flaskenv")

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_pyfile("settings.py")
    app.register_blueprint(bp)
    
    return app