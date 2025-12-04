import random
import os

ARQUIVO_FRASES = "frases.txt"

# Frases padrão caso o arquivo não exista
FRASES_PADRAO = [
    "A prática leva à perfeição.",a
    "Nunca desista dos seus sonhos.",
    "O conhecimento é poder.",
    "A persistência é o caminho do êxito.",
    "Seja a mudança que você quer ver no mundo.",
    "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
    "Acredite em si mesmo e tudo será possível.",
    "Grandes conquistas requerem grandes esforços.",
    "O futuro pertence àqueles que acreditam na beleza de seus sonhos.",
    "Você é mais forte do que imagina."
]

def carregar_frases():
    # Tenta carregar do arquivo
    if os.path.exists(ARQUIVO_FRASES):
        try:
            with open(ARQUIVO_FRASES, "r", encoding="utf-8") as arquivo:
                frases = [linha.strip() for linha in arquivo if linha.strip()]
                if frases:
                    return frases
        except Exception as e:
            print(f"Erro ao carregar frases: {e}")
    
    # Se não conseguiu carregar, cria o arquivo com frases padrão
    criar_arquivo_frases_padrao()
    return FRASES_PADRAO

def criar_arquivo_frases_padrao():
    """Cria arquivo frases.txt com frases padrão"""
    try:
        with open(ARQUIVO_FRASES, "w", encoding="utf-8") as arquivo:
            for frase in FRASES_PADRAO:
                arquivo.write(frase + "\n")
        print(f"Arquivo {ARQUIVO_FRASES} criado com frases padrão.")
    except Exception as e:
        print(f"Erro ao criar arquivo de frases: {e}")

def gerar_texto():
    frases = carregar_frases()
    return random.choice(frases)

def adicionar_frase(nova_frase):
    """Adiciona uma nova frase ao arquivo"""
    try:
        with open(ARQUIVO_FRASES, "a", encoding="utf-8") as arquivo:
            arquivo.write(nova_frase.strip() + "\n")
        return True
    except Exception as e:
        print(f"Erro ao adicionar frase: {e}")
        return False
