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

        frame_centro = tk.Frame(root, bg=config.COR_FUNDO)
        frame_centro.pack(expand=True)

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

    def iniciar_jogo(self, tipo_teclado):
        self.root.destroy()
        self.loop_jogo(tipo_teclado)

    def loop_jogo(self, tipo_teclado):
        root = tk.Tk()
        root.title("Jogo de Digitação")
        root.configure(bg=config.COR_FUNDO)
        root.geometry(config.TELA)

        def repetir():
            root.destroy()
            self.loop_jogo(tipo_teclado)

        def sair():
            root.destroy()

        texto_para_digitar = gerador.gerar_texto()
        tela_jogo = interface.Interface(root, tipo_teclado, repetir_callback=repetir, sair_callback=sair)
        tela_jogo.definir_texto(texto_para_digitar)
        tela_jogo.iniciar()

        root.mainloop()

def main():
    root = tk.Tk()
    SeletorTeclado(root)
    root.mainloop()

if __name__ == "__main__":
    main()
