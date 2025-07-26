from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load datasets
def load_datasets():
    """Load all CSV datasets into memory"""
    dataset_path = "../ecommerce-dataset/archive"
    
    try:
        products_df = pd.read_csv(f"{dataset_path}/products.csv")
        orders_df = pd.read_csv(f"{dataset_path}/orders.csv")
        order_items_df = pd.read_csv(f"{dataset_path}/order_items.csv")
        inventory_items_df = pd.read_csv(f"{dataset_path}/inventory_items.csv")
        users_df = pd.read_csv(f"{dataset_path}/users.csv")
        distribution_centers_df = pd.read_csv(f"{dataset_path}/distribution_centers.csv")
        
        return {
            'products': products_df,
            'orders': orders_df,
            'order_items': order_items_df,
            'inventory_items': inventory_items_df,
            'users': users_df,
            'distribution_centers': distribution_centers_df
        }
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return None

# Load datasets on startup
datasets = load_datasets()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Customer Support Chatbot API is running',
        'datasets_loaded': datasets is not None
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chatbot endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        if not datasets:
            return jsonify({
                'error': 'Datasets not loaded',
                'message': 'Please check if the dataset files are available'
            }), 500
        
        # Process the user message and generate response
        response = process_message(user_message)
        
        return jsonify({
            'message': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while processing your request'
        }), 500

def process_message(message):
    """Process user message and return appropriate response"""
    
    # Check for top products query
    if 'top' in message and ('product' in message or 'sold' in message):
        return get_top_products(message)
    
    # Check for order status query
    elif 'order' in message and ('status' in message or 'id' in message):
        return get_order_status(message)
    
    # Check for inventory/stock query
    elif any(word in message for word in ['stock', 'inventory', 'left', 'available']):
        return get_inventory_status(message)
    
    # Check for product information
    elif 'product' in message or 'item' in message:
        return get_product_info(message)
    
    # Default response
    else:
        return get_help_message()

def get_top_products(message):
    """Get top selling products"""
    try:
        # Count products sold by merging order_items with products
        sold_products = datasets['order_items'].merge(
            datasets['products'], 
            left_on='product_id', 
            right_on='id', 
            how='inner'
        )
        
        # Count sales by product
        product_sales = sold_products.groupby(['name', 'brand', 'category']).size().reset_index(name='sales_count')
        product_sales = product_sales.sort_values('sales_count', ascending=False)
        
        # Get top 5
        top_5 = product_sales.head(5)
        
        response = "Here are the top 5 most sold products:\n\n"
        for idx, row in top_5.iterrows():
            response += f"{idx + 1}. {row['name']} ({row['brand']}) - {row['category']} - {row['sales_count']} units sold\n"
        
        return response
        
    except Exception as e:
        return f"Sorry, I couldn't retrieve the top products information. Error: {str(e)}"

def get_order_status(message):
    """Get order status by order ID"""
    try:
        # Extract order ID from message
        import re
        order_id_match = re.search(r'(\d+)', message)
        
        if not order_id_match:
            return "Please provide an order ID. For example: 'Show me the status of order ID 12345'"
        
        order_id = int(order_id_match.group(1))
        
        # Find the order
        order = datasets['orders'][datasets['orders']['order_id'] == order_id]
        
        if order.empty:
            return f"Order ID {order_id} not found. Please check the order ID and try again."
        
        order_info = order.iloc[0]
        
        # Get order items
        order_items = datasets['order_items'][datasets['order_items']['order_id'] == order_id]
        
        response = f"Order ID: {order_id}\n"
        response += f"Status: {order_info['status']}\n"
        response += f"Created: {order_info['created_at']}\n"
        response += f"Number of items: {order_info['num_of_item']}\n"
        
        if pd.notna(order_info['shipped_at']):
            response += f"Shipped: {order_info['shipped_at']}\n"
        if pd.notna(order_info['delivered_at']):
            response += f"Delivered: {order_info['delivered_at']}\n"
        if pd.notna(order_info['returned_at']):
            response += f"Returned: {order_info['returned_at']}\n"
        
        return response
        
    except Exception as e:
        return f"Sorry, I couldn't retrieve the order status. Error: {str(e)}"

def get_inventory_status(message):
    """Get inventory status for products"""
    try:
        # Extract product name from message
        import re
        
        # Look for product names in the message
        product_name = None
        
        # Check for specific product mentions
        if 'classic t-shirt' in message or 'classic tshirt' in message:
            product_name = 'Classic T-Shirt'
        elif 't-shirt' in message or 'tshirt' in message:
            product_name = 'T-Shirt'
        else:
            # Try to extract any product name
            words = message.split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    matching_products = datasets['products'][
                        datasets['products']['name'].str.contains(word, case=False, na=False)
                    ]
                    if not matching_products.empty:
                        product_name = matching_products.iloc[0]['name']
                        break
        
        if not product_name:
            return "Please specify which product you'd like to check inventory for. For example: 'How many Classic T-Shirts are left in stock?'"
        
        # Get inventory for the product
        product = datasets['products'][datasets['products']['name'] == product_name]
        
        if product.empty:
            return f"Product '{product_name}' not found in our inventory."
        
        product_id = product.iloc[0]['id']
        
        # Count available inventory (not sold)
        available_inventory = datasets['inventory_items'][
            (datasets['inventory_items']['product_id'] == product_id) & 
            (datasets['inventory_items']['sold_at'].isna())
        ]
        
        total_inventory = datasets['inventory_items'][
            datasets['inventory_items']['product_id'] == product_id
        ]
        
        available_count = len(available_inventory)
        total_count = len(total_inventory)
        
        response = f"Inventory Status for {product_name}:\n"
        response += f"Available in stock: {available_count} units\n"
        response += f"Total inventory: {total_count} units\n"
        response += f"Sold: {total_count - available_count} units"
        
        return response
        
    except Exception as e:
        return f"Sorry, I couldn't retrieve the inventory information. Error: {str(e)}"

def get_product_info(message):
    """Get general product information"""
    try:
        # Count total products
        total_products = len(datasets['products'])
        
        # Get product categories
        categories = datasets['products']['category'].value_counts()
        
        # Get brands
        brands = datasets['products']['brand'].value_counts()
        
        response = f"Product Information:\n\n"
        response += f"Total products: {total_products}\n\n"
        response += f"Product Categories:\n"
        for category, count in categories.head(5).items():
            response += f"- {category}: {count} products\n"
        
        response += f"\nTop Brands:\n"
        for brand, count in brands.head(5).items():
            response += f"- {brand}: {count} products\n"
        
        return response
        
    except Exception as e:
        return f"Sorry, I couldn't retrieve the product information. Error: {str(e)}"

def get_help_message():
    """Return help message with available queries"""
    return """I'm your customer support chatbot! I can help you with:

1. **Top Products**: "What are the top 5 most sold products?"
2. **Order Status**: "Show me the status of order ID 12345"
3. **Inventory**: "How many Classic T-Shirts are left in stock?"
4. **Product Info**: "Tell me about your products"

Please ask me any of these questions or something similar!"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 