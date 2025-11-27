import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import config
import time
import ranked
import gerador

class Interface:
    def __init__(self, root, tipo_teclado, repetir_callback=None, sair_callback=None):
        self.root = root
        self.tipo_teclado = tipo_teclado
        self.repetir_callback = repetir_callback
        self.sair_callback = sair_callback

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
        self.caixa_digitacao.bind("<Return>", self.finalizar_digitacao)  # ENTER finaliza

        self.texto = ""
        self.tempo_inicio = None

    def definir_texto(self, texto):
        self.texto = texto
        self.label_texto.config(text=self.texto)
        self.caixa_digitacao.delete(0, tk.END)
        self.tempo_inicio = time.time()  # reinicia tempo

    def iniciar(self):
        self.caixa_digitacao.focus_set()

    # ---------------- Ranking automático ----------------
    def finalizar_digitacao(self, event=None):
        digitado = self.caixa_digitacao.get().strip()
        if digitado == self.texto.strip():  # só considera se acertou a frase
            tempo_total = time.time() - self.tempo_inicio
            palavras_acertadas = len(self.texto.split())
            pontos = self.calcular_pontos(palavras_acertadas, tempo_total)

            # mostra tempo e segundos
            messagebox.showinfo("Resultado",
                                f"Você digitou corretamente!\n"
                                f"Tempo gasto: {tempo_total:.2f} segundos\n"
                                f"Palavras corretas: {palavras_acertadas}\n"
                                f"Pontuação: {pontos}")

            # pede nome e impede repetição
            nome = simpledialog.askstring("Ranking", "Digite seu nome:")
            if nome:
                ranking = ranked.carregar_ranking()
                nomes_existentes = [n for n, _ in ranking]
                if nome in nomes_existentes:
                    messagebox.showwarning("Aviso", "Esse nome já existe no ranking!")
                else:
                    ranked.salvar_pontos(nome, pontos)
            # abre janela final
            self.janela_final()
        else:
            messagebox.showwarning("Erro", "Texto digitado não confere com o original!")

    def calcular_pontos(self, palavras_acertadas, tempo_segundos):
        # Fórmula enxuta: cada palavra vale 2 pontos, penaliza 1 ponto a cada 5 segundos
        pontos = (palavras_acertadas * 2) - int(tempo_segundos / 5)
        return max(pontos, 0)

    def mostrar_ranking(self):
        ranking = ranked.carregar_ranking()
        ranking.sort(key=lambda x: x[1], reverse=True)

        # Janela bonitinha com Treeview
        janela = tk.Toplevel(self.root)
        janela.title("Ranking")
        janela.configure(bg=config.COR_FUNDO)

        label = tk.Label(janela, text="Ranking de Jogadores", font=config.FONTE,
                         bg=config.COR_FUNDO, fg=config.COR_TEXTO)
        label.pack(pady=10)

        tree = ttk.Treeview(janela, columns=("Nome", "Pontos"), show="headings", height=10)
        tree.heading("Nome", text="Nome")
        tree.heading("Pontos", text="Pontos")
        tree.pack(padx=20, pady=20)

        for nome, pontos in ranking:
            tree.insert("", "end", values=(nome, pontos))

    def janela_final(self):
        janela = tk.Toplevel(self.root)
        janela.title("Fim da Rodada")
        janela.configure(bg=config.COR_FUNDO)

        label = tk.Label(janela, text="O que deseja fazer?", font=config.FONTE,
                         bg=config.COR_FUNDO, fg=config.COR_TEXTO)
        label.pack(pady=20)

        btn_repetir = tk.Button(janela, text="Repetir", font=config.FONTE,
                                command=lambda: [janela.destroy(), self.repetir_callback()])
        btn_repetir.pack(pady=10)

        btn_ranking = tk.Button(janela, text="Ver Ranking", font=config.FONTE,
                                command=self.mostrar_ranking)
        btn_ranking.pack(pady=10)

        btn_sair = tk.Button(janela, text="Sair", font=config.FONTE,
                             command=lambda: [janela.destroy(), self.sair_callback()])
        btn_sair.pack(pady=10)
