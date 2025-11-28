import json
import os
import hashlib

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

    dados = carregar_usuarios()
    for u in dados["usuarios"]:
        if u["usuario"].lower() == usuario.lower():
            return False, "Usuário já existe."

    dados["usuarios"].append({"usuario": usuario, "senha": _hash_senha(senha)})
    salvar_usuarios(dados)
    return True, "Usuário cadastrado com sucesso."

def verificar_login(usuario, senha):
    usuario = usuario.strip()
    senha = senha.strip()
    dados = carregar_usuarios()
    senha_hash = _hash_senha(senha)
    for u in dados["usuarios"]:
        if u["usuario"].lower() == usuario.lower() and u["senha"] == senha_hash:
            return True
    return False
