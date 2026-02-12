import tkinter as tk

# ==================== DETECÇÃO AUTOMÁTICA DE RESOLUÇÃO ====================
def obter_resolucao_tela():
    """Detecta a resolução da tela automaticamente"""
    root = tk.Tk()
    root.withdraw()  # Esconde a janela temporária
    largura = root.winfo_screenwidth()
    altura = root.winfo_screenheight()
    root.destroy()
    return largura, altura

# Detecta resolução
LARGURA_TELA, ALTURA_TELA = obter_resolucao_tela()

# Define tamanho da janela como 90% da tela (para não ficar fullscreen)
LARGURA_JANELA = int(LARGURA_TELA * 0.9)
ALTURA_JANELA = int(ALTURA_TELA * 0.85)

TELA = f"{LARGURA_JANELA}x{ALTURA_JANELA}"
TELA_MIN_WIDTH = 800
TELA_MIN_HEIGHT = 600

# ==================== FONTES RESPONSIVAS ====================
# Calcula tamanhos de fonte baseados na resolução
def calcular_tamanho_fonte(tamanho_base):
    """Ajusta tamanho da fonte baseado na resolução"""
    fator = min(LARGURA_TELA / 1920, ALTURA_TELA / 1080)
    return max(8, int(tamanho_base * fator))

FONTE_TITULO = ("Segoe UI", calcular_tamanho_fonte(36), "bold")
FONTE_SUBTITULO = ("Segoe UI", calcular_tamanho_fonte(20), "bold")
FONTE_TEXTO = ("Segoe UI", calcular_tamanho_fonte(18))
FONTE_TEXTO_GRANDE = ("Segoe UI", calcular_tamanho_fonte(22))
FONTE_MONO = ("Consolas", calcular_tamanho_fonte(20))
FONTE_STATS = ("Segoe UI", calcular_tamanho_fonte(16))
FONTE_MINI = ("Segoe UI", calcular_tamanho_fonte(14))

# ==================== PALETA DE CORES MODERNA ====================
COR_FUNDO = "#0f172a"
COR_FUNDO_GRADIENTE = "#1e293b"
COR_FRAME = "#1e293b"
COR_FRAME_BORDA = "#334155"
COR_CARD_DESTAQUE = "#2d3748"

COR_TEXTO = "#f1f5f9"
COR_TEXTO_SECUNDARIO = "#94a3b8"
COR_TEXTO_DESTAQUE = "#ffffff"

COR_BOTAO = "#3b82f6"
COR_BOTAO_HOVER = "#2563eb"
COR_BOTAO_TEXTO = "#ffffff"
COR_BOTAO_SECUNDARIO = "#475569"
COR_BOTAO_SECUNDARIO_HOVER = "#334155"

COR_SUCESSO = "#10b981"
COR_SUCESSO_CLARO = "#34d399"
COR_ERRO = "#ef4444"
COR_ERRO_CLARO = "#f87171"
COR_AVISO = "#f59e0b"
COR_INFO = "#06b6d4"

COR_NORMAL = "#10b981"
COR_MORTE_SUBITA = "#f59e0b"
COR_HARDCORE = "#ef4444"

COR_OURO = "#fbbf24"
COR_PRATA = "#94a3b8"
COR_BRONZE = "#f97316"

COR_PROGRESSO = "#3b82f6"
COR_PROGRESSO_BG = "#1e293b"

COR_COMBO_1 = "#3b82f6"
COR_COMBO_2 = "#8b5cf6"
COR_COMBO_3 = "#ec4899"
COR_COMBO_4 = "#f59e0b"
COR_COMBO_5 = "#ef4444"

# ==================== TEMPO E MODOS ====================
TEMPO = 60

MODOS_JOGO = [
    ("normal", "Normal"),
    ("morte_subita", "Morte Súbita"),
    ("hardcore", "Hardcore"),
]

TEMPO_POR_MODO = {
    "normal": 60,
    "morte_subita": 45,
    "hardcore": 30,
}

# ==================== SISTEMA DE PONTUAÇÃO ====================
PESOS_PONTOS = {
    "normal": {
        "ponto_por_correto": 3,
        "penalidade_por_erro": 1,
        "penalidade_tempo_5s": 1,
        "bonus_combo_10": 20,
        "bonus_combo_25": 50,
        "bonus_combo_50": 100,
        "bonus_perfeito": 200,
    },
    "morte_subita": {
        "ponto_por_correto": 5,
        "penalidade_por_erro": 9999,
        "penalidade_tempo_5s": 0,
        "bonus_combo_10": 30,
        "bonus_combo_25": 75,
        "bonus_combo_50": 150,
        "bonus_perfeito": 500,
    },
    "hardcore": {
        "ponto_por_correto": 4,
        "penalidade_por_erro": 5,
        "penalidade_tempo_5s": 3,
        "bonus_combo_10": 25,
        "bonus_combo_25": 60,
        "bonus_combo_50": 120,
        "bonus_perfeito": 300,
    },
}

