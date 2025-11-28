import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import config
import time
import ranked

class InterfaceJogo:
    def __init__(self, root, tipo_teclado, on_fim, on_voltar_menu, usuario=None):
        self.root = root
        self.tipo_teclado = tipo_teclado
        self.on_fim = on_fim
        self.on_voltar_menu = on_voltar_menu
        self.usuario = usuario  # usuário logado

        self.root.configure(bg=config.COR_FUNDO)

        self.frame_centro = tk.Frame(root, bg=config.COR_FUNDO)
        self.frame_centro.pack(expand=True, fill="both")

        # Cronômetro
        self.tempo_restante = config.TEMPO
        self.label_tempo = tk.Label(
            self.frame_centro,
            text=f"Tempo: {self.tempo_restante}s",
            font=("Arial", 16),
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        )
        self.label_tempo.pack(pady=5)

        # Texto-alvo (escondido até clicar Pronto)
        self.label_texto = tk.Label(
            self.frame_centro,
            font=config.FONTE,
            fg=config.COR_TEXTO,
            bg=config.COR_FUNDO,
            wraplength=900,
            justify="center",
            text="(A frase será exibida após você clicar em PRONTO)"
        )
        self.label_texto.pack(pady=20)

        # Caixa de digitação (desabilitada até Pronto)
        self.caixa_digitacao = tk.Entry(self.frame_centro, font=config.FONTE, width=60, state="disabled")
        self.caixa_digitacao.pack(pady=10)
        self.caixa_digitacao.bind("<Return>", self.finalizar_digitacao)

        # Botão Pronto
        self.btn_pronto = tk.Button(
            self.frame_centro,
            text="Pronto",
            font=("Arial", 14),
            command=self.comecar
        )
        self.btn_pronto.pack(pady=10)

        # Área para botões finais / ranking
        self.frame_botoes_finais = tk.Frame(self.frame_centro, bg=config.COR_FUNDO)
        self.frame_botoes_finais.pack(pady=10)

        self.texto = ""
        self.tempo_inicio = None
        self.timer_id = None

    def definir_texto(self, texto):
        self.texto = texto
        self.label_texto.config(text="(A frase será exibida após você clicar em PRONTO)")
        self.caixa_digitacao.delete(0, tk.END)
        self.tempo_restante = config.TEMPO
        self.label_tempo.config(text=f"Tempo: {self.tempo_restante}s")

    def iniciar(self):
        self.caixa_digitacao.configure(state="disabled")

    def comecar(self):
        # Mostra frase e libera digitação
        self.btn_pronto.config(state="disabled")
        self.label_texto.config(text=self.texto)
        self.caixa_digitacao.configure(state="normal")
        self.caixa_digitacao.delete(0, tk.END)
        self.caixa_digitacao.focus_set()

        self.tempo_inicio = time.time()
        self.tempo_restante = config.TEMPO
        self.atualizar_cronometro()

    def atualizar_cronometro(self):
        self.label_tempo.config(text=f"Tempo: {self.tempo_restante}s")
        if self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.timer_id = self.root.after(1000, self.atualizar_cronometro)
        else:
            self.caixa_digitacao.configure(state="disabled")
            self.finalizar_digitacao()

    def finalizar_digitacao(self, event=None):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        digitado = self.caixa_digitacao.get().strip()
        self.caixa_digitacao.configure(state="disabled")

        if not self.tempo_inicio:
            messagebox.showwarning("Aviso", "Clique em 'Pronto' para começar.")
            return

        tempo_total = time.time() - self.tempo_inicio

        if digitado == self.texto.strip():
            palavras_acertadas = len(self.texto.split())
            pontos = self.calcular_pontos(palavras_acertadas, tempo_total)
            messagebox.showinfo(
                "Resultado",
                f"Você digitou corretamente!\n"
                f"Tempo: {tempo_total:.2f}s\n"
                f"Palavras: {palavras_acertadas}\n"
                f"Pontuação: {pontos}"
            )
            self.salvar_no_ranking(pontos)
        else:
            messagebox.showwarning("Erro", "Texto digitado não confere com o original!")

        self.mostrar_botoes_finais()

    def calcular_pontos(self, palavras_acertadas, tempo_segundos):
        pontos = (palavras_acertadas * 2) - int(tempo_segundos / 5)
        return max(pontos, 0)

    def salvar_no_ranking(self, pontos):
        if self.usuario:
            nome = self.usuario
        else:
            nome = simpledialog.askstring("Ranking", "Digite seu nome:")

        if not nome:
            return

        ranked.salvar_pontos(nome, pontos)

    def mostrar_botoes_finais(self):
        for widget in self.frame_botoes_finais.winfo_children():
            widget.destroy()

        btn_repetir = tk.Button(
            self.frame_botoes_finais,
            text="Repetir",
            font=config.FONTE,
            command=self.on_fim
        )
        btn_repetir.pack(pady=5)

        btn_ranking = tk.Button(
            self.frame_botoes_finais,
            text="Ver Ranking",
            font=config.FONTE,
            command=self.mostrar_ranking
        )
        btn_ranking.pack(pady=5)

        btn_sair = tk.Button(
            self.frame_botoes_finais,
            text="Voltar ao Menu",
            font=config.FONTE,
            command=self.on_voltar_menu
        )
        btn_sair.pack(pady=5)

    def mostrar_ranking(self):
        for widget in self.frame_centro.winfo_children():
            widget.destroy()

        label = tk.Label(
            self.frame_centro,
            text="Ranking de Jogadores",
            font=config.FONTE,
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO
        )
        label.pack(pady=10)

        tree = ttk.Treeview(self.frame_centro, columns=("Nome", "Pontos"), show="headings", height=10)
        tree.heading("Nome", text="Nome")
        tree.heading("Pontos", text="Pontos")
        tree.pack(padx=20, pady=20)

        ranking = ranked.carregar_ranking()
        ranking.sort(key=lambda x: x[1], reverse=True)
        for nome, pontos in ranking:
            tree.insert("", "end", values=(nome, pontos))

        btn_voltar = tk.Button(
            self.frame_centro,
            text="Voltar ao Menu",
            font=config.FONTE,
            command=self.on_voltar_menu
        )
        btn_voltar.pack(pady=10)
