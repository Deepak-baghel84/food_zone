# main.py
from fastapi import FastAPI, Request
import uvicorn, os, requests
from pydantic import BaseModel
from typing import Any, List, Dict
import random
from handler import intent_handler
from dialogflow_request import dialogflow_handler

class WhatsAppChangeValue(BaseModel):
    messages: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class WhatsAppChange(BaseModel):
    value: WhatsAppChangeValue

class WhatsAppEntry(BaseModel):
    changes: List[WhatsAppChange]

class WhatsAppWebhook(BaseModel):
    entry: List[WhatsAppEntry]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "foody-afby-e4470a543071.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

app = FastAPI()

# In‑memory store: phone_number → order_id
user_orders = {}

# In‑memory store: order_id → order data
orders = {}

PRICES = {"Pizza":199, "Burger":149, "Pasta":179, "Coke":49}       #add your food items

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")      # whatsapp token

phone_id =" "                             # phone_id of the whatsapp number
PROJECT_ID  = " "                         # project id of the google cloud project 
to = " "                                   # phone number of the user



# 2) Helper to send a WhatsApp text
class send_whatsapp():
    def send(self,phone_id: str, to: str, text: str):
        print("request is received for sending message to whatsapp")
        url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
        payload = {"messaging_product":"whatsapp","recipient_type":"individual","to":to,"type":"text","text":{"body":text}}
        headers = {"Authorization":f"Bearer {WHATSAPP_TOKEN}","Content-Type":"application/json"}
        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()
        print("message is sent to whatsapp")
        

# 4) Main webhook receiver
@app.post("/webhook")
async def webhook(payload: WhatsAppWebhook):
    # no more `await req.json()`, you already have `payload`
    msg = payload.entry[0].changes[0].value.messages[0]
    text = msg["text"]["body"]
    user = msg["from"]
    phone_id = payload.entry[0].changes[0].value.metadata["phone_number_id"]
    # …rest of your logic…
    print(f"text {text} and user {user} and phone_id {phone_id}")
        # --- Dialogflow roundtrip ---
    print("message is passed to dialogflow")
    df = dialogflow_handler.detect_intent_df(text, session_id=user)
    intent, params = df["intent"], df["params"]
    print(f"intent {intent} and parameters {params} are received")

        # --- Dispatch to handler ---
    if intent == "Default_Welcome_Intent":
        intent_handler.Default_Welcome_Intent(phone_id,user)
    if intent == "NewOrder":
        intent_handler.handle_new_order(phone_id, user)
    elif intent == "AddItemIntent":
        intent_handler.handle_add_item(phone_id, user, params)
    elif intent == "remove_item":
        intent_handler.handle_remove_item(phone_id, user, params)
    elif intent == "ShowTotalIntent":
        intent_handler.handle_show_total(phone_id, user)
    elif intent == "ConfirmOrderIntent":
        intent_handler.handle_confirm(phone_id, user)
    else:
            # fallback
        send_whatsapp.send(phone_id, user,
            "Sorry, I didn’t understand. Try “New Order” or “Show total.”"
        )

    return {"status":"ok"}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