# ==================== SISTEMA DE XP E NÍVEIS ====================
XP_POR_PARTIDA = 10
XP_POR_WPM = 2  # 2 XP por cada WPM
XP_POR_PRECISAO = 1  # 1 XP por cada % de precisão
XP_BONUS_PERFEITO = 50

NIVEIS = [
    (0, "Iniciante", "🌱"),
    (100, "Aprendiz", "📚"),
    (300, "Intermediário", "⚡"),
    (600, "Avançado", "🔥"),
    (1000, "Expert", "💎"),
    (1500, "Mestre", "👑"),
    (2500, "Lenda", "⭐")
]

def calcular_nivel(xp):
    """Retorna o nível atual baseado no XP"""
    nivel_atual = NIVEIS[0]
    for xp_necessario, nome, icone in NIVEIS:
        if xp >= xp_necessario:
            nivel_atual = (xp_necessario, nome, icone)
    return nivel_atual

def xp_para_proximo_nivel(xp):
    """Retorna quanto XP falta para o próximo nível"""
    for i, (xp_necessario, nome, icone) in enumerate(NIVEIS):
        if xp < xp_necessario:
            return xp_necessario - xp
    return 0

# ==================== CONQUISTAS E BADGES ====================
CONQUISTAS = {
    "primeira_vitoria": {"nome": "Primeira Vitória", "desc": "Complete sua primeira rodada", "icone": "🏆", "xp": 25},
    "velocista": {"nome": "Velocista", "desc": "Alcance 60 WPM", "icone": "⚡", "xp": 50},
    "mestre": {"nome": "Mestre da Digitação", "desc": "Alcance 80 WPM", "icone": "👑", "xp": 100},
    "perfeito": {"nome": "Perfeição", "desc": "Complete sem erros", "icone": "💎", "xp": 75},
    "combo_master": {"nome": "Combo Master", "desc": "Combo de 50+ caracteres", "icone": "🔥", "xp": 60},
    "resistencia": {"nome": "Resistência", "desc": "Complete 10 rodadas", "icone": "💪", "xp": 80},
    "dedicacao": {"nome": "Dedicação", "desc": "Complete 50 rodadas", "icone": "🎯", "xp": 150},
    "maratonista": {"nome": "Maratonista", "desc": "Complete 100 rodadas", "icone": "🏃", "xp": 300},
    "flash": {"nome": "Flash", "desc": "Alcance 100 WPM", "icone": "⚡", "xp": 200},
}

# ==================== NÍVEIS DE COMBO ====================
NIVEIS_COMBO = [
    (10, "Bom!", COR_COMBO_1),
    (25, "Ótimo!", COR_COMBO_2),
    (50, "Incrível!", COR_COMBO_3),
    (75, "Perfeito!", COR_COMBO_4),
    (100, "LENDÁRIO!", COR_COMBO_5),
]

# ==================== CONFIGURAÇÕES DE ANIMAÇÃO ====================
ANIMACAO_DURACAO = 300
ANIMACAO_FEEDBACK_ERRO = 150
ANIMACAO_COMBO = 500

# ==================== CONFIGURAÇÕES DE SOM (OPCIONAL) ====================
SOM_HABILITADO = False
SOM_ACERTO = "sounds/click.wav"
SOM_ERRO = "sounds/error.wav"
SOM_COMBO = "sounds/combo.wav"
SOM_VITORIA = "sounds/win.wav"

# ==================== RANKINGS ====================
RANKING_TOP_EXIBIR = 10

RANKING_CORES_POSICAO = {
    1: COR_OURO,
    2: COR_PRATA,
    3: COR_BRONZE,
}

# ==================== MENSAGENS MOTIVACIONAIS ====================
MENSAGENS_WPM = {
    (0, 20): "Continue praticando! 📚",
    (20, 40): "Você está melhorando! 👍",
    (40, 60): "Bom trabalho! 🎯",
    (60, 80): "Excelente! ⚡",
    (80, 100): "Impressionante! 🔥",
    (100, float('inf')): "LENDÁRIO! 👑",
}

MENSAGENS_PRECISAO = {
    (0, 70): "Foque na precisão!",
    (70, 85): "Boa precisão!",
    (85, 95): "Quase perfeito!",
    (95, 100): "Precisão impecável!",
    (100, 100): "PERFEIÇÃO ABSOLUTA!",
}

# ==================== DESCRIÇÕES DOS MODOS ====================
DESCRICOES_MODO = {
    "normal": {
        "titulo": "🎮 Modo Normal",
        "desc": "Pontuação balanceada\nPenalidade leve por erros\nIdeal para treino",
        "dica": "Foque em velocidade e precisão!"
    },
    "morte_subita": {
        "titulo": "💀 Modo Morte Súbita",
        "desc": "Qualquer erro encerra\nPontuação alta\nSem penalidade de tempo",
        "dica": "Seja perfeito ou perca tudo!"
    },
    "hardcore": {
        "titulo": "🔥 Modo Hardcore",
        "desc": "Tempo limitado (30s)\nErros pesam muito\nPara especialistas",
        "dica": "Velocidade + precisão = vitória!"
    },
}
