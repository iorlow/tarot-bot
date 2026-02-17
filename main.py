import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")

ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    phone = data.get("phone")

    print("Mensagem recebida de:", phone)

    payload = {
        "phone": phone,
        "message": "✨ Seja bem-vindo(a). O universo já está ouvindo você..."
    }

    response = requests.post(ZAPI_URL, json=payload)
    print("Status envio:", response.status_code)
    print("Responta Z-API:", response.text)
    
    return {"status": "ok"}
