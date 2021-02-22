from flask import render_template, json, redirect, request, current_app, url_for, flash
from src.models.transactions import Transaction
from src.models.cards import Card
from src.models.users import User
from datetime import datetime
from flask_login import current_user
import requests

# Flutterwave BaseUrl
BaseUrl = 'https://api.flutterwave.com/v3'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
}
WebDomain = 'http://localhost:5000'

def payments():
    """Method to fetch form and send payment request payload"""
    if request.method == 'GET':
        try:
            subAccountsURL = '{}/subaccounts'.format(BaseUrl)
            res = requests.get(subAccountsURL, headers=headers)
            subAccounts = res.json()
            
            cards = current_user.cards
            
            if subAccounts['data']:
                return render_template('donations.html', vendors=subAccounts['data'], cards=cards)
            else:
                flash('There are no vendors on this platform!')
                return render_template('donations.html')
        except Exception:
            pass
        
    if request.method == 'POST':
        ref = datetime.timestamp(datetime.now())
        form = request.form
        
        currency = form.get('currency')
        amount = form.get('amount')
        subID = form.get('subaccountID')
        donationType = form.get('donation_type')
        retainedCard = form.get('retainedCard')
        
        if int(amount) == False:
            # check if the amount entered is an integer
            flash('Amount must be a round figure!')
            return redirect(url_for('payment.payment_view'))

        if subID is None:
            #  check if subID is provided
            flash('Please a select a church to donate to!')
            return redirect(url_for('payment.payment_view'))
        
        
        if  retainedCard == '1':
            # existing user can be gotten if a login system is used
            # if user exists, charge user with token instead
            card_id = form.get('card')
            card = Card.query.filter_by(id = card_id).first()
            country = card.country
            
            data = {
                "tx_ref": ref,
                "token": card.token,
                "currency": currency,
                "country": country[-2:],
                "amount": amount,
                "email": current_user.email,
                "phone": current_user.phone,
                "full_name": current_user.full_name,
                "meta":{
                    "reference": donationType
                },
                "subaccounts": [
                    {
                        "id": subID
                    }
                ],
            }
            
            tokenUrl = '{}/tokenized-charges'.format(BaseUrl)
            res = requests.post(tokenUrl, data=json.dumps(data), headers=headers)
            response = res.json()
            
            # store transaction ref to check if costumers have any issue with a payment
            transaction = Transaction(
                card_id = card.id,
                user_id = current_user.id,
                transaction_ref = response['data']['tx_ref'],
                status = response['data']['status'],
                amount = response['data']['amount']
            )
            transaction.save()
            
            return render_template('response.html', home=url_for('user.payment_view'))
        else:   
            # only use if it's a new user or new card
            payload = {
                "tx_ref": ref,
                "amount": amount,
                "currency": currency,
                "redirect_url": '{}{}'.format(WebDomain, url_for('user.verification_view')),
                "payment_options": "card",
                "meta":{
                    "reference": donationType
                },
                "customer":{
                    "email": current_user.email,
                    "phonenumber": current_user.phone,
                    "name": current_user.full_name
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
                    return redirect(url_for('user.payment_view'))
            except Exception:
                pass
        
        
def verify_payment():
    """ verify payment parameters"""
    
    if request.args.get('status'):
        if request.args.get('status') == 'cancelled':
            # if request is cancelled by user redirect to main page and flash message
            
            flash('You cancelled the payment!')
            return redirect('user.payment_view')
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
                    # store card token generated in order to carry out future payments 
                    # via the token instead of user entering card details
                    # user can be recognised on login to the app
                    firstSix = response['data']['card']['first_6digits']
                    lastFour = response['data']['card']['last_4digits']
                    card = Card.query.filter_by(first_six = firstSix, last_four = lastFour).first()
                    
                    if card is None:
                        new_card = Card(
                            user_id = current_user.id,
                            first_six = firstSix,
                            last_four = lastFour,
                            token = response['data']['card']['token'],
                            issuer = response['data']['card']['issuer'],
                            card_type = response['data']['card']['type'],
                            card_expiry = response['data']['card']['expiry'],
                            country = response['data']['card']['country']
                        )
                        new_card.save()
                        
                        transaction = Transaction(
                            card_id = new_card.id,
                            user_id = current_user.id,
                            transaction_ref = transactionRef,
                            status = response['data']['status'],
                            amount = response['data']['amount_settled']
                        )
                    else:   
                        # store transaction ref to check if costumers have any issue with a payment
                        transaction = Transaction(
                            card_id = card.id,
                            user_id = current_user.id,
                            transaction_ref = transactionRef,
                            status = response['data']['status'],
                            amount = response['data']['amount_settled']
                        )
                    transaction.save()
                    
                    
                    if current_user.customer_id is None:
                        # update user table with customer_id
                        current_user.customer_id = response['data']['customer']['id']
    
                        current_user.save()
                    
                    
                    return render_template('response.html', home=url_for('user.payment_view'))
                else:
                    flash('Not enough funds to cover the transaction')
                    return redirect('user.payment_view')
            else:
                flash('Invalid Transaction')
                return redirect('user.payment_view')