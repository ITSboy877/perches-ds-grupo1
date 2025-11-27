import tkinter as tk
import config

class Interface:
    def __init__(self, root, tipo_teclado):
        self.root = root
        self.tipo_teclado = tipo_teclado

        self.label_texto = tk.Label(
            root,
            font=config.FONTE,
            fg=config.COR_TEXTO,
            bg=config.COR_FUNDO,
            wraplength=750,
            justify="left"
        )
        self.label_texto.pack(pady=20)

        self.caixa_digitacao = tk.Entry(root, font=config.FONTE, width=60)
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
            # Aqui você pode tratar algo específico do teclado PT se quiser
            pass
        elif self.tipo_teclado == "en":
            # Aqui você pode tratar algo específico do teclado EN se quiser
            pass

        print(f"Digitado: {digitado}")

    def iniciar(self):
        self.caixa_digitacao.focus_set()
