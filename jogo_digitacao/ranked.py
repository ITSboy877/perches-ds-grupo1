import json
import os
from datetime import datetime

ARQUIVO_RANKING = "ranking.json"

def carregar_ranking():
    """Carrega o ranking do arquivo JSON"""
    if not os.path.exists(ARQUIVO_RANKING):
        return []
    
    try:
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            dados = json.load(f)
            lista = dados.get("ranking", [])
            
            # Retorna tupla (nome, pontos, wpm, precisao, modo, data)
            resultado = []
            for item in lista:
                resultado.append((
                    item.get("nome", "Jogador"),
                    int(item.get("pontos", 0)),
                    float(item.get("wpm", 0)),
                    float(item.get("precisao", 0)),
                    item.get("modo", "normal"),
                    item.get("data", "")
                ))
            return resultado
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as e:
        print(f"⚠️ Erro ao carregar ranking: {e}")
        return []

def salvar_pontos(nome, pontos, wpm=0, precisao=0, modo="normal"):
    """Salva uma nova pontuação no ranking"""
    ranking = carregar_ranking()
    
    nova_entrada = {
        "nome": nome,
        "pontos": int(pontos),
        "wpm": float(wpm),
        "precisao": float(precisao),
        "modo": modo,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Converte ranking para dicionários
    ranking_dict = []
    for r in ranking:
        ranking_dict.append({
            "nome": r[0],
            "pontos": r[1],
            "wpm": r[2],
            "precisao": r[3],
            "modo": r[4],
            "data": r[5]
        })
    
    ranking_dict.append(nova_entrada)
    
    # Salva no arquivo
    dados = {"ranking": ranking_dict}
    try:
        with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"✅ Pontuação salva: {nome} - {pontos} pontos ({modo})")
    except Exception as e:
        print(f"❌ Erro ao salvar ranking: {e}")

def obter_top_por_modo(modo, limite=10):
    """Retorna top jogadores de um modo específico"""
    ranking = carregar_ranking()
    filtrado = [r for r in ranking if r[4] == modo]
    filtrado.sort(key=lambda x: x[1], reverse=True)
    return filtrado[:limite]

def obter_melhor_pontuacao_usuario(nome):
    """Retorna a melhor pontuação de um usuário"""
    ranking = carregar_ranking()
    usuario_scores = [r[1] for r in ranking if r[0].lower() == nome.lower()]
    return max(usuario_scores) if usuario_scores else 0

def obter_posicao_usuario(nome, modo):
    """Retorna a posição do usuário no ranking do modo"""
    ranking = obter_top_por_modo(modo, limite=1000)
    for idx, entrada in enumerate(ranking, 1):
        if entrada[0].lower() == nome.lower():
            return idx
    return None
