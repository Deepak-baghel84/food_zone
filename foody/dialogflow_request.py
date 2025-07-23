from google.cloud import dialogflow_v2 as dialogflow
from app import PROJECT_ID
from tokens import project_id, to




class dialogflow_handler():
    # 1) Helper to call Dialogflow
    def detect_intent_df(self,text: str, session_id: str):
      print("request is received for sending message to whatsapp")
      client  = dialogflow.SessionsClient()
      session = client.session_path(PROJECT_ID, session_id)
      query_input = dialogflow.QueryInput(
          text=dialogflow.TextInput(text=text, language_code="en")
      )
      resp = client.detect_intent(request={"session": session, "query_input": query_input})

      qr   = resp.query_result
      return {
          "intent": qr.intent.display_name,
          "params": dict(qr.parameters),
          "contexts": qr.output_contexts,
          "reply": qr.fulfillment_text
     }
    
    
    
    
    
    
    
    