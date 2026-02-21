import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

# Métodos de envio de mensagens. Podem ser reunilizados para as demais mensagens

ZAPI_URL_TEXT = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text" #mensagem de texto
ZAPI_URL_BUTTON = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-button-list" #lista de botões
ZAPI_URL_BUTTON_ACTIONS = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-button-actions" #botões de ação


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Payload recebido: ", data)
    if data.get("fromMe"):
        print("Mensagem ignorada (enviada pelo próprio BOT)")
        return {"status": "ignored"}
    
    phone = data.get("phone")
    texto = data.get("body","").lower()
    tipo = data.get("type")
    botao_id = data.get("selectedId") if tipo == "button" else "vazio"  
    
    print("Mensagem recebida de:", phone)
                                

    # Definição dos headers, pode ser reutilizado em todas as mensagens
    headers={
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN
            }
    
    if tipo = "button":
          if botao_id == "1":
              payload={"phone": phone,"message":"Você escolheu a opção 1"}
          elif botao_id == "2":
              payload={"phone": phone,"message":"Você escolheu a opção 2"}
          else:
              payload={"phone": phone,"message":"Nenhuma mensagem escolhida"}
          response = requests.post(ZAPI_URL_TEXT, json=payload, headers=headers)
          
    else:
          payload = {
                "phone": phone,
                "message": "✨ Desejamos as boas vindas! O universo já está ouvindo você... Escolha o que você quer fazer a seguir:",
                "buttonList": {
                    "buttons": [
                                  {
                                    "id": "1",
                                    "label": "Leitura básica (1 carta)"
                                  },
                                  {
                                    "id": "2",
                                    "label": "Leitura completa (7 cartas)"
                                  }
                               ]
                              }
                       }
          response = requests.post(ZAPI_URL_BUTTON, json=payload, headers=headers)

    print("Status envio:", response.status_code)
    print("Responta Z-API:", response.text)
    return {"status": "ok"}
