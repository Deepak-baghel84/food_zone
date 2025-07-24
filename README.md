# Food Zone - WhatsApp + Dialogflow Integration

This project integrates WhatsApp Business API with Dialogflow for a food ordering chatbot.

Note : Folder structure have possibly a problem will be update in 2-3 working days. 

## Features

- WhatsApp webhook integration
- Dialogflow API integration for natural language processing
- Food ordering system with menu items
- Order management (add/remove items, show total, confirm orders)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Dialogflow

1. Go to [Dialogflow Console](https://dialogflow.cloud.google.com/)
2. Create a new project or use existing one
3. Get your Project ID from the settings
4. Create a service account and download the JSON key file
5. Enable the Dialogflow API in Google Cloud Console

### 3. Configure Environment Variables

Update the following constants in `main.py`:

```python
# WhatsApp Configuration
VERIFY_TOKEN = "your_custom_verify_token"
ACCESS_TOKEN = "your_whatsapp_access_token"

# Dialogflow Configuration
DIALOGFLOW_PROJECT_ID = "your-dialogflow-project-id"
DIALOGFLOW_API_KEY = "your-dialogflow-api-key"
```

### 4. Dialogflow Intents

Make sure your Dialogflow agent has the following intents:
- `NewOrder` - Start a new order
- `Add.item` - Add items to order
- `remove_item` - Remove items from order
- `order_complete` - Complete the order

### 5. Run the Application

```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /webhook` - WhatsApp webhook verification
- `POST /webhook` - WhatsApp webhook for receiving messages
- `POST /webhook` - Dialogflow webhook for processing intents

## How it Works

1. User sends a message via WhatsApp
2. WhatsApp webhook receives the message
3. Text is sent to Dialogflow API for intent detection
4. Dialogflow response is sent back to WhatsApp
5. For order-related intents, the system processes the order logic

## Dialogflow API Integration

The `send_text_to_dialogflow()` function:
- Sends text to Dialogflow's detectIntent API
- Uses the user's phone number as session ID for context
- Extracts the fulfillment text from Dialogflow's response
- Returns the response to be sent back to WhatsApp

## Error Handling

- API errors are logged and default responses are sent
- Invalid orders are handled gracefully
- Missing items are reported to the user

## Security Notes

- Store API keys securely (use environment variables in production)
- Validate webhook signatures
- Implement rate limiting for production use


