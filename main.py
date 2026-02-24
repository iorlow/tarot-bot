from fastapi import FastAPI, Request

from database import engine
from models import Base
from services import obter_ou_criar_usuario, atualizar_etapa
import variaveis

app = FastAPI()

# Cria tabelas se não existirem
Base.metadata.create_all(engine)

@app.post("/webhook")
async def webhook(request: Request):
    if data.get("fromMe"):
        print("Mensagem ignorada (enviada pelo próprio BOT)")
        return {"status": "ignored"}
    else:
        body = await request.json()
        # Ajuste conforme payload real da Z-API
        telefone = body.get("phone")
        mensagem = body.get("message")
    
        if not telefone:
            return {"erro": "Telefone não informado"}
    
        usuario = obter_ou_criar_usuario(telefone)
    
        # Exemplo simples de fluxo
        if usuario.etapa_fluxo == "inicio":
            
            nova_etapa = "aguardando_descricao"
            
        elif usuario.etapa_fluxo == "aguardando_descricao":
            
            nova_etapa = "finalizado"
            
        else:
            
            nova_etapa = "inicio"
    
            
        usuario = atualizar_etapa(usuario.id, nova_etapa)
        print("Telefone do usuário: ", usuario.telefone)
    
        return {
            "status": "ok",
            "usuario_id": usuario.id,
            "etapa_atual": usuario.etapa_fluxo
        }
