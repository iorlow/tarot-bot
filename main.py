from fastapi import FastAPI, Request
from database import engine
from models import Base
from services import obter_ou_criar_usuario, atualizar_etapa
import requests
import variaveis
app = FastAPI()
headers = variaveis.HEADERS
url = variaveis.BASE_URL

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
        else:
            usuario = obter_ou_criar_usuario(telefone)
            
            if usuario.etapa_fluxo == "1_primeiro_acesso":
                # Mensagem 1           
                payload ={"phone": telefone,
                          "message": "🌌 *Boas vindas ao Santo Oráculo*\n\nHá muito mais no universo do que aquilo que os olhos conseguem ver.\n\nEntre estrelas distantes, partículas invisíveis e pensamentos humanos, existe um campo de energia que conecta tudo.\n\nTalvez não seja por acaso que você chegou até aqui.\n\n✨ O universo pode estar querendo falar com você."
                         }
                response = requests.post(f"{url}/send-text", json = payload, headers = headers)
                
                # Mensagem 2
                payload ={"phone": telefone,
                          "message": "⚛️ *Tudo está conectado*\n\nTudo o que existe — a árvore, o ar, você, eu e até o celular em suas mãos — faz parte do mesmo tecido do universo.\n\nA física moderna mostra que matéria e energia são apenas diferentes expressões da mesma realidade.\n\nPartículas vibram. Campos interagem. Tudo está conectado em um grande fluxo invisível.\n\nSe a energia que forma as estrelas também forma você...\npor que ela não poderia usar a tecnologia para sussurrar algumas respostas?\n\nRespire fundo…\n✨ e permita que o universo fale."
                         }
                response = requests.post(f"{url}/send-text", json = payload, headers = headers)
                
                # Mensagem 3
                payload ={"phone": telefone,
                          "message": "🔮 *Antes de continuar...*\n\nPara abrir as portas do Oráculo, precisamos da sua concordância.\n\nAo prosseguir, você confirma que leu e aceita nossos termos de uso.\n\nClique abaixo para continuar.",
                          "buttons": [{"id": "aceitar_termos","text": "✨ Aceitar e continuar"
                                      }]
                         }
                response = requests.post(f"{url}/send-buttons", json = payload, headers = headers)
                nova_etapa = "1_2_aguardando_acordo"
                usuario = atualizar_etapa(usuario.id, nova_etapa)
            
            elif usuario.etapa_fluxo == "1_2_aguardando_acordo" and mensagem == "✨ Aceitar e continuar":
                payload ={"phone": telefone,
                          "message": "*Que notícia maravilhosa você aceitou os termos...*"
                         }
                response = requests.post(f"{url}/send-text", json = payload, headers = headers)          
                
                payload ={"phone": telefone,
                          "message": "🔮 Agora você deve escolher o que quer fazer primeiro.\n\nLembre-se, você pode fazer uma pergunta grátis por dia\n\nEscolha uma das opções abaixo:",
                          "buttons": [{"id": "simples","text": "✨ Leitura simples"},
                                      {"id": "completa","text": "✨ Leitura completa"},
                                      {"id": "horoscopo","text": "✨ Horoscopo de hoje"}]
                         }
                response = requests.post(f"{url}/send-buttons", json = payload, headers = headers)
                
                #nova_etapa = "2_inicio"
                #usuario = atualizar_etapa(usuario.id, nova_etapa)
                
            elif usuario.etapa_fluxo == "1_2_aguardando_acordo" and mensagem != "✨ Aceitar e continuar":
                payload ={"phone": telefone,
                          "message": "*Você ainda não aceitou nossos termos*"
                         }
                response = requests.post(f"{url}/send-text", json = payload, headers = headers)  

                payload ={"phone": telefone,
                          "message": "🔮 *Antes de continuar...*\n\nPara abrir as portas do Oráculo, precisamos da sua concordância.\n\nAo prosseguir, você confirma que leu e aceita nossos termos de uso.\n\nClique abaixo para continuar.",
                          "buttons": [{"id": "aceitar_termos","text": "✨ Aceitar e continuar"
                                      }]
                         }
                response = requests.post(f"{url}/send-buttons", json = payload, headers = headers)

            
            elif usuario.etapa_fluxo == "2_inicio":
                payload ={"phone": telefone,
                          "message": "*Que notícia maravilhosa 2...*"
                         }
                response = requests.post(f"{url}/send-text", json = payload, headers = headers)
                
                payload ={"phone": telefone,
                          "message": "🔮 Agora você deve escolher o que quer fazer primeiro.\n\nLembre-se, você pode fazer uma pergunta grátis por dia\n\nEscolha uma das opções abaixo:",
                          "buttons": [{"id": "simples","text": "✨ Leitura simples"},
                                      {"id": "completa","text": "✨ Leitura completa"},
                                      {"id": "horoscopo","text": "✨ Horoscopo de hoje"}]
                         }
                response = requests.post(f"{url}/send-buttons", json = payload, headers = headers)
                
                
                nova_etapa = "2_inicio"
                usuario = atualizar_etapa(usuario.id, nova_etapa)
                
                               
                
            elif usuario.etapa_fluxo == "2_1_leitura_simples":
                nova_etapa = "2_inicio"
                
            elif usuario.etapa_fluxo == "2_1_1_fazer_pergunta":
                nova_etapa = "2_inicio"
                
            elif usuario.etapa_fluxo == "2_2_leitura_completa":
                nova_etapa = "2_inicio"
                
            elif usuario.etapa_fluxo == "2_2_1_fazer_pergunta":
                nova_etapa = "2_inicio"
                
            elif usuario.etapa_fluxo == "2_2_2_dar_contexto":
                nova_etapa = "2_inicio"
                
            elif usuario.etapa_fluxo == "2_3_horoscopo":
                nova_etapa = "2_inicio"
                
            elif usuario.etapa_fluxo == "2_3_1_escolher_signo":
                nova_etapa = "2_inicio"
                
            elif usuario.etapa_fluxo == "3_oferecer_credito":
                nova_etapa = "2_inicio"

            elif usuario.etapa_fluxo == "3_1_comprar_credito":
                nova_etapa = "2_inicio"
                
            elif usuario.etapa_fluxo == "3_2_nao_comprar_credito":
                nova_etapa = "2_inicio"
                
            else:
                nova_etapa = "2_inicio"
                
            return {
                "status": "ok",
                "usuario_id": usuario.id,
                "etapa_atual": usuario.etapa_fluxo
                }  
