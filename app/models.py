from app import db


class Product(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    specification = db.Column(db.String(120))
    unit = db.Column(db.String(20))
    initial_stock = db.Column(db.Integer, default=0)
    current_stock = db.Column(db.Integer, default=0)


class Purchase(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    product_id = db.Column(db.String(64), db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date)
    supplier = db.Column(db.String(64))


class Sale(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    product_id = db.Column(db.String(64), db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date)
    destination = db.Column(db.String(64))
