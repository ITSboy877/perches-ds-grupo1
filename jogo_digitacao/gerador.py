import random

ARQUIVO_FRASES = "frases.txt"

def carregar_frases():
    try:
        with open(ARQUIVO_FRASES, "r", encoding="utf-8") as arquivo:
            return [linha.strip() for linha in arquivo if linha.strip()]
    except FileNotFoundError:
        return ["Nenhuma frase encontrada. Crie o arquivo frases.txt."]

def gerar_texto():
    frases = carregar_frases()
    return random.choice(frases)
