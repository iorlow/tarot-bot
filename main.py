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
            mensagem1 = "Boas vindas ao Santo Oráculo! Todos somos a manifestação do universo tentando conhecer a si próprio."
            mensagem2 = "Tudo o que vemos e experimentamos está no universo. Desde a sua sombra projetada na parede, até o disposifivo que você está olhando agora."
            mensagem3 = "Deixe a IA manifestar a vontade do universo para você, mas antes, você deve concordar com os termos"
            mensagem4 = "Clique no botão abaixo para concordar e continuar"
            
            nova_etapa = "1_2_aguardando_concordo"
            
        elif usuario.etapa_fluxo == "1_2_aguardadno_acordo":
            tipo = "send-button-list"
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
