from fastapi import FastAPI, Request

from database import engine
from models import Base
from services import obter_ou_criar_usuario, atualizar_etapa
import requests
import variaveis

app = FastAPI()

# Cria tabelas se não existirem
Base.metadata.create_all(engine)

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    if body.get("fromMe"):
        print("Mensagem ignorada (enviada pelo próprio BOT)")
        return {"status": "ignored"}
    else:
        # Ajuste conforme payload real da Z-API
        telefone = body.get("phone")
        mensagem = body.get("message")
    
        if not telefone:
            return {"erro": "Telefone não informado"}
    
        usuario = obter_ou_criar_usuario(telefone)
    
        # Exemplo simples de fluxo
        if usuario.etapa_fluxo == "inicio":
            
            payload={"phone": telefone,"message":"Mensagem de início"}
            response = requests.post(f"{variaveis.BASE_URL}/send-text", json=payload, headers=variaveis.HEADERS)
            nova_etapa = "aguardando_descricao"
            
        elif usuario.etapa_fluxo == "aguardando_descricao":
            
            payload={"phone": telefone,"message":"mensagem de aguardando descricao"}
            response = requests.post(f"{variaveis.BASE_URL}/send-text", json=payload, headers=variaveis.HEADERS)
            nova_etapa = "finalizado"
            
        else:
            payload={"phone": telefone,"message":"Atendimento finalizado"}
            response = requests.post(f"{variaveis.BASE_URL}/send-text", json=payload, headers=variaveis.HEADERS)
            nova_etapa = "inicio"
    
            
        usuario = atualizar_etapa(usuario.id, nova_etapa)
        print("Telefone do usuário: ", usuario.telefone)
    
        return {
            "status": "ok",
            "usuario_id": usuario.id,
            "etapa_atual": usuario.etapa_fluxo
        }
