import tkinter as tk
import config
import gerador
import login
from interface import InterfaceJogo

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Digitação")
        self.root.geometry(config.TELA)
        self.root.configure(bg=config.COR_FUNDO)

        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.sair_fullscreen)

        self.frame_atual = None
        self.usuario_logado = None

        self.mostrar_tela_login()

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

    # --------- Tela Login (etapa 1: escolher Entrar ou Registrar) ---------
    def mostrar_tela_login(self):
        self.limpar_tela()
        frame = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame.pack(expand=True)
        self.frame_atual = frame

        tk.Label(
            frame,
            text="Bem-vindo ao Jogo de Digitação",
            font=config.FONTE,
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        ).pack(pady=10)
        
        tk.Label(
            frame,
            text="Escolha uma opção para continuar:",
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Entrar",
            width=15,
            command=lambda: self.mostrar_form_login(frame, modo="entrar")
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Registrar",
            width=15,
            command=lambda: self.mostrar_form_login(frame, modo="registrar")
        ).pack(pady=5)

    # --------- Tela Login (etapa 2: formulário de usuário/senha) ---------
    def mostrar_form_login(self, frame_antigo, modo="entrar"):
        # limpa o conteúdo do mesmo frame
        for widget in frame_antigo.winfo_children():
            widget.destroy()
        frame = frame_antigo

        titulo = "Entrar" if modo == "entrar" else "Registrar"

        tk.Label(
            frame,
            text=titulo,
            font=config.FONTE,
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Nome de usuário:",
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        ).pack()
        entry_user = tk.Entry(frame, font=config.FONTE)
        entry_user.pack(pady=5)

        tk.Label(
            frame,
            text="Senha:",
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        ).pack()
        entry_pwd = tk.Entry(frame, font=config.FONTE, show="*")
        entry_pwd.pack(pady=5)

        lbl_msg = tk.Label(frame, text="", bg=config.COR_FUNDO, fg="red")
        lbl_msg.pack(pady=5)

        def acao_entrar():
            u = entry_user.get()
            p = entry_pwd.get()
            if login.verificar_login(u, p):
                self.usuario_logado = u
                self.mostrar_tela_seletor()
            else:
                lbl_msg.config(text="Usuário ou senha inválidos.", fg="red")

        def acao_registrar():
            u = entry_user.get()
            p = entry_pwd.get()
            ok, msg = login.cadastrar_usuario(u, p)
            lbl_msg.config(text=msg, fg="green" if ok else "red")
            if ok:
                # após registrar, já entra no jogo logado
                self.usuario_logado = u
                self.mostrar_tela_seletor()

        if modo == "entrar":
            tk.Button(frame, text="Entrar", command=acao_entrar).pack(pady=5)
        else:
            tk.Button(frame, text="Registrar", command=acao_registrar).pack(pady=5)

        tk.Button(
            frame,
            text="Voltar",
            command=self.mostrar_tela_login
        ).pack(pady=5)

    # --------- Tela Seletor de Teclado ---------
    def mostrar_tela_seletor(self):
        self.limpar_tela()
        frame = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame.pack(expand=True)
        self.frame_atual = frame

        tk.Label(
            frame,
            text=f"Bem-vindo, {self.usuario_logado}!\nEscolha o teclado:",
            font=("Arial", 14),
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        ).pack(pady=20)

        tk.Button(
            frame,
            text="Português (ABNT)",
            command=lambda: self.mostrar_tela_jogo("pt")
        ).pack(pady=5)

        tk.Button(
            frame,
            text="Inglês Internacional",
            command=lambda: self.mostrar_tela_jogo("en")
        ).pack(pady=5)

    # --------- Tela Jogo ---------
    def mostrar_tela_jogo(self, tipo_teclado):
        self.limpar_tela()
        frame = tk.Frame(self.root, bg=config.COR_FUNDO)
        frame.pack(expand=True, fill="both")
        self.frame_atual = frame

        texto = gerador.gerar_texto()

        def repetir():
            self.mostrar_tela_jogo(tipo_teclado)

        def voltar_menu():
            self.mostrar_tela_seletor()

        jogo = InterfaceJogo(
            frame,
            tipo_teclado,
            on_fim=repetir,
            on_voltar_menu=voltar_menu,
            usuario=self.usuario_logado
        )
        jogo.definir_texto(texto)
        jogo.iniciar()

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
