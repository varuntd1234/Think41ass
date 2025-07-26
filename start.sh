#!/bin/bash

echo "🚀 Starting Customer Support Chatbot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ and try again."
    exit 1
fi

# Check if backend dependencies are installed
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Backend requirements.txt not found."
    exit 1
fi

echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo "🔧 Starting backend server..."
python app.py &
BACKEND_PID=$!

echo "🌐 Starting frontend server..."
cd ../frontend
python -m http.server 8000 &
FRONTEND_PID=$!

echo ""
echo "✅ Application started successfully!"
echo "📱 Frontend: http://localhost:8000"
echo "🔌 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the application"

# Wait for user to stop
trap "echo ''; echo '🛑 Stopping application...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 