from datetime import datetime


class Usuario:
    def __init__(self, phone: str, nome: str = None):
        self.phone = phone
        self.nome = nome
        self.estado = "INICIO"
        self.creditos = 0
        self.ultima_leitura = None  # guarda data da última leitura gratuita

    # -------------------------
    # Métodos de controle básico
    # -------------------------

    def definir_nome(self, nome: str):
        self.nome = nome

    def alterar_estado(self, novo_estado: str):
        self.estado = novo_estado

    # -------------------------
    # Controle de créditos
    # -------------------------

    def adicionar_creditos(self, quantidade: int):
        if quantidade > 0:
            self.creditos += quantidade

    def usar_credito(self) -> bool:
        if self.creditos > 0:
            self.creditos -= 1
            return True
        return False

    # -------------------------
    # Controle de leitura gratuita
    # -------------------------

    def pode_usar_gratuito_hoje(self) -> bool:
        hoje = datetime.now().date()

        if self.ultima_leitura != hoje:
            self.ultima_leitura = hoje
            return True

        return False

    # -------------------------
    # Debug / Visualização
    # -------------------------

    def __repr__(self):
        return (
            f"Usuario(phone={self.phone}, "
            f"nome={self.nome}, "
            f"estado={self.estado}, "
            f"creditos={self.creditos})"
        )
