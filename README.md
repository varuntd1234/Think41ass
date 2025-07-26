# Conversational AI Full-Stack Application

A complete full-stack application featuring a conversational AI chatbot with React frontend, Flask backend, PostgreSQL database, and LLM integration using Groq API.

## 🚀 Features

### **Backend (Flask + PostgreSQL)**
- **RESTful API**: Complete chat API with conversation management
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **LLM Integration**: Groq API for intelligent responses
- **Data Processing**: E-commerce dataset integration
- **Health Checks**: Comprehensive monitoring endpoints

### **Frontend (React)**
- **Modern UI**: Responsive chat interface with real-time messaging
- **State Management**: React Context API with useReducer
- **Conversation History**: Side panel for past conversations
- **Connection Status**: Real-time backend connectivity monitoring
- **Error Handling**: Graceful error management and user feedback

### **Docker & Deployment**
- **Containerized**: Complete Docker setup for all services
- **Orchestration**: Docker Compose for easy deployment
- **Reverse Proxy**: Nginx configuration for production
- **Health Monitoring**: Built-in health checks for all services

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │◄──►│   (Flask)       │◄──►│  (PostgreSQL)   │
│   Port: 3000    │    │   Port: 5000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Nginx Proxy   │
                    │   Port: 80      │
                    └─────────────────┘
```

## 📋 Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository
- **Groq API Key**: For LLM functionality (optional for demo)

## 🚀 Quick Start

### **1. Clone the Repository**
```bash
git clone https://github.com/varuntd1234/Think41ass.git
cd Think41ass
```

### **2. Set Environment Variables**
Create a `.env` file in the root directory:
```bash
# Groq API Configuration (optional)
GROQ_API_KEY=your_groq_api_key_here

# Application Configuration
SECRET_KEY=your-secret-key-here

# Database Configuration (defaults provided in docker-compose)
DATABASE_URL=postgresql://postgres:postgres123@postgres:5432/conversational_ai
```

### **3. Start the Application**
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### **4. Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Nginx Proxy**: http://localhost:80
- **Database**: localhost:5432

## 🔧 Development Setup

### **Local Development (Without Docker)**

#### **Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://postgres:postgres123@localhost:5432/conversational_ai"
export GROQ_API_KEY="your_groq_api_key_here"

# Run the application
python app.py
```

#### **Frontend Setup**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

#### **Database Setup**
```bash
# Install PostgreSQL locally or use Docker
docker run -d \
  --name postgres-dev \
  -e POSTGRES_DB=conversational_ai \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres123 \
  -p 5432:5432 \
  postgres:13-alpine
```

## 📁 Project Structure

```
Think41ass/
├── backend/                    # Flask Backend
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── models.py              # SQLAlchemy models
│   ├── chat_service.py        # Chat business logic
│   ├── llm_service.py         # LLM integration
│   ├── load_data.py           # Data ingestion script
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── context/           # State management
│   │   ├── services/          # API services
│   │   └── ...
│   └── package.json
├── ecommerce-dataset/          # Sample dataset
├── docker-compose.yml          # Docker orchestration
├── Dockerfile.backend          # Backend container
├── Dockerfile.frontend         # Frontend container
├── nginx.conf                  # Nginx configuration
├── init-db.sql                 # Database initialization
└── README.md                   # This file
```

## 🐳 Docker Commands

### **Basic Commands**
```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Rebuild and start
docker-compose up --build

# Stop and remove volumes
docker-compose down -v
```

### **Service Management**
```bash
# Start specific service
docker-compose up backend

# Restart service
docker-compose restart frontend

# Scale services
docker-compose up --scale backend=2

# Check service status
docker-compose ps
```

### **Development Commands**
```bash
# Run backend tests
docker-compose exec backend python -m pytest

# Access database
docker-compose exec postgres psql -U postgres -d conversational_ai

# View container resources
docker stats
```

## 🔌 API Endpoints

### **Health Check**
- `GET /api/health` - Service health status

### **Chat**
- `POST /api/chat` - Send message and get AI response

### **Users**
- `POST /api/users` - Create new user

### **Conversations**
- `POST /api/conversations` - Create new conversation
- `GET /api/conversations/<id>` - Get conversation with messages
- `POST /api/conversations/<id>/messages` - Add message to conversation
- `GET /api/users/<id>/conversations` - Get user's conversations

### **Statistics**
- `GET /api/stats` - Database statistics

## 🧪 Testing

### **Backend Testing**
```bash
# Run backend tests
cd backend
python -m pytest

# Run with coverage
python -m pytest --cov=.
```

### **Frontend Testing**
```bash
# Run frontend tests
cd frontend
npm test

# Run with coverage
npm test -- --coverage
```

### **Integration Testing**
```bash
# Test API endpoints
curl -X GET http://localhost:5000/api/health

# Test chat functionality
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how can you help me?"}'
```

## 🔍 Monitoring & Debugging

### **Health Checks**
All services include health checks:
- **Backend**: `http://localhost:5000/api/health`
- **Frontend**: `http://localhost:3000`
- **Database**: Automatic PostgreSQL health check

### **Logs**
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### **Database Access**
```bash
# Connect to database
docker-compose exec postgres psql -U postgres -d conversational_ai

# View tables
\dt

# Query data
SELECT * FROM conversations LIMIT 5;
```

## 🚀 Deployment

### **Production Deployment**
```bash
# Set production environment variables
export NODE_ENV=production
export FLASK_ENV=production

# Build and deploy
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### **Environment Variables**
```bash
# Required for production
GROQ_API_KEY=your_production_groq_api_key
SECRET_KEY=your_production_secret_key
DATABASE_URL=your_production_database_url
```

## 🛠️ Troubleshooting

### **Common Issues**

#### **Backend Connection Issues**
```bash
# Check if backend is running
docker-compose ps

# Check backend logs
docker-compose logs backend

# Restart backend service
docker-compose restart backend
```

#### **Database Connection Issues**
```bash
# Check database status
docker-compose exec postgres pg_isready -U postgres

# Reset database
docker-compose down -v
docker-compose up postgres
```

#### **Frontend Build Issues**
```bash
# Clear node modules and rebuild
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### **Performance Optimization**
```bash
# Monitor resource usage
docker stats

# Optimize images
docker-compose build --no-cache

# Scale services
docker-compose up --scale backend=2 --scale frontend=2
```

## 📊 Performance Metrics

### **Resource Requirements**
- **Minimum**: 2GB RAM, 1 CPU core
- **Recommended**: 4GB RAM, 2 CPU cores
- **Production**: 8GB RAM, 4 CPU cores

### **Response Times**
- **API Health Check**: < 100ms
- **Chat Response**: < 2s (with LLM)
- **Database Queries**: < 500ms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the Conversational AI demonstration.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review the logs
- Create an issue on GitHub

---

**Repository**: https://github.com/varuntd1234/Think41ass

**Status**: ✅ All milestones completed and ready for deployment 