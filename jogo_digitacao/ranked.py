ARQUIVO_RANKING = 'ranking.txt'

def salvar_pontos(nome, pontos):
    with open(ARQUIVO_RANKING, "a") as arquivo:
        arquivo.write(f'{nome},{pontos}\n')

def carregar_ranking():
    ranking = []
    try:
        with open(ARQUIVO_RANKING, "r") as arquivo:
            for linha in arquivo:
                nome, pontos = linha.strip().split(',')
                ranking.append((nome, int(pontos)))
    except FileNotFoundError:
        pass
    return ranking
