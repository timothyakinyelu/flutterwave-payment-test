from flask import render_template, json, redirect, request, current_app, url_for
from datetime import datetime
import requests

# Flutterwave BaseUrl
BaseUrl = 'https://api.flutterwave.com/v3'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
}

def payments():
    """Method to fetch form and send payment request payload"""
    
    if request.method == 'GET':
        try:
            subAccountsURL = '{}/subaccounts'.format(BaseUrl)
            res = requests.get(subAccountsURL, headers=headers)
            subAccounts = res.json()
            
            if subAccounts:
                return render_template('donations.html', vendors=subAccounts)
            else:
                flash('There are no vendors on this platform!')
                return render_template('donations.html')
        except Exception:
            pass
    
    if request.method == 'POST':
        ref = datetime.timestamp(datetime.now())
        form = request.form
        payload = {
            "tx_ref": ref,
            "amount": form.get('amount'),
            "currency": form.get('currency'),
            "redirect_url": "http://localhost:5000/process",
            "payment_options": "card",
            "customer":{
                "email": form.get('email'),
                "phonenumber": form.get('phone'),
                "name": form.get('full_name')
            },
            "subaccounts": [
                {
                    "id": form.get('subaccountID')
                }
            ],
            "customizations":{
                "title":"Pied Piper Payments",
                "description":"Middleout isn't free. Pay the price",
                "logo":"https://assets.piedpiper.com/logo.png"
            }
        }
        
        paymentURL = '{}/payments'.format(BaseUrl)
        
        try:
            donate = requests.post(paymentURL, data=json.dumps(payload), headers=headers)
            response = donate.json()
            
            flutterCheckout = response['data']['link']
            if donate.status_code == 200 and response['status'] == 'success':
                return redirect(flutterCheckout)
            else:
                flash('Unable to process payment')
                return redirect(url_for('paymentview.payment_view'))
        except Exception:
            pass
        
        