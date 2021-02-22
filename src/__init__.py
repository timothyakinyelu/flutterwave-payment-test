from flask import Flask, jsonify, json, redirect, request, current_app
from src.helpers.load_config import loadConfig
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from src.models.users import User
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
    
    @login_manager.user_loader
    def load_user(user_id):
        """Check if user is logged-in on every page load."""
        
        if user_id is not None:
            return User.query.get(user_id)
        return None

        

    @app.route('/update-subaccount/<int:id>')
    def updateSubAccount(id):
        data = {
            "business_name": "Leaping Lizards",
            "business_email": "llp@example.com",
            "account_bank": "044",
            "account_number": "0690000040",
            "split_type": "flat",
            "split_value": 0
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
        }
        
        res = requests.put('https://api.flutterwave.com/v3/subaccounts/{}'.format(id), data=json.dumps(data), headers=headers)
        resp = res.json()
        
        # if resp['status'] == 'success':
        #     res = requests.get(fetchUrl, headers=headers)
        #     response = res.json()
            
        #     return response
        # else:
        return resp
        
        
    @app.route('/delete-subaccount/<int:id>')
    def deleteSubAccount(id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
        }
        fetchUrl = 'https://api.flutterwave.com/v3/subaccounts'
        
        res = requests.delete('https://api.flutterwave.com/v3/subaccounts/{}'.format(id), headers=headers)
        resp = res.json()
        
        if resp['status'] == 'success':
            res = requests.get(fetchUrl, headers=headers)
            response = res.json()
            
            return response
        else:
            return resp
        
    @app.route('/settlements')
    def settlements():
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
        }
        fetchUrl = 'https://api.flutterwave.com/v3/settlements'
        
        res = requests.get(fetchUrl, headers=headers)
        resp = res.json()
        
        return resp
    
    @app.route('/webhook', methods=['POST'])
    @csrf.exempt
    def webhook(request):
        pass
    
    from src.models import cards, transactions, users
    
    with app.app_context():
        # register app blueprints
        from src.views.users import users_route
        from src.views.admin import admin_route
        
        app.register_blueprint(users_route.user)
        app.register_blueprint(admin_route.admin)
        
        db.create_all()
        return app;
    