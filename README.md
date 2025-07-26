# Customer Support Chatbot for E-commerce Clothing Site

A complete customer support chatbot solution with backend API and modern frontend interface, designed to handle e-commerce queries using real dataset analysis.

## 🚀 Features

### Backend API
- **Flask REST API** with CORS support
- **Data Processing** using pandas for CSV analysis
- **Query Processing** for:
  - Top selling products
  - Order status tracking
  - Inventory management
  - Product information

### Frontend UI
- **Modern Chat Interface** with responsive design
- **Real-time Communication** with backend API
- **Quick Suggestion Buttons** for common queries
- **Connection Status Indicators**
- **Mobile Responsive** design

### Data Analysis
- **E-commerce Dataset** with 6 CSV files
- **Product Analytics** and sales tracking
- **Inventory Management** and stock levels
- **Order Processing** and status tracking

## 📋 Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- Modern web browser

## 🛠️ Installation & Setup

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/varuntd1234/Think41ass.git
   cd Think41ass
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:8000
   - Backend API: http://localhost:5000

### Option 2: Local Development

1. **Setup Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Setup Frontend:**
   ```bash
   cd frontend
   # Open index.html in a web browser
   # Or use a local server:
   python -m http.server 8000
   ```

## 🎯 Usage Examples

### Example Queries

1. **Top Products:**
   ```
   "What are the top 5 most sold products?"
   ```

2. **Order Status:**
   ```
   "Show me the status of order ID 12345"
   ```

3. **Inventory Check:**
   ```
   "How many Classic T-Shirts are left in stock?"
   ```

4. **Product Information:**
   ```
   "Tell me about your products"
   ```

### Quick Start

1. Open the frontend in your browser
2. Click on suggestion buttons or type your question
3. Get instant responses from the chatbot

## 📊 Dataset Information

The chatbot uses a comprehensive e-commerce dataset with:

- **Products**: Product catalog with categories, brands, and pricing
- **Orders**: Customer order information and status
- **Order Items**: Individual items within orders
- **Inventory**: Stock levels and availability
- **Users**: Customer information and demographics
- **Distribution Centers**: Warehouse locations

## 🔧 API Endpoints

### Health Check
- **GET** `/api/health`
- Returns API status and dataset loading information

### Chat Endpoint
- **POST** `/api/chat`
- Request: `{"message": "your question"}`
- Response: `{"message": "bot response", "timestamp": "..."}`

## 🏗️ Project Structure

```
Think41ass/
├── backend/
│   ├── app.py              # Flask API application
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── styles.css         # CSS styling
│   ├── script.js          # JavaScript functionality
│   └── README.md          # Frontend documentation
├── ecommerce-dataset/     # Dataset files
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
└── README.md             # This file
```

## 🐳 Docker Commands

### Build and Run
```bash
# Build the image
docker build -t chatbot-app .

# Run the container
docker run -p 5000:5000 -p 8000:8000 chatbot-app

# Or use docker-compose
docker-compose up --build
```

### Management
```bash
# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up --build --force-recreate
```

## 🧪 Testing

### Backend Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the top 5 most sold products?"}'
```

### Frontend Testing
1. Open http://localhost:8000 in your browser
2. Try the suggestion buttons
3. Test manual input with various queries

## 🔍 Troubleshooting

### Common Issues

1. **Backend not starting:**
   - Check if port 5000 is available
   - Verify Python dependencies are installed
   - Check dataset files are present

2. **Frontend not connecting:**
   - Ensure backend is running on localhost:5000
   - Check browser console for CORS errors
   - Verify API endpoints are accessible

3. **Docker issues:**
   - Check Docker is running
   - Verify ports are not in use
   - Check Docker logs for errors

## 📈 Performance

- **Backend**: Fast response times with pandas data processing
- **Frontend**: Smooth animations and real-time updates
- **Data**: Efficient CSV loading and query processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for educational and demonstration purposes.

## 🎉 Milestones Completed

- ✅ **Milestone 1**: Environment Setup
- ✅ **Milestone 2**: Dataset Setup
- ✅ **Milestone 3**: Backend Service
- ✅ **Milestone 4**: Frontend UI
- ✅ **Milestone 5**: Integration & Containerization

---

**Repository**: https://github.com/varuntd1234/Think41ass 