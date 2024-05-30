from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.models import Product, Purchase, Sale


@current_app.route('/')
@current_app.route('/index')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)



