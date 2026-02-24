import os
import requests

# Variáveis de ambiente
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")
BASE_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}"

# Métodos de envio de mensagens. Podem ser reutilizados para as demais mensagens
ZAPI_URL_TEXT = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text" #mensagem de texto
ZAPI_URL_BUTTON = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-button-list" #lista de botões
ZAPI_URL_BUTTON_ACTIONS = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-button-actions" #botões de ação

# Definição dos headers, pode ser reutilizado em todas as mensagens
headers={
    "Content-Type": "application/json",
    "Client-Token": ZAPI_CLIENT_TOKEN
        }

