import tkinter as tk
import config

class Interface:
    def __init__(self, root, tipo_teclado):
        self.root = root
        self.tipo_teclado = tipo_teclado

        self.root.configure(bg=config.COR_FUNDO)

        self.frame_centro = tk.Frame(root, bg=config.COR_FUNDO)
        self.frame_centro.pack(expand=True)

        self.label_texto = tk.Label(
            self.frame_centro,
            font=config.FONTE,
            fg=config.COR_TEXTO,
            bg=config.COR_FUNDO,
            wraplength=900,
            justify="center"
        )
        self.label_texto.pack(pady=20)

        self.caixa_digitacao = tk.Entry(self.frame_centro, font=config.FONTE, width=60)
        self.caixa_digitacao.pack(pady=10)
        self.caixa_digitacao.bind("<KeyRelease>", self.tecla_pressionada)

        self.texto = ""

    def definir_texto(self, texto):
        self.texto = texto
        self.label_texto.config(text=self.texto)
        self.caixa_digitacao.delete(0, tk.END)

    def tecla_pressionada(self, event):
        digitado = self.caixa_digitacao.get()

        if self.tipo_teclado == "pt":
            pass
        elif self.tipo_teclado == "en":
            pass

        print(f"Digitado: {digitado}")

    def iniciar(self):
        self.caixa_digitacao.focus_set()
