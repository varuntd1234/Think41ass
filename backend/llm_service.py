import os
import requests
import json
from config import Config

class LLMService:
    """Service class for integrating with Groq LLM API"""
    
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.api_key:
            print("Warning: GROQ_API_KEY not set. LLM features will be disabled.")
    
    def generate_response(self, user_message, conversation_history=None, context=None):
        """
        Generate AI response using Groq LLM
        """
        if not self.api_key:
            return self._fallback_response(user_message)
        
        try:
            # Build conversation context
            messages = self._build_messages(user_message, conversation_history, context)
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7,
                "stream": False
            }
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"Groq API error: {response.status_code} - {response.text}")
                return self._fallback_response(user_message)
                
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return self._fallback_response(user_message)
    
    def _build_messages(self, user_message, conversation_history=None, context=None):
        """
        Build messages array for the LLM
        """
        messages = []
        
        # System message with context
        system_message = self._get_system_prompt(context)
        messages.append({
            "role": "system",
            "content": system_message
        })
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Limit to last 10 messages
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    def _get_system_prompt(self, context=None):
        """
        Get system prompt with context about the e-commerce system
        """
        base_prompt = """You are a helpful customer support assistant for an e-commerce clothing website. You have access to the following information:

1. **Products**: Product catalog with categories, brands, pricing, and SKUs
2. **Orders**: Customer order information and status tracking
3. **Inventory**: Stock levels and availability for all products
4. **Users**: Customer information and demographics
5. **Distribution Centers**: Warehouse locations

Your capabilities:
- Answer questions about top-selling products
- Check order status by order ID
- Provide inventory/stock information
- Give general product information
- Ask clarifying questions when needed

Always be helpful, professional, and accurate. If you need more information to answer a question, ask for it politely."""
        
        if context:
            base_prompt += f"\n\nAdditional context: {context}"
        
        return base_prompt
    
    def _fallback_response(self, user_message):
        """
        Fallback response when LLM is not available
        """
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['top', 'best', 'most sold', 'popular']):
            return "I can help you find the top-selling products. Let me check our sales data for you."
        
        elif any(word in message_lower for word in ['order', 'status', 'track']):
            return "I can help you check your order status. Please provide your order ID."
        
        elif any(word in message_lower for word in ['stock', 'inventory', 'available', 'left']):
            return "I can check inventory levels for you. Which product would you like to know about?"
        
        elif any(word in message_lower for word in ['product', 'item', 'catalog']):
            return "I can provide information about our products. What would you like to know?"
        
        else:
            return "I'm here to help with your e-commerce questions! I can assist with product information, order status, inventory levels, and more. What can I help you with today?"
    
    def ask_clarifying_question(self, user_message, missing_info):
        """
        Generate a clarifying question when information is missing
        """
        if not self.api_key:
            return self._simple_clarifying_question(missing_info)
        
        try:
            clarifying_prompt = f"""The user asked: "{user_message}"

I need to ask a clarifying question because I'm missing: {missing_info}

Generate a polite, helpful clarifying question to get the missing information. Keep it short and friendly."""

            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful customer support assistant. Generate polite clarifying questions."
                },
                {
                    "role": "user",
                    "content": clarifying_prompt
                }
            ]
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return self._simple_clarifying_question(missing_info)
                
        except Exception as e:
            print(f"Error generating clarifying question: {str(e)}")
            return self._simple_clarifying_question(missing_info)
    
    def _simple_clarifying_question(self, missing_info):
        """
        Simple fallback clarifying questions
        """
        if 'order id' in missing_info.lower():
            return "Could you please provide your order ID? I need it to check the status for you."
        elif 'product' in missing_info.lower():
            return "Which product would you like me to check? Please let me know the product name."
        elif 'inventory' in missing_info.lower():
            return "I'd be happy to check inventory levels. Which specific product are you interested in?"
        else:
            return "I need a bit more information to help you properly. Could you please provide more details?" 