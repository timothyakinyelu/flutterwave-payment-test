from flask import render_template, flash, redirect, url_for, request
from src.models.users import User
from flask_login import login_user

def Register():
    """ Register a new user on the application. """
    
    if request.method == 'GET':
        render_template('registration.html')
        
    if request.method == 'POST':
        form = request.form
        
        phone = form.get('phone')
        email = form.get('email')
        firstName = form.get('first_name')
        lastName = form.get('last_name')
        
        user = User(
            phone = phone,
            email = email,
            full_name = '{} {}'.format(firstName, lastName)
        )
        user.save()
        login_user(user)
        
        return redirect(url_for('user.payment_view'))
        