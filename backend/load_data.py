import pandas as pd
import os
from datetime import datetime
from models import db, Product, Order, OrderItem, InventoryItem, UserData, DistributionCenter
from config import Config
from dateutil import parser

def parse_datetime(date_str):
    """Parse datetime string safely"""
    if pd.isna(date_str) or date_str == '':
        return None
    try:
        return parser.parse(str(date_str))
    except:
        return None

def load_products(csv_path):
    """Load products data from CSV"""
    print("Loading products...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        product = Product(
            id=row['id'],
            cost=row['cost'] if pd.notna(row['cost']) else None,
            category=row['category'] if pd.notna(row['category']) else None,
            name=row['name'] if pd.notna(row['name']) else None,
            brand=row['brand'] if pd.notna(row['brand']) else None,
            retail_price=row['retail_price'] if pd.notna(row['retail_price']) else None,
            department=row['department'] if pd.notna(row['department']) else None,
            sku=row['sku'] if pd.notna(row['sku']) else None,
            distribution_center_id=row['distribution_center_id'] if pd.notna(row['distribution_center_id']) else None
        )
        db.session.add(product)
    
    db.session.commit()
    print(f"Loaded {len(df)} products")

def load_orders(csv_path):
    """Load orders data from CSV"""
    print("Loading orders...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        order = Order(
            order_id=row['order_id'],
            user_id=row['user_id'] if pd.notna(row['user_id']) else None,
            status=row['status'] if pd.notna(row['status']) else None,
            gender=row['gender'] if pd.notna(row['gender']) else None,
            created_at=parse_datetime(row['created_at']),
            returned_at=parse_datetime(row['returned_at']),
            shipped_at=parse_datetime(row['shipped_at']),
            delivered_at=parse_datetime(row['delivered_at']),
            num_of_item=row['num_of_item'] if pd.notna(row['num_of_item']) else None
        )
        db.session.add(order)
    
    db.session.commit()
    print(f"Loaded {len(df)} orders")

def load_order_items(csv_path):
    """Load order items data from CSV"""
    print("Loading order items...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        order_item = OrderItem(
            id=row['id'],
            order_id=row['order_id'] if pd.notna(row['order_id']) else None,
            user_id=row['user_id'] if pd.notna(row['user_id']) else None,
            product_id=row['product_id'] if pd.notna(row['product_id']) else None,
            inventory_item_id=row['inventory_item_id'] if pd.notna(row['inventory_item_id']) else None,
            status=row['status'] if pd.notna(row['status']) else None,
            created_at=parse_datetime(row['created_at']),
            shipped_at=parse_datetime(row['shipped_at']),
            delivered_at=parse_datetime(row['delivered_at']),
            returned_at=parse_datetime(row['returned_at'])
        )
        db.session.add(order_item)
    
    db.session.commit()
    print(f"Loaded {len(df)} order items")

def load_inventory_items(csv_path):
    """Load inventory items data from CSV"""
    print("Loading inventory items...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        inventory_item = InventoryItem(
            id=row['id'],
            product_id=row['product_id'] if pd.notna(row['product_id']) else None,
            created_at=parse_datetime(row['created_at']),
            sold_at=parse_datetime(row['sold_at']),
            cost=row['cost'] if pd.notna(row['cost']) else None,
            product_category=row['product_category'] if pd.notna(row['product_category']) else None,
            product_name=row['product_name'] if pd.notna(row['product_name']) else None,
            product_brand=row['product_brand'] if pd.notna(row['product_brand']) else None,
            product_retail_price=row['product_retail_price'] if pd.notna(row['product_retail_price']) else None,
            product_department=row['product_department'] if pd.notna(row['product_department']) else None,
            product_sku=row['product_sku'] if pd.notna(row['product_sku']) else None,
            product_distribution_center_id=row['product_distribution_center_id'] if pd.notna(row['product_distribution_center_id']) else None
        )
        db.session.add(inventory_item)
    
    db.session.commit()
    print(f"Loaded {len(df)} inventory items")

def load_users(csv_path):
    """Load users data from CSV"""
    print("Loading users...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        user_data = UserData(
            id=row['id'],
            first_name=row['first_name'] if pd.notna(row['first_name']) else None,
            last_name=row['last_name'] if pd.notna(row['last_name']) else None,
            email=row['email'] if pd.notna(row['email']) else None,
            age=row['age'] if pd.notna(row['age']) else None,
            gender=row['gender'] if pd.notna(row['gender']) else None,
            state=row['state'] if pd.notna(row['state']) else None,
            street_address=row['street_address'] if pd.notna(row['street_address']) else None,
            postal_code=row['postal_code'] if pd.notna(row['postal_code']) else None,
            city=row['city'] if pd.notna(row['city']) else None,
            country=row['country'] if pd.notna(row['country']) else None,
            latitude=row['latitude'] if pd.notna(row['latitude']) else None,
            longitude=row['longitude'] if pd.notna(row['longitude']) else None,
            traffic_source=row['traffic_source'] if pd.notna(row['traffic_source']) else None,
            created_at=parse_datetime(row['created_at'])
        )
        db.session.add(user_data)
    
    db.session.commit()
    print(f"Loaded {len(df)} users")

def load_distribution_centers(csv_path):
    """Load distribution centers data from CSV"""
    print("Loading distribution centers...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        distribution_center = DistributionCenter(
            id=row['id'],
            name=row['name'] if pd.notna(row['name']) else None,
            latitude=row['latitude'] if pd.notna(row['latitude']) else None,
            longitude=row['longitude'] if pd.notna(row['longitude']) else None
        )
        db.session.add(distribution_center)
    
    db.session.commit()
    print(f"Loaded {len(df)} distribution centers")

def load_all_data():
    """Load all CSV data into the database"""
    dataset_path = Config.DATASET_PATH
    
    # Check if dataset path exists
    if not os.path.exists(dataset_path):
        print(f"Dataset path not found: {dataset_path}")
        return
    
    try:
        # Load all data
        load_products(os.path.join(dataset_path, 'products.csv'))
        load_orders(os.path.join(dataset_path, 'orders.csv'))
        load_order_items(os.path.join(dataset_path, 'order_items.csv'))
        load_inventory_items(os.path.join(dataset_path, 'inventory_items.csv'))
        load_users(os.path.join(dataset_path, 'users.csv'))
        load_distribution_centers(os.path.join(dataset_path, 'distribution_centers.csv'))
        
        print("✅ All data loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        db.session.rollback()

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Load data
        load_all_data() 