from flask import Flask, jsonify, json, redirect, request, current_app
from src.helpers.load_config import loadConfig
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
import requests

login_manager = LoginManager()
csrf = CSRFProtect()

def createApp():
    app = Flask(__name__, instance_relative_config=True, template_folder='./templates')
    MODE = app.env
    Config = loadConfig(MODE)
    app.config.from_object(Config)
    
    from src.db import db
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    from src.models import cards, transactions, users
    
    @login_manager.user_loader
    def load_user(user_id):
        """Check if user is logged-in on every page load."""
        
        if user_id is not None:
            return users.User.query.get(user_id)
        return None
    
    with app.app_context():
        # register app blueprints
        from src.views.users import users_route
        from src.views.admin import admin_route
        
        app.register_blueprint(users_route.user)
        app.register_blueprint(admin_route.admin)
        
        db.create_all()
        return app;
    