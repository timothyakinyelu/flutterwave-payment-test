from flask import render_template, url_for, request


def admin():
    """ Display all action buttons in admin area"""
    
    return render_template('admin.html')