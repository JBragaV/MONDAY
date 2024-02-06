import os


def criador_de_pastas(pasta_principal: str = "", pasta_secundaria: str = "", pasta_terciaria: str = "") -> str:
    # Passta onde irá ficar os documentos: documentos/recibos||escala||normas_atc/nome_docs
    """
    Função responsável por verificar se todas as pastas de informadas existem e, caso não exista, cria as pastas.
    :param pasta_principal: Nome da pasta principal informada pelo sistema
    :param pasta_secundaria: Nome da pasta secundária informada pelo sistema. Opcional
    :param pasta_terciaria: Nome da pasta terciária informada pelo sistema. Opcional
    :return: None
    """
    try:
        __pasta_raiz = "documentos"
        __caminho = ""

        if not os.path.exists(__pasta_raiz):
            os.mkdir(__pasta_raiz)
            __caminho = os.path.join(os.getcwd(), __pasta_raiz)

        if not os.path.exists(os.path.join(__pasta_raiz, pasta_principal)):
            os.mkdir(os.path.join(__pasta_raiz, pasta_principal))
            __caminho = os.path.join(os.getcwd(), __pasta_raiz, pasta_principal)

        if not os.path.exists(os.path.join(__pasta_raiz, pasta_principal, pasta_secundaria)):
            os.mkdir(os.path.join(__pasta_raiz, pasta_principal, pasta_secundaria))
            __caminho = os.path.join(os.getcwd(), __pasta_raiz, pasta_principal, pasta_secundaria)

        if not os.path.exists(os.path.join(__pasta_raiz, pasta_principal, pasta_secundaria, pasta_terciaria)):
            os.mkdir(os.path.join(os.path.join(__pasta_raiz, pasta_principal, pasta_secundaria, pasta_terciaria)))
            __caminho = os.path.join(os.getcwd(), __pasta_raiz, pasta_principal, pasta_secundaria, pasta_terciaria)

        return __caminho
    except Exception as e:
        print(e)
