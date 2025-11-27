import tkinter as tk
import config
import interface
import gerador


class SeletorTeclado:
    def __init__(self, root):
        self.root = root
        self.root.title("Selecionar Teclado")
        self.root.geometry("300x150")

        label = tk.Label(root, text = "Escolha o teclado:", font = ("Arial", 14))
        label.pack(pady = 20)

        btn_pt = tk.Button(root, text = "Português (ABNT)", command = lambda: self.iniciar_jogo("pt"))
        btn_en = tk.Button(root, text = "Inglês Internacional", command = lambda: self.iniciar_jogo("en"))

        btn_pt.pack(pady = 5)
        btn_en.pack(pady = 5)

    def iniciar_jogo(self, tipo_teclado):
        self.root.destroy()

        root = tk.Tk()
        root.title("Jogo de Digitação")
        root.geometry(config.TELA)

        texto_para_digitar = gerador.gerar_texto(tipo_teclado)
        tela_jogo = interface.Interface(root, tipo_teclado)
        tela_jogo.definir_texto(texto_para_digitar)
        tela_jogo.iniciar()

        root.mainloop()


def main():
    root = tk.Tk()
    seletor = SeletorTeclado(root)
    root.mainloop()


if __name__ == "__main__":
    main()
