from flask import render_template, flash, redirect, url_for, request
from src.models.users import User
from flask_login import login_user

def Register():
    """ Register a new user on the application. """
    
    if request.method == 'GET':
        return render_template('registration.html')
        
    if request.method == 'POST':
        form = request.form
        
        phone = form.get('phone')
        email = '{}@example.com'.format(form.get('phone'))
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
        
        
def Login():
    """ Login a user into the application. """
    
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        phone = request.form.get('phone')
        
        user = User.query.filter_by(phone = phone).first()
        
        if user:
            login_user(user)
            return redirect(url_for('user.payment_view'))
        else:
            flash('Phone number not recognized')
            return redirect(url_for('user.login_view'))
        