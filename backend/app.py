from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Conversation, Message, Product, Order, OrderItem, InventoryItem, UserData, DistributionCenter
from config import Config
import uuid
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    return app

app = create_app()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'message': 'Conversational AI Backend Service is running',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user = User(
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user.id,
            'email': user.email
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation for a user"""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({'error': 'user_id is required'}), 400
        
        # Verify user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create new conversation
        conversation = Conversation(
            user_id=data['user_id'],
            title=data.get('title', 'New Conversation')
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        return jsonify({
            'message': 'Conversation created successfully',
            'conversation_id': conversation.id,
            'title': conversation.title
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation with all messages"""
    try:
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        messages = []
        for message in conversation.messages:
            messages.append({
                'id': message.id,
                'role': message.role,
                'content': message.content,
                'created_at': message.created_at.isoformat()
            })
        
        return jsonify({
            'conversation_id': conversation.id,
            'title': conversation.title,
            'created_at': conversation.created_at.isoformat(),
            'messages': messages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations/<conversation_id>/messages', methods=['POST'])
def add_message(conversation_id):
    """Add a message to a conversation"""
    try:
        data = request.get_json()
        
        if not data or 'role' not in data or 'content' not in data:
            return jsonify({'error': 'role and content are required'}), 400
        
        # Verify conversation exists
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        # Create new message
        message = Message(
            conversation_id=conversation_id,
            role=data['role'],
            content=data['content']
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'message': 'Message added successfully',
            'message_id': message.id,
            'role': message.role,
            'content': message.content,
            'created_at': message.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<user_id>/conversations', methods=['GET'])
def get_user_conversations(user_id):
    """Get all conversations for a user"""
    try:
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        conversations = []
        for conv in user.conversations:
            conversations.append({
                'id': conv.id,
                'title': conv.title,
                'created_at': conv.created_at.isoformat(),
                'updated_at': conv.updated_at.isoformat(),
                'message_count': len(conv.messages)
            })
        
        return jsonify({
            'user_id': user_id,
            'conversations': conversations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Database statistics endpoints for testing
@app.route('/api/stats', methods=['GET'])
def get_database_stats():
    """Get database statistics"""
    try:
        stats = {
            'users': User.query.count(),
            'conversations': Conversation.query.count(),
            'messages': Message.query.count(),
            'products': Product.query.count(),
            'orders': Order.query.count(),
            'order_items': OrderItem.query.count(),
            'inventory_items': InventoryItem.query.count(),
            'user_data': UserData.query.count(),
            'distribution_centers': DistributionCenter.query.count()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 