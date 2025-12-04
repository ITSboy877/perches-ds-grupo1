# ==================== CONFIGURAÇÕES DE TELA ====================
TELA = "1400x800"
TELA_MIN_WIDTH = 1200
TELA_MIN_HEIGHT = 700

# ==================== FONTES MODERNAS ====================
FONTE_TITULO = ("Segoe UI", 36, "bold")
FONTE_SUBTITULO = ("Segoe UI", 20, "bold")
FONTE_TEXTO = ("Segoe UI", 18)
FONTE_TEXTO_GRANDE = ("Segoe UI", 22)
FONTE_MONO = ("Consolas", 20)  # Para área de digitação
FONTE_STATS = ("Segoe UI", 16)
FONTE_MINI = ("Segoe UI", 14)

# ==================== PALETA DE CORES MODERNA ====================
# Fundo e Cards
COR_FUNDO = "#0f172a"  # Azul escuro moderno
COR_FUNDO_GRADIENTE = "#1e293b"
COR_FRAME = "#1e293b"  # Card escuro
COR_FRAME_BORDA = "#334155"
COR_CARD_DESTAQUE = "#2d3748"

# Texto
COR_TEXTO = "#f1f5f9"  # Branco suave
COR_TEXTO_SECUNDARIO = "#94a3b8"
COR_TEXTO_DESTAQUE = "#ffffff"

# Botões
COR_BOTAO = "#3b82f6"  # Azul vibrante
COR_BOTAO_HOVER = "#2563eb"
COR_BOTAO_TEXTO = "#ffffff"
COR_BOTAO_SECUNDARIO = "#475569"
COR_BOTAO_SECUNDARIO_HOVER = "#334155"

# Status e Feedback
COR_SUCESSO = "#10b981"  # Verde moderno
COR_SUCESSO_CLARO = "#34d399"
COR_ERRO = "#ef4444"  # Vermelho vibrante
COR_ERRO_CLARO = "#f87171"
COR_AVISO = "#f59e0b"  # Laranja
COR_INFO = "#06b6d4"  # Ciano

# Modos de Jogo
COR_NORMAL = "#10b981"
COR_MORTE_SUBITA = "#f59e0b"
COR_HARDCORE = "#ef4444"

# Ranking e Progresso
COR_OURO = "#fbbf24"
COR_PRATA = "#94a3b8"
COR_BRONZE = "#f97316"
COR_PROGRESSO = "#3b82f6"
COR_PROGRESSO_BG = "#1e293b"

# Efeitos visuais
COR_COMBO_1 = "#3b82f6"  # Azul
COR_COMBO_2 = "#8b5cf6"  # Roxo
COR_COMBO_3 = "#ec4899"  # Rosa
COR_COMBO_4 = "#f59e0b"  # Laranja
COR_COMBO_5 = "#ef4444"  # Vermelho (FIRE!)

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

# ==================== CONQUISTAS E BADGES ====================
CONQUISTAS = {
    "primeira_vitoria": {"nome": "Primeira Vitória", "desc": "Complete sua primeira rodada", "icone": "🏆"},
    "velocista": {"nome": "Velocista", "desc": "Alcance 60 WPM", "icone": "⚡"},
    "mestre": {"nome": "Mestre da Digitação", "desc": "Alcance 80 WPM", "icone": "👑"},
    "perfeito": {"nome": "Perfeição", "desc": "Complete sem erros", "icone": "💎"},
    "combo_master": {"nome": "Combo Master", "desc": "Combo de 50+ caracteres", "icone": "🔥"},
    "resistencia": {"nome": "Resistência", "desc": "Complete 10 rodadas", "icone": "💪"},
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
ANIMACAO_DURACAO = 300  # ms
ANIMACAO_FEEDBACK_ERRO = 150  # ms
ANIMACAO_COMBO = 500  # ms

# ==================== CONFIGURAÇÕES DE SOM (OPCIONAL) ====================
SOM_HABILITADO = False  # Mude para True se quiser sons
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
