import uuid

from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.models import Product, Purchase, Sale
from datetime import datetime


@current_app.route('/')
@current_app.route('/index')
def index():
    products = Product.query.all()
    purchases = Purchase.query.all()
    sales = Sale.query.all()
    return render_template('index.html', products=products, purchases=purchases, sales=sales)


@current_app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        specification = request.form['specification']
        unit = request.form['unit']
        initial_stock = request.form['initial_stock']
        product = Product(id=id, name=name, specification=specification, unit=unit, initial_stock=initial_stock, current_stock=initial_stock)
        db.session.add(product)
        db.session.commit()
        flash('新库存添加成功')
        return redirect(url_for('index', show_inventory=True))
    return render_template('product.html')


@current_app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['purchase_name']
        quantity = request.form['quantity']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        supplier = request.form['supplier']
        purchase = Purchase(id=str(uuid.uuid4()), product_id=product_id, name=name, quantity=quantity, date=date, supplier=supplier)
        db.session.add(purchase)

        product = Product.query.get(product_id)
        product.current_stock += int(quantity)

        db.session.commit()
        flash('入库记录添加成功!')
        return redirect(url_for('index', show_inventory=True))
    products = Product.query.all()
    return render_template('purchase.html', products=products)


@current_app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['sale_name']
        quantity = request.form['quantity']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        destination = request.form['destination']
        sale = Sale(id=str(uuid.uuid4()), product_id=product_id, name=name, quantity=quantity, date=date, destination=destination)
        db.session.add(sale)

        product = Product.query.get(product_id)
        product.current_stock -= int(quantity)

        db.session.commit()
        flash('出库记录添加成功')
        return redirect(url_for('index',show_inventory=True))
    available_products = Product.query.filter(Product.initial_stock > 0).all()
    return render_template('sale.html', available_products=available_products)


@current_app.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('产品删除成功!')
    return redirect(url_for('index',show_inventory=True))


@current_app.route('/delete_purchase/<purchase_id>', methods=['POST'])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    db.session.delete(purchase)
    db.session.commit()
    flash('入库记录删除成功!')
    return redirect(url_for('index',show_inventory=True))


@current_app.route('/delete_sale/<sale_id>', methods=['POST'])
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    flash('出库记录删除成功!')
    return redirect(url_for('index',show_inventory=True))
