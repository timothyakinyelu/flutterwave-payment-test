from flask import render_template, json, redirect, request, current_app, url_for, flash
from src.models.transactions import Transaction
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
            
            if subAccounts['data']:
                return render_template('donations.html', vendors=subAccounts['data'])
            else:
                flash('There are no vendors on this platform!')
                return render_template('donations.html')
        except Exception:
            pass
        
    if request.method == 'POST':
        ref = datetime.timestamp(datetime.now())
        form = request.form
        
        fullName = '{} {}'.format(form.get('first_name'), form.get('last_name'))
        email = form.get('email')
        phone = form.get('phone')
        currency = form.get('currency')
        amount = form.get('amount')
        subID = form.get('subaccountID')
        donationType = form.get('donation_type')
        
        if int(amount) == False:
            # check if the amount entered is an integer
            flash('Amount must be a round figure!')
            return redirect(url_for('payment.payment_view'))
            
        if not email:
            #  check if email is provided
            flash('Please enter a valid email!')
            return redirect(url_for('payment.payment_view'))

        if subID is None:
            #  check if subID is provided
            flash('Please a select a church to donate to!')
            return redirect(url_for('payment.payment_view'))

            
        payload = {
            "tx_ref": ref,
            "amount": amount,
            "currency": currency,
            "redirect_url": "http://localhost:5000/process",
            "payment_options": "card",
            "meta":{
                "reference": donationType
            },
            "customer":{
                "email": email,
                "phonenumber": phone,
                "name": fullName
            },
            "subaccounts": [
                {
                    "id": subID
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
        
        
def process_payment():
    """ verify payment parameters"""
    
    if request.args.get('status'):
        if request.args.get('status') == 'cancelled':
            # if request is cancelled by user redirect to main page and flash message
            
            flash('You cancelled the payment!')
            return redirect('payment.payment_view')
        elif request.args.get('status') == 'successful':
            # if request is successful, verify the transaction
            
            transactionID = request.args.get('transaction_id')
            transactionRef = request.args.get('tx_ref')
            url = '{}/transactions/{}/verify'.format(BaseUrl, transactionID)
            
            res = requests.get(url, headers=headers)
            response = res.json()
            
            amountSettled = response['data']['amount_settled']
            
            if response['data']['tx_ref'] == transactionRef:
                if amountSettled:
                    return render_template('response.html', home=url_for('payment.payment_view'))
                else:
                    flash('Not enough funds to cover the transaction')
                    return redirect('payment.payment_view')
            else:
                flash('Invalid Transaction')
                return redirect('payment.payment_view')