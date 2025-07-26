from models import db, Conversation, Message, Product, Order, OrderItem, InventoryItem, UserData
from sqlalchemy import func, and_
import re
from datetime import datetime

class ChatService:
    """Service class for handling chat functionality and business logic"""
    
    @staticmethod
    def process_chat_message(user_message, conversation_id=None, user_id=None):
        """
        Process a user message and return AI response
        """
        try:
            # Create conversation if not provided
            if not conversation_id and user_id:
                conversation = Conversation(user_id=user_id, title="New Chat")
                db.session.add(conversation)
                db.session.commit()
                conversation_id = conversation.id
            elif conversation_id:
                conversation = Conversation.query.get(conversation_id)
                if not conversation:
                    return {"error": "Conversation not found"}, 404
            else:
                return {"error": "Either conversation_id or user_id is required"}, 400
            
            # Save user message
            user_msg = Message(
                conversation_id=conversation_id,
                role='user',
                content=user_message
            )
            db.session.add(user_msg)
            
            # Generate AI response
            ai_response = ChatService._generate_response(user_message)
            
            # Save AI response
            ai_msg = Message(
                conversation_id=conversation_id,
                role='assistant',
                content=ai_response
            )
            db.session.add(ai_msg)
            db.session.commit()
            
            return {
                "conversation_id": conversation_id,
                "user_message": user_message,
                "ai_response": ai_response,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
    
    @staticmethod
    def _generate_response(user_message):
        """
        Generate AI response based on user message
        """
        message_lower = user_message.lower()
        
        # Check for different types of queries
        if any(word in message_lower for word in ['top', 'best', 'most sold', 'popular']):
            return ChatService._handle_top_products_query(message_lower)
        
        elif any(word in message_lower for word in ['order', 'status', 'track']):
            return ChatService._handle_order_status_query(message_lower)
        
        elif any(word in message_lower for word in ['stock', 'inventory', 'available', 'left']):
            return ChatService._handle_inventory_query(message_lower)
        
        elif any(word in message_lower for word in ['product', 'item', 'catalog']):
            return ChatService._handle_product_query(message_lower)
        
        else:
            return ChatService._handle_general_query(message_lower)
    
    @staticmethod
    def _handle_top_products_query(message):
        """Handle queries about top selling products"""
        try:
            # Query to get top selling products
            top_products = db.session.query(
                Product.name,
                Product.brand,
                Product.category,
                func.count(OrderItem.id).label('sales_count')
            ).join(OrderItem, Product.id == OrderItem.product_id)\
             .group_by(Product.name, Product.brand, Product.category)\
             .order_by(func.count(OrderItem.id).desc())\
             .limit(5).all()
            
            if not top_products:
                return "I couldn't find any sales data for products."
            
            response = "Here are the top 5 most sold products:\n\n"
            for i, (name, brand, category, sales_count) in enumerate(top_products, 1):
                response += f"{i}. {name} ({brand}) - {category} - {sales_count} units sold\n"
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error while retrieving top products: {str(e)}"
    
    @staticmethod
    def _handle_order_status_query(message):
        """Handle queries about order status"""
        try:
            # Extract order ID from message
            order_id_match = re.search(r'(\d+)', message)
            if not order_id_match:
                return "Please provide an order ID. For example: 'Show me the status of order ID 12345'"
            
            order_id = int(order_id_match.group(1))
            
            # Query order information
            order = Order.query.filter_by(order_id=order_id).first()
            if not order:
                return f"Order ID {order_id} not found. Please check the order ID and try again."
            
            # Get order items
            order_items = OrderItem.query.filter_by(order_id=order_id).all()
            
            response = f"Order ID: {order_id}\n"
            response += f"Status: {order.status}\n"
            response += f"Created: {order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else 'N/A'}\n"
            response += f"Number of items: {order.num_of_item}\n"
            
            if order.shipped_at:
                response += f"Shipped: {order.shipped_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            if order.delivered_at:
                response += f"Delivered: {order.delivered_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            if order.returned_at:
                response += f"Returned: {order.returned_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error while retrieving order status: {str(e)}"
    
    @staticmethod
    def _handle_inventory_query(message):
        """Handle queries about inventory/stock levels"""
        try:
            # Extract product name from message
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
                        matching_product = Product.query.filter(
                            Product.name.ilike(f'%{word}%')
                        ).first()
                        if matching_product:
                            product_name = matching_product.name
                            break
            
            if not product_name:
                return "Please specify which product you'd like to check inventory for. For example: 'How many Classic T-Shirts are left in stock?'"
            
            # Query inventory information
            product = Product.query.filter_by(name=product_name).first()
            if not product:
                return f"Product '{product_name}' not found in our inventory."
            
            # Count available inventory (not sold)
            available_inventory = InventoryItem.query.filter(
                and_(
                    InventoryItem.product_id == product.id,
                    InventoryItem.sold_at.is_(None)
                )
            ).count()
            
            # Count total inventory
            total_inventory = InventoryItem.query.filter_by(product_id=product.id).count()
            
            response = f"Inventory Status for {product_name}:\n"
            response += f"Available in stock: {available_inventory} units\n"
            response += f"Total inventory: {total_inventory} units\n"
            response += f"Sold: {total_inventory - available_inventory} units"
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error while retrieving inventory information: {str(e)}"
    
    @staticmethod
    def _handle_product_query(message):
        """Handle general product information queries"""
        try:
            # Get product statistics
            total_products = Product.query.count()
            
            # Get top categories
            top_categories = db.session.query(
                Product.category,
                func.count(Product.id).label('count')
            ).filter(Product.category.isnot(None))\
             .group_by(Product.category)\
             .order_by(func.count(Product.id).desc())\
             .limit(5).all()
            
            # Get top brands
            top_brands = db.session.query(
                Product.brand,
                func.count(Product.id).label('count')
            ).filter(Product.brand.isnot(None))\
             .group_by(Product.brand)\
             .order_by(func.count(Product.id).desc())\
             .limit(5).all()
            
            response = f"Product Information:\n\n"
            response += f"Total products: {total_products}\n\n"
            response += f"Product Categories:\n"
            for category, count in top_categories:
                response += f"- {category}: {count} products\n"
            
            response += f"\nTop Brands:\n"
            for brand, count in top_brands:
                response += f"- {brand}: {count} products\n"
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error while retrieving product information: {str(e)}"
    
    @staticmethod
    def _handle_general_query(message):
        """Handle general queries and provide help"""
        return """I'm your customer support assistant! I can help you with:

1. **Top Products**: "What are the top 5 most sold products?"
2. **Order Status**: "Show me the status of order ID 12345"
3. **Inventory**: "How many Classic T-Shirts are left in stock?"
4. **Product Info**: "Tell me about your products"

Please ask me any of these questions or something similar!""" 