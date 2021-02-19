from flask import Flask, jsonify, json, redirect, request, current_app
from src.helpers.load_config import loadConfig
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
import requests

csrf = CSRFProtect()

def createApp():
    app = Flask(__name__, instance_relative_config=True)
    MODE = app.env
    Config = loadConfig(MODE)
    app.config.from_object(Config)
    
    from src.db import db
    db.init_app(app)
    csrf.init_app(app)
    
    
    @app.route('/')
    def index():
        ref = datetime.timestamp(datetime.now())
    
        percent_charge = 10
        amount = 300
        # merchant_charge = percent_charge/100
        # merchant_fee = merchant_charge * amount
        # subaccount_value = float(amount) - merchant_fee
        
        data = {
            "tx_ref":ref,
            "amount":amount,
            "currency":"NGN",
            "redirect_url":"http://localhost:5000/process",
            "payment_options":"card",
            "customer":{
                "email":"user@gmail.com",
                "phonenumber":"080****4528",
                "name":"Trey Desola"
            },
            "subaccounts": [
                {
                    "id": "RS_91DD512FFC60A8EA0D6A3D6806692808"
                }
            ],
            "customizations":{
                "title":"Pied Piper Payments",
                "description":"Middleout isn't free. Pay the price",
                "logo":"https://assets.piedpiper.com/logo.png"
            }
        }
        
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
                resp = res.json()
                return resp
                
                # amountPaid = response['data']['charged_amount']
                # amountRequired = response['data']['meta']['price']
                
                # if response['data']['tx_ref'] == transactionRef:
                #     if amountPaid >= float(amountRequired):
                #         res = {'msg': 'Payment Successful!'}
                #     else:
                #         res = {'msg': 'Not enough funds to cover the transaction'}
                # else:
                #     res = {'msg': 'Invalid Transaction'}
                    
                # return jsonify(res)
          
  
    @app.route('/create-subaccount')
    def createSubAccount():
        data = { 
            "account_bank": "044",
            "account_number": "0690000039",
            "business_name": "Grape Scotch",
            "business_email": "petya@stu.net",
            "business_contact": "Anonymous",
            "business_contact_mobile": "090820382",
            "business_mobile": "09083930450",
            "country": "NG",
            "split_type": "percentage",
            "split_value": 0.1
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
        }
        url = 'https://api.flutterwave.com/v3/subaccounts'
        
        res = requests.post(url, data=json.dumps(data), headers=headers)
        response = res.json()
        
        return response
        
        if resp['status'] == 'success':
            res = requests.get(url, headers=headers)
            response = res.json()
            
            return response
        else:
            res = {'msg': 'Account already exists!'}
            return jsonify(res)
        

    @app.route('/subaccounts')
    def subaccounts():
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
        }
        fetchUrl = 'https://api.flutterwave.com/v3/subaccounts'
        
        res = requests.get(fetchUrl, headers=headers)
        response = res.json()
        
        return response
        

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
    
    
    @app.route('/charge-token')
    def remeberToken():
        data = {
            "token":"flw-t1nf-7ba64bb6ffd422f6a92a846f7a5de269-m03k",
            "currency":"NGN",
            "country":"NG",
            "amount":200,
            "email":"user@gmail.com",
            "narration":"Sample tokenized charge",
            "tx_ref":"1613693187.078396"
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
        }
        fetchUrl = 'https://api.flutterwave.com/v3/tokenized-charges'
        res = requests.post(fetchUrl, data=json.dumps(data), headers=headers)
        response = res.json()
        
        return response
    
    @app.route('/webhook', methods=['POST'])
    @csrf.exempt
    def webhook(request):
        pass
    
    from src.models import cards, transactions, users, pivot
    
    with app.app_context():
        # register app blueprints
        from src.views.payments import payment
        app.register_blueprint(payment)
        
        db.create_all()
        return app;
    