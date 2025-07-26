from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with conversations
    conversations = db.relationship('Conversation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class Conversation(db.Model):
    """Conversation model for storing conversation sessions"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with messages
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade='all, delete-orphan', order_by='Message.created_at')
    
    def __repr__(self):
        return f'<Conversation {self.id} - {self.title}>'

class Message(db.Model):
    """Message model for storing individual messages in conversations"""
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id} - {self.role}>'

# E-commerce data models for storing the CSV data
class Product(db.Model):
    """Product model for storing e-commerce product data"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(200), nullable=True)
    brand = db.Column(db.String(100), nullable=True)
    retail_price = db.Column(db.Float, nullable=True)
    department = db.Column(db.String(100), nullable=True)
    sku = db.Column(db.String(100), nullable=True)
    distribution_center_id = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Order(db.Model):
    """Order model for storing e-commerce order data"""
    __tablename__ = 'orders'
    
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    num_of_item = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f'<Order {self.order_id}>'

class OrderItem(db.Model):
    """OrderItem model for storing e-commerce order item data"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    product_id = db.Column(db.Integer, nullable=True)
    inventory_item_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'

class InventoryItem(db.Model):
    """InventoryItem model for storing e-commerce inventory data"""
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    sold_at = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    product_category = db.Column(db.String(100), nullable=True)
    product_name = db.Column(db.String(200), nullable=True)
    product_brand = db.Column(db.String(100), nullable=True)
    product_retail_price = db.Column(db.Float, nullable=True)
    product_department = db.Column(db.String(100), nullable=True)
    product_sku = db.Column(db.String(100), nullable=True)
    product_distribution_center_id = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f'<InventoryItem {self.id}>'

class UserData(db.Model):
    """UserData model for storing e-commerce user data"""
    __tablename__ = 'user_data'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    street_address = db.Column(db.String(200), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    traffic_source = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<UserData {self.id}>'

class DistributionCenter(db.Model):
    """DistributionCenter model for storing e-commerce distribution center data"""
    __tablename__ = 'distribution_centers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f'<DistributionCenter {self.name}>' 