from extensions import db
from sqlalchemy.dialects.postgresql import BYTEA
from datetime import datetime

class Users(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(31), nullable=False)
    user_password = db.Column(BYTEA, nullable=False)
    
    sold_product = db.relationship("Products", backref='users')
    
    def __init__(self, username, password):
        self.user_name = username
        self.user_password = password
        
    def __repr__(self):
        return f"<User {self.user_name!r}>"
    
    def update_data(self, username, password):
        if username:
            self.user_name = username
        self.user_password = password
    
    def get_userid(self):
        return self.user_id
    
    def get_username(self):
        return self.user_name
    
    def get_password(self):
        return self.user_password
        
class Products(db.Model):
    __tablename__ = "products"
    
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(31), nullable=False)
    product_size = db.Column(db.Integer, nullable=False)
    product_color = db.Column(db.String(31))
    product_sold_price = db.Column(db.Integer, nullable=False)
    product_get_price = db.Column(db.Integer, nullable=False)
    product_sold_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    product_profit = db.Column(db.Integer, nullable=False)
    
    seller_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
    def __init__(self, name, size, color, sold_price, get_price, seller_id):
        self.product_name = name
        self.product_size = size
        self.product_color = color
        self.product_sold_price = sold_price
        self.product_get_price = get_price
        self.product_profit = sold_price - get_price
        self.seller_id = seller_id
    
    def __repr__(self):
        return f"<Product {self.product_color!r} {self.product_name!r} {self.product_size!r}>"