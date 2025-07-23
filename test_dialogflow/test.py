from fastapi import FastAPI, Request, HTTPException
import uvicorn, os, uuid, requests
from google.cloud import dialogflow_v2 as dialogflow
import os

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "foody/theta-now-428108-k5-df16cb0640f0.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "foody-afby-e4470a543071.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

PROJECT_ID     = "foody-afby"

def detect_intent_df(text: str, session_id: str):
    print("request is received for sending message to whatsapp")
    client  = dialogflow.SessionsClient()
    print("client passed")
    session = client.session_path(PROJECT_ID, session_id)
    print("session passed")
    query_input = dialogflow.QueryInput(
        text=dialogflow.TextInput(text=text, language_code="en")
    )
    print("query_input passed")
    resp = client.detect_intent(request={"session": session, "query_input": query_input})

    qr   = resp.query_result
    return {
        "intent": qr.intent.display_name,
        "params": dict(qr.parameters),
        "contexts": qr.output_contexts,
        "reply": qr.fulfillment_text
    }

df = detect_intent_df("hi", "test-123456")
intent, params = df["intent"], df["params"]
print(f'{intent}, {params}')
