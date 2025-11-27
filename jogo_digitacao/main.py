import tkinter as tk
import config
import interface
import gerador

class SeletorTeclado:
    def __init__(self, root):
        self.root = root
        self.root.title("Selecionar Teclado")
        self.root.geometry("300x150")
        self.root.configure(bg=config.COR_FUNDO)

        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.sair_fullscreen)

        # frame central
        frame_centro = tk.Frame(root, bg=config.COR_FUNDO)
        frame_centro.pack(expand=True)  # centraliza vertical/horizontal

        label = tk.Label(
            frame_centro,
            text="Escolha o teclado:",
            font=("Arial", 14),
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        )
        label.pack(pady=20)

        btn_pt = tk.Button(frame_centro, text="Português (ABNT)", command=lambda: self.iniciar_jogo("pt"))
        btn_en = tk.Button(frame_centro, text="Inglês Internacional", command=lambda: self.iniciar_jogo("en"))

        btn_pt.pack(pady=5)
        btn_en.pack(pady=5)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def sair_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def iniciar_jogo(self, tipo_teclado):
        estava_full = self.fullscreen
        self.root.destroy()

        root = tk.Tk()
        root.title("Jogo de Digitação")
        root.configure(bg=config.COR_FUNDO)
        root.geometry(config.TELA)
        root.attributes("-fullscreen", estava_full)
        root.bind("<F11>", lambda e: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
        root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

        texto_para_digitar = gerador.gerar_texto()
        tela_jogo = interface.Interface(root, tipo_teclado)
        tela_jogo.definir_texto(texto_para_digitar)
        tela_jogo.iniciar()

        root.mainloop()

def main():
    root = tk.Tk()
    SeletorTeclado(root)
    root.mainloop()

if __name__ == "__main__":
    main()
