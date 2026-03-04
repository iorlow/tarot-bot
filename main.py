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
    
        # Fluxo de estado de mensagens

        tipo = ""
        mensagem = ""
        nova_etapa = ""

        if usuario.etapa_fluxo == "1_primeiro_acesso":
            tipo = "send-text"
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "2_inicio":
            tipo = "send-button-list"
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "2_1_leitura_simples":
            tipo = "send-text"
            nova_etapa = "2_inicio"
            mensagem = ""
                    
        elif usuario.etapa_fluxo == "2_1_1_fazer_pergunta":
            tipo = "send-text"
            nova_etapa = "2_inicio"
            mensagem = ""
        
        elif usuario.etapa_fluxo == "2_2_leitura_completa":
            tipo = "send-text"
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "2_2_1_fazer_pergunta":
            tipo = "send-text"
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "2_2_2_dar_contexto":
            tipo = ""
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "2_3_horoscopo":
            tipo = ""
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "2_3_1_escolher_signo":
            tipo = ""
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "3_oferecer_credito":
            tipo = ""
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "3_1_comprar_credito":
            tipo = ""
            nova_etapa = "2_inicio"
            mensagem = ""
            
        elif usuario.etapa_fluxo == "3_2_nao_comprar_credito":
            tipo = ""
            nova_etapa = "2_inicio"
            mensagem = ""
                        
        else:
            tipo = ""
            nova_etapa = "2_inicio"
            mensagem = ""
            
        payload={"phone": telefone,"message":mensagem}
        response = requests.post(f"{variaveis.BASE_URL}/tipo", json=payload, headers=variaveis.HEADERS)
        usuario = atualizar_etapa(usuario.id, nova_etapa)
    
    
        return {
            "status": "ok",
            "usuario_id": usuario.id,
            "etapa_atual": usuario.etapa_fluxo
        }
