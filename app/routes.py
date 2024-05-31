from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.models import Product, Purchase, Sale


@current_app.route('/')
@current_app.route('/index')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@current_app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        name = request.form['name']
        specification = request.form['specification']
        unit = request.form['unit']
        product = Product(name=name, specification=specification, unit=unit)
        db.session.add(product)
        db.session.commit()
        flash('New product added successfully!')
        return redirect(url_for('index'))
    return render_template('product.html')



