import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import config
import gerador
import login
from interface import InterfaceJogo


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

        # Logo global (canto superior direito da janela)
        self.logo_img = None
        self.lbl_logo_global = None
        self.carregar_logo_perches()

        self.mostrar_tela_inicial()

    # =============== LOGO GLOBAL ===============
    def carregar_logo_perches(self):
        """Carrega logo_perches.jpg uma vez."""
        try:
            img = Image.open("logo_perches.jpg")
            largura_max = 110  # aumentado de 80 para 110
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
        # canto superior direito da janela (desceu um pouco)
        self.lbl_logo_global.place(relx=0.99, rely=0.06, anchor="ne")

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
            padx=40,  # reduzido de 60 para 40
            pady=35   # reduzido de 50 para 35
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
        ).pack(pady=(0, 25))  # reduzido de 40 para 25

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
            saudacao = f"Bem-vindo, {self.usuario_logado}! 👋"
            info = f"Partidas: {stats['total_partidas']} | Melhor WPM: {stats['melhor_wpm']:.0f}"
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
            self.mostrar_tela_teclado()

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
                highlightthickness=1,
                highlightbackground=cor_modo
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

            def on_enter(e, b=btn, c=cor_modo):
                b.config(bg=c, font=config.FONTE_TEXTO_GRANDE + ("bold",))

            def on_leave(e, b=btn, c=cor_modo):
                b.config(bg=c, font=config.FONTE_TEXTO_GRANDE)

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

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

        self.criar_botao_moderno(
            card, "🚪 Sair", self.mostrar_tela_inicial,
            config.COR_BOTAO_SECUNDARIO, 20
        ).pack(pady=(25, 0))

    # =============== TELA TECLADO ===============
    def mostrar_tela_teclado(self):
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
            text="Escolha o Layout do Teclado",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO
        ).pack(pady=(0, 30))

        self.criar_botao_moderno(
            card, "⌨️ Português (ABNT)",
            lambda: self.mostrar_tela_jogo("pt"),
            config.COR_BOTAO, 30
        ).pack(pady=10)

        self.criar_botao_moderno(
            card, "⌨️ Inglês Internacional",
            lambda: self.mostrar_tela_jogo("en"),
            config.COR_BOTAO, 30
        ).pack(pady=10)

        self.criar_botao_moderno(
            card, "← Voltar", self.mostrar_tela_modo,
            config.COR_BOTAO_SECUNDARIO, 30
        ).pack(pady=(30, 0))

    # =============== TELA JOGO ===============
    def mostrar_tela_jogo(self, tipo_teclado):
        self.limpar_tela()

        frame_fundo = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame_fundo.pack(expand=True, fill="both")
        self.frame_atual = frame_fundo

        self.mostrar_logo_global()

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
            logo_img=None
        )
        jogo.definir_texto(texto)
        jogo.iniciar()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
