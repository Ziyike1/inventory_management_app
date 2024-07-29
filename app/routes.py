import getpass
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
    current_user = getpass.getuser()
    return render_template('index.html', products=products, purchases=purchases, sales=sales, current_time=datetime.now(), current_user=current_user)


@current_app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        specification = request.form['specification']
        initial_stock = request.form['initial_stock']
        product = Product(id=id, name=name, specification=specification, initial_stock=initial_stock, current_stock=initial_stock)
        db.session.add(product)
        db.session.commit()
        flash('新库存添加成功')
        return redirect(url_for('index', show_inventory=True))
    current_user = getpass.getuser()
    return render_template('product.html', current_time=datetime.now(), current_user=current_user)


@current_app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        product_id = request.form['product_id']
        new_product_id = request.form.get('new_product_id')
        name = request.form['purchase_name']
        specification = request.form['specification']
        quantity = int(request.form['quantity'])
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        supplier = request.form.get('supplier', None)
        things = request.form['things']
        company = request.form['company']

        if new_product_id:
            product_id = new_product_id
            product = Product(id=product_id, name=name, specification=specification, initial_stock=quantity,
                              current_stock=quantity)
            db.session.add(product)
        else:
            product = Product.query.get(product_id)
            product.current_stock = int(product.current_stock)
            product.current_stock = int(product.current_stock) + quantity

        purchase = Purchase(id=str(uuid.uuid4()), product_id=product_id, name=name, specification=specification, quantity=quantity, date=date, supplier=supplier, things=things, company=company)
        db.session.add(purchase)
        db.session.commit()

        flash('入库记录添加成功!')
        return redirect(url_for('index', show_inventory=True))

    products = Product.query.all()
    current_user = getpass.getuser()
    return render_template('purchase.html', products=products, current_time=datetime.now(), current_user=current_user)


@current_app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['sale_name']
        specification = request.form['specification']
        quantity = request.form['quantity']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        supplier = request.form.get('supplier', None)
        things = request.form['things']
        company = request.form['company']
        sale = Sale(id=str(uuid.uuid4()), product_id=product_id, name=name, specification=specification, quantity=quantity, date=date, supplier=supplier, things=things, company=company)
        db.session.add(sale)

        product = Product.query.get(product_id)
        product.current_stock -= int(quantity)

        db.session.commit()
        flash('出库记录添加成功')
        return redirect(url_for('index',show_inventory=True))
    available_products = Product.query.filter(Product.current_stock > 0).all()
    current_user = getpass.getuser()
    return render_template('sale.html', available_products=available_products, current_time=datetime.now(), current_user=current_user)


@current_app.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('产品删除成功!')
    return redirect(url_for('index', show_inventory=True))


@current_app.route('/delete_purchase/<purchase_id>', methods=['POST'])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    db.session.delete(purchase)
    db.session.commit()
    flash('入库记录删除成功!')
    return redirect(url_for('index', show_inventory=True))


@current_app.route('/delete_sale/<sale_id>', methods=['POST'])
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    flash('出库记录删除成功!')
    return redirect(url_for('index', show_inventory=True))
