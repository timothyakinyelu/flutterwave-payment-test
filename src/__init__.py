from flask import Flask, jsonify, json, redirect, request, current_app
from src.helpers.load_config import loadConfig
import requests
import time


def createApp():
    app = Flask(__name__, instance_relative_config=True)
    MODE = app.env
    Config = loadConfig(MODE)
    app.config.from_object(Config)
    
    data = {
        "tx_ref":'123-mx-32',
        "amount":"100",
        "currency":"NGN",
        "redirect_url":"http://localhost:5000/process",
        "payment_options":"card",
        "meta":{
            "price": "100"
        },
        "customer":{
            "email":"user@gmail.com",
            "phonenumber":"080****4528",
            "name":"Yemi Desola"
        },
        "customizations":{
            "title":"Pied Piper Payments",
            "description":"Middleout isn't free. Pay the price",
            "logo":"https://assets.piedpiper.com/logo.png"
        }
    }
    
    @app.route('/')
    def index():
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
        }
        
        res = requests.post('https://api.flutterwave.com/v3/payments',data=json.dumps(data), headers=headers)
        
        response = res.json()
        location = response['data']['link']
        
        if res.status_code and response['status'] == 'success':
            return redirect(location)
        else:
            res = {'msg': 'Unable to process payment'}
            return jsonify(res)
        
    @app.route('/process')
    def process():
        print(request.args)
    
    with app.app_context():
        return app;