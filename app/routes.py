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
        name = request.form['name']
        specification = request.form['specification']
        unit = request.form['unit']
        product = Product(name=name, specification=specification, unit=unit)
        db.session.add(product)
        db.session.commit()
        flash('新产品添加成功')
        return redirect(url_for('index'))
    return render_template('product.html')


@current_app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
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
        flash('出售记录添加成功')
        return redirect(url_for('index'))
    return render_template('sale.html')


@current_app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('产品删除成功!')
    return redirect(url_for('index'))


@current_app.route('/delete_purchase/<int:purchase_id>', methods=['POST'])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    db.session.delete(purchase)
    db.session.commit()
    flash('采购记录删除成功!')
    return redirect(url_for('index'))


@current_app.route('/delete_sale/<int:sale_id>', methods=['POST'])
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    flash('销售记录删除成功!')
    return redirect(url_for('index'))
