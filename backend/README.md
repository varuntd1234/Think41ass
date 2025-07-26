# Customer Support Chatbot - Backend

This is the backend service for the Customer Support Chatbot for an E-commerce Clothing Site.

## Features

- **Top Products Query**: Get the top 5 most sold products
- **Order Status**: Check the status of any order by ID
- **Inventory Status**: Check stock levels for specific products
- **Product Information**: Get general product statistics

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/api/health`
- Returns the health status of the API

### Chat Endpoint
- **POST** `/api/chat`
- Request body: `{"message": "your question here"}`
- Returns chatbot response

## Example Queries

1. "What are the top 5 most sold products?"
2. "Show me the status of order ID 12345"
3. "How many Classic T-Shirts are left in stock?"
4. "Tell me about your products"

## Data Sources

The chatbot uses the following CSV datasets:
- `products.csv` - Product information
- `orders.csv` - Order details
- `order_items.csv` - Individual order items
- `inventory_items.csv` - Inventory tracking
- `users.csv` - Customer information
- `distribution_centers.csv` - Distribution center locations 