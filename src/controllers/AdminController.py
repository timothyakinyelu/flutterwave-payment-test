from flask import render_template, url_for, request, current_app, json, flash, redirect
import requests


# Flutterwave BaseUrl
BaseUrl = 'https://api.flutterwave.com/v3'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(current_app.config['SEC_KEY'])
}


def admin():
    """ Display all action buttons in admin area"""
    
    return render_template('admin.html')


def create_vendor():
    """ Get and create new vendor"""
    
    if request.method == 'GET':        
        banksUrl = '{}/banks/NG'.format(BaseUrl)
        response = requests.get(banksUrl, headers=headers)
        banks = response.json()
        
        return render_template('create_subaccounts.html', banks=banks['data'])
    
    if request.method == 'POST':
        form = request.form
        code = form.get('bank_code')
        number = form.get('account_number')
        name = form.get('business_name')
        email = form.get('business_email')
        phone = form.get('business_mobile')
        contact = form.get('contact_person')
        mobile = form.get('contact_mobile')
        
        payload = { 
            "account_bank": code,
            "account_number": number,
            "business_name": name,
            "business_email": email,
            "business_contact": contact,
            "business_contact_mobile": mobile,
            "business_mobile": phone,
            "country": "NG",
            "split_type": "percentage",
            "split_value": 0.1
        }
        
        subUrl = '{}/subaccounts'.format(BaseUrl)
        
        res = requests.post(subUrl, data=json.dumps(payload), headers=headers)
        response = res.json()
        
        if response['status'] == 'success':
            return redirect(url_for('admin.allvendors_view'))
        else:
            flash(response['message'])
            return redirect(url_for('admin.vendors_view'))