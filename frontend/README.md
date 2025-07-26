# Customer Support Chatbot - Frontend

This is the frontend UI for the Customer Support Chatbot for an E-commerce Clothing Site.

## Features

- **Modern Chat Interface**: Clean, responsive design with smooth animations
- **Real-time Communication**: Connects to the backend API for chatbot responses
- **Quick Suggestions**: Pre-built suggestion buttons for common queries
- **Status Indicators**: Shows connection status to the backend
- **Mobile Responsive**: Works perfectly on desktop and mobile devices

## Setup

1. Open `index.html` in a web browser
2. Make sure the backend server is running on `http://localhost:5000`
3. Start chatting!

## Usage

### Quick Suggestions
Click on any of the suggestion buttons to quickly ask common questions:
- **Top Products**: Get the top 5 most sold products
- **Order Status**: Check order status by ID
- **Check Stock**: Check inventory levels
- **Product Info**: Get general product information

### Manual Input
Type your questions in the input field and press Enter or click the send button.

## File Structure

- `index.html` - Main HTML structure
- `styles.css` - Modern CSS styling with animations
- `script.js` - JavaScript functionality and API communication

## API Integration

The frontend communicates with the backend API at `http://localhost:5000/api`:
- `GET /api/health` - Health check
- `POST /api/chat` - Send messages and get responses

## Design Features

- **Gradient Background**: Modern purple gradient theme
- **Smooth Animations**: Fade-in effects and hover animations
- **Typing Indicators**: Shows when the bot is processing
- **Status Indicators**: Real-time connection status
- **Responsive Design**: Adapts to different screen sizes

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Development

To modify the frontend:
1. Edit the HTML structure in `index.html`
2. Update styles in `styles.css`
3. Modify functionality in `script.js`
4. Refresh the browser to see changes 