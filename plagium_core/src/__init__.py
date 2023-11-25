from flask import Flask
from src.routes import bp
from dotenv import dotenv_values
import json

config = dotenv_values(".flaskenv")

def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config.from_pyfile("settings.py")
    app.register_blueprint(bp)
    
    return app