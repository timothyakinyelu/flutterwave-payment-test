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
        if request.args.get('status'):
            if request.args.get('status') == 'cancelled':
                res = {'msg': 'You cancelled the payment!'}
                return jsonify(res)
            elif request.args.get('status') == 'successful':
                transactionID = request.args.get('transaction_id')
                transactionRef = request.args.get('tx_ref')
                url = 'https://api.flutterwave.com/v3/transactions/{}/verify'.format(transactionID)
                
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
                }
                res = requests.get(url, headers=headers)
                response = res.json()
                
                amountPaid = response['data']['charged_amount']
                amountRequired = response['data']['meta']['price']
                
                if response['data']['tx_ref'] == transactionRef:
                    if amountPaid >= int(amountRequired):
                        res = {'msg': 'Payment Successful!'}
                    else:
                        res = {'msg': 'Not enough funds to cover the transaction'}
                else:
                    res = {'msg': 'Invalid Transaction'}
                    
                return jsonify(res)
          
  
    @app.route('/create-subaccount')
    def createSubAccount():
        data = { 
            "account_bank":"044",
            "account_number":"0690000040",
            "business_name":"Grape Scotch",
            "business_email":"petya@stu.net",
            "business_contact":"Anonymous",
            "business_contact_mobile":"090820382",
            "business_mobile":"09083930450",
            "country":"NG",
            "meta":[
                {
                    "meta_name":"mem_adr",
                    "meta_value":"0x16241F327213"
                }
            ],
            "split_type":"percentage",
            "split_value":0.1
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
        }
        url = 'https://api.flutterwave.com/v3/subaccounts'
        
        res = requests.post(url, data=json.dumps(data), headers=headers)
        resp = res.json()
        
        if resp['status'] == 'success':
            res = requests.get(url, headers=headers)
            response = res.json()
            
            return response
        else:
            res = {'msg': 'Account already exists!'}
            return jsonify(res)
                   
    
    with app.app_context():
        return app;