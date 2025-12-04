import json
import os
import hashlib
from datetime import datetime

ARQUIVO_USUARIOS = "usuarios.json"

def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {"usuarios": []}
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if "usuarios" not in dados or not isinstance(dados["usuarios"], list):
                return {"usuarios": []}
            return dados
    except (json.JSONDecodeError, OSError):
        return {"usuarios": []}

def salvar_usuarios(dados):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def cadastrar_usuario(usuario, senha):
    usuario = usuario.strip()
    senha = senha.strip()
    if not usuario or not senha:
        return False, "Usuário e senha não podem ser vazios."
    if len(usuario) < 3:
        return False, "Usuário deve ter pelo menos 3 caracteres."
    if len(senha) < 4:
        return False, "A senha deve ter pelo menos 4 caracteres."
    
    dados = carregar_usuarios()
    for u in dados["usuarios"]:
        if u["usuario"].lower() == usuario.lower():
            return False, "Usuário já existe."
    
    novo_usuario = {
        "usuario": usuario,
        "senha": _hash_senha(senha),
        "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_partidas": 0,
        "melhor_wpm": 0,
        "melhor_precisao": 0,
        "conquistas": [],
        "xp": 0 
    }
    
    dados["usuarios"].append(novo_usuario)
    salvar_usuarios(dados)
    return True, "Usuário cadastrado com sucesso!"

def verificar_login(usuario, senha):
    usuario = usuario.strip()
    senha = senha.strip()
    dados = carregar_usuarios()
    senha_hash = _hash_senha(senha)
    for u in dados["usuarios"]:
        if u["usuario"].lower() == usuario.lower() and u["senha"] == senha_hash:
            return True
    return False

def atualizar_stats_usuario(usuario, wpm, precisao):
    """Atualiza as estatísticas do usuário"""
    dados = carregar_usuarios()
    for u in dados["usuarios"]:
        if u["usuario"].lower() == usuario.lower():
            u["total_partidas"] = u.get("total_partidas", 0) + 1
            u["melhor_wpm"] = max(u.get("melhor_wpm", 0), wpm)
            u["melhor_precisao"] = max(u.get("melhor_precisao", 0), precisao)
            break
    salvar_usuarios(dados)

def adicionar_conquista(usuario, conquista_id):
    """Adiciona conquista ao usuário e retorna XP ganho"""
    import config
    dados = carregar_usuarios()
    xp_ganho = 0
    for u in dados["usuarios"]:
        if u["usuario"].lower() == usuario.lower():
            if "conquistas" not in u:
                u["conquistas"] = []
            if conquista_id not in u["conquistas"]:
                u["conquistas"].append(conquista_id)
                conquista_info = config.CONQUISTAS.get(conquista_id, {})
                xp_ganho = conquista_info.get("xp", 0)
            break
    salvar_usuarios(dados)
    return xp_ganho

def ganhar_xp(usuario, xp_ganho):
    """Adiciona XP ao usuário e retorna se subiu de nível"""
    import config
    dados = carregar_usuarios()
    for u in dados["usuarios"]:
        if u["usuario"].lower() == usuario.lower():
            xp_atual = u.get("xp", 0)
            nivel_antes = config.calcular_nivel(xp_atual)
            
            u["xp"] = xp_atual + xp_ganho
            
            nivel_depois = config.calcular_nivel(u["xp"])
            
            salvar_usuarios(dados)
            
            if nivel_antes[1] != nivel_depois[1]:
                return True, nivel_depois, u["xp"]
            return False, None, u["xp"]
    return False, None, 0

def obter_stats_usuario(usuario):
    dados = carregar_usuarios()
    for u in dados["usuarios"]:
        if u["usuario"].lower() == usuario.lower():
            return {
                "total_partidas": u.get("total_partidas", 0),
                "melhor_wpm": u.get("melhor_wpm", 0),
                "melhor_precisao": u.get("melhor_precisao", 0),
                "conquistas": u.get("conquistas", []),
                "xp": u.get("xp", 0)
            }
    return None
