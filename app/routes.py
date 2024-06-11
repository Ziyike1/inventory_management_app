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


@current_app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        date = request.form['date']
        supplier = request.form['supplier']
        purchase = Purchase(product_id=product_id, quantity=quantity, date=date, supplier=supplier)
        db.session.add(purchase)
        db.session.commit()
        flash('Purchase record added successfully!')
        return redirect(url_for('index'))
    return render_template('purchase.html')


@current_app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        date = request.form['date']
        destination = request.form['destination']
        sale = Sale(product_id=product_id, quantity=quantity, date=date, destination=destination)
        db.session.add(sale)
        db.session.commit()
        flash('Sale record added successfully!')
        return redirect(url_for('index'))
    return render_template('sale.html')
