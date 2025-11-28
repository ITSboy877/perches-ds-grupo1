import json
import os

ARQUIVO_RANKING = "ranking.json"

def carregar_ranking():
    if not os.path.exists(ARQUIVO_RANKING):
        return []
    try:
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            dados = json.load(f)
            lista = dados.get("ranking", [])
            return [(item["nome"], int(item["pontos"])) for item in lista]
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        return []

def salvar_pontos(nome, pontos):
    ranking = carregar_ranking()
    ranking.append((nome, int(pontos)))
    dados = {"ranking": [{"nome": n, "pontos": p} for n, p in ranking]}
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
