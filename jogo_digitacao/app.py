import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import config
import gerador
import login
import categorias
from interface import InterfaceJogo
from multiplayer import SessaoMultiplayer

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Digitação - Perches Limeira")
        self.root.geometry(config.TELA)
        self.root.minsize(config.TELA_MIN_WIDTH, config.TELA_MIN_HEIGHT)
        self.root.configure(bg=config.COR_FUNDO)
        
        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.sair_fullscreen)
        
        self.frame_atual = None
        self.usuario_logado = None
        self.modo_jogo = tk.StringVar(value="normal")
        self.tipo_teclado_selecionado = "pt"
        self.categoria_selecionada = None
        self.texto_personalizado = None
        
        self.sessao_multi = None
        self.jogadores_multi = []
        self.num_jogadores_multi = 0
        
        # Logo global
        self.logo_img = None
        self.lbl_logo_global = None
        self.carregar_logo_perches()
        
        self.mostrar_tela_inicial()
    
    # =============== LOGO GLOBAL ===============
    def carregar_logo_perches(self):
        """Carrega logo_perches.jpg uma vez."""
        try:
            img = Image.open("logo_perches.jpg")
            largura_max = 110
            prop = largura_max / img.width
            nova_altura = int(img.height * prop)
            img = img.resize((largura_max, nova_altura), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            print("✅ Logo carregada com sucesso!")
        except Exception as e:
            print("⚠️ Erro ao carregar logo_perches.jpg:", e)
            self.logo_img = None
    
    def mostrar_logo_global(self):
        """Mostra a logo no canto superior direito da JANELA."""
        if self.logo_img is None:
            return
        
        if self.lbl_logo_global is not None:
            self.lbl_logo_global.destroy()
        
        self.lbl_logo_global = tk.Label(
            self.root,
            image=self.logo_img,
            bg=config.COR_FUNDO,
            borderwidth=0
        )
        self.lbl_logo_global.place(relx=0.99, rely=0.06, anchor="ne")
    
    def esconder_logo_global(self):
        """Esconde a logo global"""
        if self.lbl_logo_global is not None:
            self.lbl_logo_global.place_forget()
    
    # =============== UTILITÁRIOS ===============
    def limpar_tela(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()
            self.frame_atual = None
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
    
    def sair_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)
    
    def criar_botao_moderno(self, parent, texto, comando, cor_bg=None, largura=20):
        if cor_bg is None:
            cor_bg = config.COR_BOTAO
        
        btn = tk.Button(
            parent,
            text=texto,
            font=config.FONTE_TEXTO,
            bg=cor_bg,
            fg=config.COR_BOTAO_TEXTO,
            activebackground=config.COR_BOTAO_HOVER,
            activeforeground=config.COR_BOTAO_TEXTO,
            relief="flat",
            bd=0,
            width=largura,
            height=2,
            command=comando,
            cursor="hand2"
        )
        
        btn.bind("<Enter>", lambda e: btn.config(bg=config.COR_BOTAO_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=cor_bg))
        return btn
    
    # =============== TELA INICIAL ===============
    def mostrar_tela_inicial(self):
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=40,
            pady=35
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text="⌨️ Jogo de Digitação",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack(pady=(0, 10))
        
        tk.Label(
            card,
            text="Melhore sua velocidade e precisão",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(0, 25))
        
        self.criar_botao_moderno(
            card, "🚀 Entrar",
            lambda: self.mostrar_form_login("entrar"),
            config.COR_BOTAO, 22
        ).pack(pady=8)
        
        self.criar_botao_moderno(
            card, "📝 Registrar",
            lambda: self.mostrar_form_login("registrar"),
            config.COR_SUCESSO, 22
        ).pack(pady=8)
        
        tk.Label(
            card,
            text="Pressione F11 para tela cheia | ESC para sair",
            font=config.FONTE_MINI,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(30, 0))
    
    # =============== TELA LOGIN ===============
    def mostrar_form_login(self, modo="entrar"):
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=60,
            pady=50
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        titulo = "🚀 Entrar" if modo == "entrar" else "📝 Criar Conta"
        tk.Label(
            card,
            text=titulo,
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack(pady=(0, 30))
        
        tk.Label(
            card,
            text="Nome de usuário:",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(anchor="w", padx=5)
        
        entry_user = tk.Entry(
            card,
            font=config.FONTE_TEXTO_GRANDE,
            width=30,
            bg=config.COR_CARD_DESTAQUE,
            fg=config.COR_TEXTO,
            insertbackground=config.COR_TEXTO,
            relief="flat",
            bd=0
        )
        entry_user.pack(pady=(5, 15), ipady=8)
        entry_user.focus_set()
        
        tk.Label(
            card,
            text="Senha:",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(anchor="w", padx=5)
        
        entry_pwd = tk.Entry(
            card,
            font=config.FONTE_TEXTO_GRANDE,
            show="●",
            width=30,
            bg=config.COR_CARD_DESTAQUE,
            fg=config.COR_TEXTO,
            insertbackground=config.COR_TEXTO,
            relief="flat",
            bd=0
        )
        entry_pwd.pack(pady=(5, 10), ipady=8)
        
        lbl_msg = tk.Label(
            card,
            text="",
            bg=config.COR_FRAME,
            fg=config.COR_ERRO,
            font=config.FONTE_TEXTO,
            wraplength=400
        )
        lbl_msg.pack(pady=10)
        
        def acao_entrar():
            u = entry_user.get()
            p = entry_pwd.get()
            
            if not u or not p:
                lbl_msg.config(text="⚠️ Preencha todos os campos!", fg=config.COR_AVISO)
                return
            
            if login.verificar_login(u, p):
                self.usuario_logado = u
                self.mostrar_tela_modo()
            else:
                lbl_msg.config(text="❌ Usuário ou senha inválidos!", fg=config.COR_ERRO)
                entry_pwd.delete(0, tk.END)
        
        def acao_registrar():
            u = entry_user.get()
            p = entry_pwd.get()
            
            if not u or not p:
                lbl_msg.config(text="⚠️ Preencha todos os campos!", fg=config.COR_AVISO)
                return
            
            ok, msg = login.cadastrar_usuario(u, p)
            if ok:
                lbl_msg.config(text=f"✅ {msg}", fg=config.COR_SUCESSO)
                self.usuario_logado = u
                self.root.after(1000, self.mostrar_tela_modo)
            else:
                lbl_msg.config(text=f"❌ {msg}", fg=config.COR_ERRO)
        
        if modo == "entrar":
            self.criar_botao_moderno(card, "Entrar", acao_entrar, config.COR_BOTAO, 25).pack(pady=(10, 5))
            entry_pwd.bind("<Return>", lambda e: acao_entrar())
        else:
            self.criar_botao_moderno(card, "Criar Conta", acao_registrar, config.COR_SUCESSO, 25).pack(pady=(10, 5))
            entry_pwd.bind("<Return>", lambda e: acao_registrar())
        
        self.criar_botao_moderno(
            card, "← Voltar", self.mostrar_tela_inicial,
            config.COR_BOTAO_SECUNDARIO, 25
        ).pack(pady=5)
    
    # =============== TELA MODO ===============
    def mostrar_tela_modo(self):
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=60,
            pady=40
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        stats = login.obter_stats_usuario(self.usuario_logado)
        if stats:
            xp = stats.get("xp", 0)
            nivel = config.calcular_nivel(xp)
            saudacao = f"Bem-vindo, {self.usuario_logado}! 👋"
            info = f"{nivel[2]} {nivel[1]} | XP: {xp} | Partidas: {stats['total_partidas']} | Melhor WPM: {stats['melhor_wpm']:.0f}"
        else:
            saudacao = f"Bem-vindo, {self.usuario_logado}! 👋"
            info = "Primeira vez? Boa sorte!"
        
        tk.Label(
            card,
            text=saudacao,
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack(pady=(0, 5))
        
        tk.Label(
            card,
            text=info,
            font=config.FONTE_STATS,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(0, 30))
        
        tk.Label(
            card,
            text="Escolha o Modo de Jogo",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(0, 25))
        
        def escolher_modo(modo_id):
            self.modo_jogo.set(modo_id)
            self.mostrar_menu_tipo_jogo()
        
        for modo_id, modo_nome in config.MODOS_JOGO:
            desc_info = config.DESCRICOES_MODO.get(modo_id, {})
            
            if modo_id == "normal":
                cor_modo = config.COR_NORMAL
            elif modo_id == "morte_subita":
                cor_modo = config.COR_MORTE_SUBITA
            else:
                cor_modo = config.COR_HARDCORE
            
            frame_modo = tk.Frame(
                card,
                bg=config.COR_CARD_DESTAQUE,
                bd=0,
                highlightthickness=2,
                highlightbackground=config.COR_FRAME_BORDA
            )
            frame_modo.pack(pady=8, fill="x", padx=10)
            
            btn = tk.Button(
                frame_modo,
                text=desc_info.get("titulo", modo_nome),
                font=config.FONTE_TEXTO_GRANDE,
                bg=cor_modo,
                fg=config.COR_BOTAO_TEXTO,
                activebackground=cor_modo,
                activeforeground=config.COR_TEXTO_DESTAQUE,
                relief="flat",
                bd=0,
                width=22,
                height=1,
                cursor="hand2",
                command=lambda m=modo_id: escolher_modo(m)
            )
            btn.pack(side="left", padx=10, pady=10)
            
            desc_frame = tk.Frame(frame_modo, bg=config.COR_CARD_DESTAQUE)
            desc_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            tk.Label(
                desc_frame,
                text=desc_info.get("desc", ""),
                font=config.FONTE_STATS,
                bg=config.COR_CARD_DESTAQUE,
                fg=config.COR_TEXTO_SECUNDARIO,
                justify="left"
            ).pack(anchor="w")
            
            tk.Label(
                desc_frame,
                text=desc_info.get("dica", ""),
                font=config.FONTE_MINI,
                bg=config.COR_CARD_DESTAQUE,
                fg=cor_modo,
                justify="left"
            ).pack(anchor="w", pady=(5, 0))
            
            def on_enter(e, f=frame_modo, c=cor_modo):
                f.config(highlightbackground=c)
            
            def on_leave(e, f=frame_modo):
                f.config(highlightbackground=config.COR_FRAME_BORDA)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            frame_modo.bind("<Enter>", on_enter)
            frame_modo.bind("<Leave>", on_leave)
        
        frame_botoes_extra = tk.Frame(card, bg=config.COR_FRAME)
        frame_botoes_extra.pack(pady=(20, 0), fill="x")
        
        self.criar_botao_moderno(
            frame_botoes_extra, "🏆 Conquistas",
            self.mostrar_conquistas,
            config.COR_OURO, 15
        ).pack(side="left", padx=5)
        
        self.criar_botao_moderno(
            frame_botoes_extra, "🚪 Sair", self.mostrar_tela_inicial,
            config.COR_BOTAO_SECUNDARIO, 15
        ).pack(side="left", padx=5)
    
    # =============== TELA CONQUISTAS ===============
    def mostrar_conquistas(self):
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        self.root.bind("<Escape>", lambda e: [self.root.unbind("<Escape>"), self.mostrar_tela_modo()])
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=40,
            pady=30
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text="🏆 Suas Conquistas",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack(pady=(0, 20))
        
        stats = login.obter_stats_usuario(self.usuario_logado)
        conquistas_desbloqueadas = stats.get("conquistas", []) if stats else []
        
        canvas_conquistas = tk.Canvas(card, bg=config.COR_FRAME, highlightthickness=0, height=400, width=600)
        scrollbar = tk.Scrollbar(card, orient="vertical", command=canvas_conquistas.yview)
        frame_conquistas = tk.Frame(canvas_conquistas, bg=config.COR_FRAME)
        
        frame_conquistas.bind(
            "<Configure>",
            lambda e: canvas_conquistas.configure(scrollregion=canvas_conquistas.bbox("all"))
        )
        
        canvas_conquistas.create_window((0, 0), window=frame_conquistas, anchor="nw")
        canvas_conquistas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas_conquistas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas_conquistas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas_conquistas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for conquista_id, conquista_info in config.CONQUISTAS.items():
            desbloqueada = conquista_id in conquistas_desbloqueadas
            
            frame_conquista = tk.Frame(
                frame_conquistas,
                bg=config.COR_OURO if desbloqueada else config.COR_CARD_DESTAQUE,
                bd=0,
                highlightthickness=1,
                highlightbackground=config.COR_OURO if desbloqueada else config.COR_FRAME_BORDA
            )
            frame_conquista.pack(pady=8, padx=10, fill="x")
            
            tk.Label(
                frame_conquista,
                text=conquista_info["icone"],
                font=("Segoe UI", 32),
                bg=config.COR_OURO if desbloqueada else config.COR_CARD_DESTAQUE,
                fg=config.COR_TEXTO
            ).pack(side="left", padx=15, pady=10)
            
            info_frame = tk.Frame(
                frame_conquista,
                bg=config.COR_OURO if desbloqueada else config.COR_CARD_DESTAQUE
            )
            info_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            nome_text = conquista_info["nome"]
            if desbloqueada:
                nome_text += " ✅"
            
            tk.Label(
                info_frame,
                text=nome_text,
                font=config.FONTE_TEXTO,
                bg=config.COR_OURO if desbloqueada else config.COR_CARD_DESTAQUE,
                fg=config.COR_TEXTO,
                anchor="w"
            ).pack(anchor="w")
            
            tk.Label(
                info_frame,
                text=conquista_info["desc"],
                font=config.FONTE_MINI,
                bg=config.COR_OURO if desbloqueada else config.COR_CARD_DESTAQUE,
                fg=config.COR_TEXTO_SECUNDARIO,
                anchor="w"
            ).pack(anchor="w")
            
            tk.Label(
                info_frame,
                text=f"+{conquista_info['xp']} XP",
                font=config.FONTE_MINI,
                bg=config.COR_OURO if desbloqueada else config.COR_CARD_DESTAQUE,
                fg=config.COR_INFO if desbloqueada else config.COR_TEXTO_SECUNDARIO,
                anchor="w"
            ).pack(anchor="w", pady=(3, 0))
        
        total_conquistas = len(config.CONQUISTAS)
        conquistadas = len(conquistas_desbloqueadas)
        
        tk.Label(
            card,
            text=f"Progresso: {conquistadas}/{total_conquistas} conquistas desbloqueadas",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(15, 10))
        
        def voltar_limpo():
            canvas_conquistas.unbind_all("<MouseWheel>")
            self.root.unbind("<Escape>")
            self.mostrar_tela_modo()
        
        self.criar_botao_moderno(
            card, "← Voltar", voltar_limpo,
            config.COR_BOTAO_SECUNDARIO, 20
        ).pack(pady=10)
    
    # =============== MENU TIPO DE JOGO ===============
    def mostrar_menu_tipo_jogo(self):
        """Menu para escolher entre solo ou multiplayer"""
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=60,
            pady=50
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        modo_nome = next(
            (nome for mid, nome in config.MODOS_JOGO if mid == self.modo_jogo.get()),
            self.modo_jogo.get()
        )
        
        tk.Label(
            card,
            text=f"Modo: {modo_nome}",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_INFO
        ).pack(pady=(0, 10))
        
        tk.Label(
            card,
            text="Escolha o Tipo de Jogo",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(0, 30))
        
        self.criar_botao_moderno(
            card, "👤 Solo (Sozinho)",
            self.mostrar_tela_categoria,
            config.COR_BOTAO, 30
        ).pack(pady=10)
        
        self.criar_botao_moderno(
            card, "👥 Multiplayer (Turnos)",
            self.mostrar_config_multiplayer,
            config.COR_SUCESSO, 30
        ).pack(pady=10)
        
        self.criar_botao_moderno(
            card, "← Voltar", self.mostrar_tela_modo,
            config.COR_BOTAO_SECUNDARIO, 30
        ).pack(pady=(30, 0))
    
    # =============== CONFIGURAÇÃO MULTIPLAYER ===============
    def mostrar_config_multiplayer(self):
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=60,
            pady=50
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text="👥 Configurar Multiplayer",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack(pady=(0, 30))
        
        tk.Label(
            card,
            text="Quantos jogadores vão competir?",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(0, 15))
        
        frame_spinbox = tk.Frame(card, bg=config.COR_FRAME)
        frame_spinbox.pack(pady=10)
        
        spinbox_jogadores = tk.Spinbox(
            frame_spinbox,
            from_=2,
            to=8,
            font=config.FONTE_TEXTO_GRANDE,
            width=10,
            bg=config.COR_CARD_DESTAQUE,
            fg=config.COR_TEXTO,
            buttonbackground=config.COR_BOTAO,
            relief="flat",
            bd=2
        )
        spinbox_jogadores.pack()
        
        tk.Label(
            card,
            text="Você (Jogador 1) já está logado!\nOs outros jogadores farão login em suas contas.",
            font=config.FONTE_MINI,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO,
            justify="center"
        ).pack(pady=(20, 20))
        
        def iniciar_multi():
            num_jogadores = int(spinbox_jogadores.get())
            self.iniciar_multiplayer(num_jogadores)
        
        self.criar_botao_moderno(
            card, "🚀 Iniciar Multiplayer",
            iniciar_multi,
            config.COR_SUCESSO, 25
        ).pack(pady=10)
        
        self.criar_botao_moderno(
            card, "← Voltar", self.mostrar_menu_tipo_jogo,
            config.COR_BOTAO_SECUNDARIO, 25
        ).pack(pady=5)
    
    # =============== LOGIN MULTIPLAYER ===============
    def iniciar_multiplayer(self, num_jogadores):
        """Inicia processo de login multiplayer"""
        self.jogadores_multi = [{
            "numero": 1,
            "usuario": self.usuario_logado
        }]
        self.num_jogadores_multi = num_jogadores
        
        if num_jogadores == 1:
            self.mostrar_tela_categoria_multi(num_jogadores)
        else:
            self.mostrar_login_multiplayer(2)
    
    def mostrar_login_multiplayer(self, numero_jogador):
        """Tela de login para cada jogador do multiplayer"""
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=60,
            pady=50
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text=f"👤 Jogador {numero_jogador} de {self.num_jogadores_multi}",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack(pady=(0, 10))
        
        tk.Label(
            card,
            text=f"Jogador 1: {self.jogadores_multi[0]['usuario']} ✅",
            font=config.FONTE_MINI,
            bg=config.COR_FRAME,
            fg=config.COR_SUCESSO
        ).pack(pady=(0, 5))
        
        tk.Label(
            card,
            text="Faça login na sua conta",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(0, 30))
        
        tk.Label(
            card,
            text="Nome de usuário:",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(anchor="w", padx=5)
        
        entry_user = tk.Entry(
            card,
            font=config.FONTE_TEXTO_GRANDE,
            width=30,
            bg=config.COR_CARD_DESTAQUE,
            fg=config.COR_TEXTO,
            insertbackground=config.COR_TEXTO,
            relief="flat",
            bd=0
        )
        entry_user.pack(pady=(5, 15), ipady=8)
        entry_user.focus_set()
        
        tk.Label(
            card,
            text="Senha:",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(anchor="w", padx=5)
        
        entry_pwd = tk.Entry(
            card,
            font=config.FONTE_TEXTO_GRANDE,
            show="●",
            width=30,
            bg=config.COR_CARD_DESTAQUE,
            fg=config.COR_TEXTO,
            insertbackground=config.COR_TEXTO,
            relief="flat",
            bd=0
        )
        entry_pwd.pack(pady=(5, 10), ipady=8)
        
        lbl_msg = tk.Label(
            card,
            text="",
            bg=config.COR_FRAME,
            fg=config.COR_ERRO,
            font=config.FONTE_TEXTO,
            wraplength=400
        )
        lbl_msg.pack(pady=10)
        
        def fazer_login():
            u = entry_user.get()
            p = entry_pwd.get()
            
            if not u or not p:
                lbl_msg.config(text="⚠️ Preencha todos os campos!", fg=config.COR_AVISO)
                return
            
            if not login.verificar_login(u, p):
                lbl_msg.config(text="❌ Usuário ou senha inválidos!", fg=config.COR_ERRO)
                entry_pwd.delete(0, tk.END)
                return
            
            if u in [j["usuario"] for j in self.jogadores_multi]:
                lbl_msg.config(text="⚠️ Este jogador já está na partida!", fg=config.COR_AVISO)
                return
            
            self.jogadores_multi.append({
                "numero": numero_jogador,
                "usuario": u
            })
            
            if numero_jogador < self.num_jogadores_multi:
                self.mostrar_login_multiplayer(numero_jogador + 1)
            else:
                self.mostrar_tela_categoria_multi(self.num_jogadores_multi)
        
        self.criar_botao_moderno(
            card, "✅ Confirmar",
            fazer_login,
            config.COR_SUCESSO, 25
        ).pack(pady=10)
        
        entry_pwd.bind("<Return>", lambda e: fazer_login())
        
        if numero_jogador == 2:
            self.criar_botao_moderno(
                card, "← Voltar", self.mostrar_config_multiplayer,
                config.COR_BOTAO_SECUNDARIO, 25
            ).pack(pady=5)
        else:
            self.criar_botao_moderno(
                card, "← Jogador Anterior",
                lambda: self.voltar_jogador_anterior(numero_jogador),
                config.COR_BOTAO_SECUNDARIO, 25
            ).pack(pady=5)
    
    def voltar_jogador_anterior(self, numero_atual):
        """Volta para o login do jogador anterior"""
        if len(self.jogadores_multi) > 0:
            self.jogadores_multi.pop()
        self.mostrar_login_multiplayer(numero_atual - 1)
    
    # =============== TELA CATEGORIA ===============
    def mostrar_tela_categoria(self):
        """Tela para escolher categoria ou texto personalizado"""
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=50,
            pady=40
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text="Escolha o Tipo de Texto",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(0, 20))
        
        for cat_id, nome, icone in categorias.obter_categorias():
            self.criar_botao_moderno(
                card,
                f"{icone} {nome}",
                lambda c=cat_id: self.selecionar_categoria(c),
                config.COR_BOTAO,
                30
            ).pack(pady=5)
        
        self.criar_botao_moderno(
            card, "🎲 Texto Aleatório",
            lambda: self.selecionar_categoria(None),
            config.COR_INFO, 30
        ).pack(pady=(15, 5))
        
        self.criar_botao_moderno(
            card, "✏️ Texto Personalizado",
            self.mostrar_tela_texto_personalizado,
            config.COR_AVISO, 30
        ).pack(pady=5)
        
        self.criar_botao_moderno(
            card, "← Voltar", self.mostrar_menu_tipo_jogo,
            config.COR_BOTAO_SECUNDARIO, 30
        ).pack(pady=(15, 0))
    
    def mostrar_tela_categoria_multi(self, num_jogadores):
        """Tela categoria para multiplayer"""
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=50,
            pady=40
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text="Escolha o Tipo de Texto",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(0, 20))
        
        for cat_id, nome, icone in categorias.obter_categorias():
            self.criar_botao_moderno(
                card,
                f"{icone} {nome}",
                lambda c=cat_id, n=num_jogadores: self.selecionar_categoria_multi(c, n),
                config.COR_BOTAO,
                30
            ).pack(pady=5)
        
        self.criar_botao_moderno(
            card, "🎲 Texto Aleatório",
            lambda: self.selecionar_categoria_multi(None, num_jogadores),
            config.COR_INFO, 30
        ).pack(pady=(15, 5))
        
        self.criar_botao_moderno(
            card, "✏️ Texto Personalizado",
            lambda: self.mostrar_tela_texto_personalizado_multi(num_jogadores),
            config.COR_AVISO, 30
        ).pack(pady=5)
        
        self.criar_botao_moderno(
            card, "← Voltar", lambda: self.mostrar_login_multiplayer(2) if num_jogadores > 1 else self.mostrar_config_multiplayer(),
            config.COR_BOTAO_SECUNDARIO, 30
        ).pack(pady=(15, 0))
    
    def selecionar_categoria(self, categoria):
        """Seleciona categoria e inicia jogo"""
        self.categoria_selecionada = categoria
        self.texto_personalizado = None
        self.mostrar_tela_jogo(self.tipo_teclado_selecionado)
    
    def selecionar_categoria_multi(self, categoria, num_jogadores):
        """Seleciona categoria e inicia multiplayer"""
        self.categoria_selecionada = categoria
        self.texto_personalizado = None
        
        if categoria:
            texto = categorias.gerar_texto_categoria(categoria)
        else:
            texto = gerador.gerar_texto()
        
        self.sessao_multi = SessaoMultiplayer(
            num_jogadores,
            self.modo_jogo.get(),
            self.tipo_teclado_selecionado,
            texto
        )
        
        self.mostrar_tela_jogo_multi()
    
    # =============== TEXTO PERSONALIZADO ===============
    def mostrar_tela_texto_personalizado(self):
        """Tela para digitar texto personalizado"""
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=50,
            pady=40
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text="✏️ Digite seu Texto Personalizado",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(0, 10))
        
        tk.Label(
            card,
            text="Escreva o texto que você quer treinar:",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(0, 15))
        
        text_area = scrolledtext.ScrolledText(
            card,
            font=config.FONTE_MONO,
            width=60,
            height=10,
            bg=config.COR_CARD_DESTAQUE,
            fg=config.COR_TEXTO,
            insertbackground=config.COR_TEXTO,
            relief="flat",
            bd=2,
            wrap=tk.WORD
        )
        text_area.pack(pady=10, padx=10)
        text_area.focus_set()
        
        lbl_aviso = tk.Label(
            card,
            text="",
            font=config.FONTE_MINI,
            bg=config.COR_FRAME,
            fg=config.COR_ERRO
        )
        lbl_aviso.pack(pady=5)
        
        def usar_texto():
            texto = text_area.get("1.0", tk.END).strip()
            if len(texto) < 10:
                lbl_aviso.config(text="⚠️ O texto deve ter pelo menos 10 caracteres!")
                return
            
            self.texto_personalizado = texto
            self.categoria_selecionada = None
            self.mostrar_tela_jogo(self.tipo_teclado_selecionado)
        
        self.criar_botao_moderno(
            card, "✅ Usar este Texto",
            usar_texto,
            config.COR_SUCESSO, 25
        ).pack(pady=10)
        
        self.criar_botao_moderno(
            card, "← Voltar", self.mostrar_tela_categoria,
            config.COR_BOTAO_SECUNDARIO, 25
        ).pack(pady=5)
    
    def mostrar_tela_texto_personalizado_multi(self, num_jogadores):
        """Tela para digitar texto personalizado (multiplayer)"""
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=50,
            pady=40
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text="✏️ Digite seu Texto Personalizado",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(0, 10))
        
        tk.Label(
            card,
            text="Escreva o texto que você quer treinar:",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(0, 15))
        
        text_area = scrolledtext.ScrolledText(
            card,
            font=config.FONTE_MONO,
            width=60,
            height=10,
            bg=config.COR_CARD_DESTAQUE,
            fg=config.COR_TEXTO,
            insertbackground=config.COR_TEXTO,
            relief="flat",
            bd=2,
            wrap=tk.WORD
        )
        text_area.pack(pady=10, padx=10)
        text_area.focus_set()
        
        lbl_aviso = tk.Label(
            card,
            text="",
            font=config.FONTE_MINI,
            bg=config.COR_FRAME,
            fg=config.COR_ERRO
        )
        lbl_aviso.pack(pady=5)
        
        def usar_texto():
            texto = text_area.get("1.0", tk.END).strip()
            if len(texto) < 10:
                lbl_aviso.config(text="⚠️ O texto deve ter pelo menos 10 caracteres!")
                return
            
            self.sessao_multi = SessaoMultiplayer(
                num_jogadores,
                self.modo_jogo.get(),
                self.tipo_teclado_selecionado,
                texto
            )
            
            self.mostrar_tela_jogo_multi()
        
        self.criar_botao_moderno(
            card, "✅ Usar este Texto",
            usar_texto,
            config.COR_SUCESSO, 25
        ).pack(pady=10)
        
        self.criar_botao_moderno(
            card, "← Voltar", lambda: self.mostrar_tela_categoria_multi(num_jogadores),
            config.COR_BOTAO_SECUNDARIO, 25
        ).pack(pady=5)
    
    # =============== TELA JOGO ===============
    def mostrar_tela_jogo(self, tipo_teclado):
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.esconder_logo_global()
        
        if self.texto_personalizado:
            texto = self.texto_personalizado
        elif self.categoria_selecionada:
            texto = categorias.gerar_texto_categoria(self.categoria_selecionada)
        else:
            texto = gerador.gerar_texto()
        
        def repetir():
            self.mostrar_tela_jogo(tipo_teclado)
        
        def voltar_menu():
            self.mostrar_tela_modo()
        
        jogo = InterfaceJogo(
            frame_fundo,
            tipo_teclado,
            self.modo_jogo.get(),
            on_fim=repetir,
            on_voltar_menu=voltar_menu,
            usuario=self.usuario_logado,
            logo_img=None,
            sessao_multi=None
        )
        
        jogo.definir_texto(texto)
    
    def mostrar_tela_jogo_multi(self):
        """Mostra tela de jogo multiplayer - CORRIGIDO"""
        self.limpar_tela()
        
        # Verifica se todos já jogaram
        if self.sessao_multi.sessao_completa():
            self.mostrar_resultado_multiplayer()
            return
        
        # Cria novo frame para este jogador
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        # Esconde logo
        self.esconder_logo_global()
        
        # Informações do jogador atual
        jogador_atual_info = self.jogadores_multi[self.sessao_multi.jogador_atual - 1]
        
        # Banner com informação do jogador
        frame_info_jogador = tk.Frame(frame_fundo, bg=config.COR_INFO, pady=15)
        frame_info_jogador.pack(fill="x", side="top")
        
        tk.Label(
            frame_info_jogador,
            text=f"🎮 Jogador {jogador_atual_info['numero']} de {self.sessao_multi.num_jogadores}",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_INFO,
            fg=config.COR_BOTAO_TEXTO
        ).pack()
        
        tk.Label(
            frame_info_jogador,
            text=f"👤 {jogador_atual_info['usuario']}",
            font=("Segoe UI", 20, "bold"),
            bg=config.COR_INFO,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack(pady=(5, 0))
        
        # Mostra quem já jogou
        if self.sessao_multi.resultados:
            resultados_text = " | ".join([
                f"{r['jogador']}: {r['pontos']} pts"
                for r in self.sessao_multi.resultados
            ])
            tk.Label(
                frame_info_jogador,
                text=f"📊 Resultados: {resultados_text}",
                font=config.FONTE_MINI,
                bg=config.COR_INFO,
                fg=config.COR_BOTAO_TEXTO
            ).pack(pady=(8, 0))
        
        # Frame para o jogo (separado do banner)
        frame_jogo = tk.Frame(frame_fundo, bg=config.COR_FUNDO)
        frame_jogo.pack(expand=True, fill="both")
        
        def proximo_jogador():
            # Limpa bindings do jogo anterior
            self.root.unbind_all("<KeyRelease>")
            self.root.unbind_all("<Return>")
            self.root.unbind_all("<space>")
            
            # Mostra próximo jogador ou resultado final
            self.mostrar_tela_jogo_multi()
        
        def voltar_menu():
            # Limpa bindings
            self.root.unbind_all("<KeyRelease>")
            self.root.unbind_all("<Return>")
            self.root.unbind_all("<space>")
            
            self.sessao_multi = None
            self.jogadores_multi = []
            self.mostrar_tela_modo()
        
        # Cria interface de jogo para este jogador
        jogo = InterfaceJogo(
            frame_jogo,  # ✅ Frame separado para cada jogador
            self.sessao_multi.tipo_teclado,
            self.sessao_multi.modo_jogo,
            on_fim=proximo_jogador,
            on_voltar_menu=voltar_menu,
            usuario=jogador_atual_info['usuario'],
            logo_img=None,
            sessao_multi=self.sessao_multi
        )
        
        jogo.definir_texto(self.sessao_multi.texto)
    
    def mostrar_resultado_multiplayer(self):
        self.limpar_tela()
        
        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo
        
        self.mostrar_logo_global()
        
        card = tk.Frame(
            frame_fundo,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=50,
            pady=40
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            card,
            text="🏆 Resultado Final - Multiplayer",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack(pady=(0, 20))
        
        ranking = self.sessao_multi.obter_ranking()
        vencedor = self.sessao_multi.obter_vencedor()
        
        if vencedor:
            frame_vencedor = tk.Frame(card, bg=config.COR_OURO, padx=20, pady=15)
            frame_vencedor.pack(pady=15, fill="x")
            
            tk.Label(
                frame_vencedor,
                text=f"👑 VENCEDOR: {vencedor['jogador']}",
                font=("Segoe UI", 28, "bold"),
                bg=config.COR_OURO,
                fg=config.COR_TEXTO
            ).pack()
            
            tk.Label(
                frame_vencedor,
                text=f"Pontos: {vencedor['pontos']} | WPM: {vencedor['wpm']:.1f} | Precisão: {vencedor['precisao']:.1f}%",
                font=config.FONTE_TEXTO,
                bg=config.COR_OURO,
                fg=config.COR_TEXTO
            ).pack(pady=(5, 0))
        
        tk.Label(
            card,
            text="📊 Ranking Completo",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(15, 10))
        
        for idx, resultado in enumerate(ranking, 1):
            if idx == 1:
                cor_pos = config.COR_OURO
                emoji = "🥇"
            elif idx == 2:
                cor_pos = config.COR_PRATA
                emoji = "🥈"
            elif idx == 3:
                cor_pos = config.COR_BRONZE
                emoji = "🥉"
            else:
                cor_pos = config.COR_CARD_DESTAQUE
                emoji = f"{idx}º"
            
            frame_pos = tk.Frame(card, bg=cor_pos, padx=15, pady=10)
            frame_pos.pack(pady=5, fill="x")
            
            tk.Label(
                frame_pos,
                text=f"{emoji} {resultado['jogador']}",
                font=config.FONTE_TEXTO,
                bg=cor_pos,
                fg=config.COR_TEXTO,
                anchor="w"
            ).pack(side="left", padx=10)
            
            tk.Label(
                frame_pos,
                text=f"{resultado['pontos']} pts | {resultado['wpm']:.1f} WPM | {resultado['precisao']:.1f}%",
                font=config.FONTE_MINI,
                bg=cor_pos,
                fg=config.COR_TEXTO_SECUNDARIO,
                anchor="e"
            ).pack(side="right", padx=10)
        
        frame_botoes = tk.Frame(card, bg=config.COR_FRAME)
        frame_botoes.pack(pady=(20, 0))
        
        self.criar_botao_moderno(
            frame_botoes, "🔄 Jogar Novamente",
            lambda: self.reiniciar_multiplayer(),
            config.COR_BOTAO, 20
        ).pack(side="left", padx=5)
        
        self.criar_botao_moderno(
            frame_botoes, "🏠 Menu Principal",
            lambda: [setattr(self, 'sessao_multi', None), setattr(self, 'jogadores_multi', []), self.mostrar_tela_modo()],
            config.COR_BOTAO_SECUNDARIO, 20
        ).pack(side="left", padx=5)
    
    def reiniciar_multiplayer(self):
        num_jogadores = self.sessao_multi.num_jogadores
        self.sessao_multi = None
        self.jogadores_multi = []
        self.mostrar_config_multiplayer()

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
