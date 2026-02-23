from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Usuario
from database import engine


def obter_ou_criar_usuario(telefone: str, nome: str = None):
    with Session(engine) as session:
        usuario = session.query(Usuario).filter_by(telefone=telefone).first()

        if usuario:
            return usuario

        novo_usuario = Usuario(
            telefone=telefone,
            nome=nome,
            etapa_fluxo="inicio"
        )

        session.add(novo_usuario)

        try:
            session.commit()
            session.refresh(novo_usuario)
            return novo_usuario

        except IntegrityError:
            session.rollback()
            return session.query(Usuario).filter_by(telefone=telefone).first()
