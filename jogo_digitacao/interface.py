import tkinter as tk
from tkinter import ttk
import config
import time
import ranked
import login

class InterfaceJogo:
    def __init__(self, root, tipo_teclado, modo_jogo, on_fim, on_voltar_menu, usuario=None, logo_img=None, sessao_multi=None):
        self.root = root
        self.tipo_teclado = tipo_teclado
        self.modo_jogo = modo_jogo
        self.on_fim = on_fim
        self.on_voltar_menu = on_voltar_menu
        self.usuario = usuario
        self.logo_img = logo_img
        self.sessao_multi = sessao_multi
        
        self.root.configure(bg=config.COR_FUNDO)
        
        # Variáveis de controle
        self.texto = ""
        self.tempo_inicio = None
        self.timer_id = None
        self.tempo_restante = config.TEMPO_POR_MODO.get(self.modo_jogo, config.TEMPO)
        self.combo_atual = 0
        self.combo_maximo = 0
        self.wpm_atual = 0
        self.caracteres_digitados = 0
        
        # =============== LAYOUT PRINCIPAL ===============
        frame_main = tk.Frame(root, bg=config.COR_FUNDO)
        frame_main.pack(expand=True, fill="both", padx=15, pady=15)
        
        # =============== PAINEL ESQUERDO - RANKING ===============
        self.frame_ranking = tk.Frame(
            frame_main,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=15,
            pady=15
        )
        self.frame_ranking.pack(side="left", fill="y", padx=(0, 10))
        
        # Título do ranking
        modo_nome = next((nome for mid, nome in config.MODOS_JOGO if mid == self.modo_jogo), "Normal")
        
        if self.modo_jogo == "normal":
            cor_modo = config.COR_NORMAL
        elif self.modo_jogo == "morte_subita":
            cor_modo = config.COR_MORTE_SUBITA
        else:
            cor_modo = config.COR_HARDCORE
        
        tk.Label(
            self.frame_ranking,
            text=f"🏆 Top {modo_nome}",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=cor_modo
        ).pack(pady=(0, 5))
        
        tk.Label(
            self.frame_ranking,
            text=f"Modo: {modo_nome}",
            font=config.FONTE_MINI,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(0, 15))
        
        # Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Ranking.Treeview",
            background=config.COR_CARD_DESTAQUE,
            foreground=config.COR_TEXTO,
            fieldbackground=config.COR_CARD_DESTAQUE,
            borderwidth=0,
            font=config.FONTE_STATS,
            rowheight=35
        )
        style.configure(
            "Ranking.Treeview.Heading",
            background=config.COR_FRAME,
            foreground=config.COR_TEXTO_DESTAQUE,
            borderwidth=0,
            font=config.FONTE_TEXTO,
            relief="flat"
        )
        style.map(
            "Ranking.Treeview",
            background=[("selected", config.COR_BOTAO)],
            foreground=[("selected", config.COR_BOTAO_TEXTO)]
        )
        
        self.tree_lateral = ttk.Treeview(
            self.frame_ranking,
            columns=("Pos", "Nome", "Pontos"),
            show="headings",
            height=12,
            style="Ranking.Treeview"
        )
        
        self.tree_lateral.heading("Pos", text="#", anchor="center")
        self.tree_lateral.heading("Nome", text="Jogador", anchor="w")
        self.tree_lateral.heading("Pontos", text="Pontos", anchor="center")
        
        self.tree_lateral.column("Pos", width=50, anchor="center", minwidth=50)
        self.tree_lateral.column("Nome", width=140, anchor="w", minwidth=100)
        self.tree_lateral.column("Pontos", width=90, anchor="center", minwidth=70)
        
        self.tree_lateral.pack(fill="both", expand=True, pady=(10, 0))
        
        self.atualizar_ranking_lateral()
        
        # =============== PAINEL DIREITO - JOGO ===============
        frame_direita = tk.Frame(frame_main, bg=config.COR_FUNDO)
        frame_direita.pack(side="right", expand=True, fill="both")
        
        self.frame_centro = tk.Frame(
            frame_direita,
            bg=config.COR_FRAME,
            bd=0,
            highlightthickness=2,
            highlightbackground=config.COR_FRAME_BORDA,
            padx=40,
            pady=30
        )
        self.frame_centro.pack(expand=True, fill="both")
        
        # =============== HEADER - INFO DO JOGO ===============
        header_frame = tk.Frame(self.frame_centro, bg=config.COR_FRAME)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Tempo
        self.label_tempo = tk.Label(
            header_frame,
            text=f"⏱️ {self.tempo_restante}s",
            font=config.FONTE_TITULO,
            bg=config.COR_FRAME,
            fg=config.COR_INFO
        )
        self.label_tempo.pack(side="left")
        
        # WPM
        self.label_wpm = tk.Label(
            header_frame,
            text="⚡ 0 WPM",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        )
        self.label_wpm.pack(side="right")
        
        # =============== BARRA DE PROGRESSO ===============
        self.canvas_progresso = tk.Canvas(
            self.frame_centro,
            height=12,
            bg=config.COR_PROGRESSO_BG,
            highlightthickness=0
        )
        self.canvas_progresso.pack(fill="x", pady=(0, 20))
        
        # =============== TEXTO DA FRASE ===============
        self.label_texto = tk.Label(
            self.frame_centro,
            font=config.FONTE_MONO,
            fg=config.COR_TEXTO,
            bg=config.COR_FRAME,
            wraplength=900,
            justify="center",
            text="Clique em INICIAR para começar",
            pady=20
        )
        self.label_texto.pack(pady=15)
        
        # =============== CAMPO DE DIGITAÇÃO ===============
        self.caixa_digitacao = tk.Entry(
            self.frame_centro,
            font=config.FONTE_MONO,
            width=50,
            state="disabled",
            bg=config.COR_CARD_DESTAQUE,
            fg=config.COR_TEXTO,
            insertbackground=config.COR_TEXTO,
            relief="flat",
            bd=0,
            justify="center"
        )
        
        self.caixa_digitacao.bind("<KeyRelease>", self.verificar_digitacao_tempo_real)
        self.caixa_digitacao.bind("<Return>", self.finalizar_digitacao)
        
        # =============== INDICADOR DE COMBO ===============
        self.label_combo = tk.Label(
            self.frame_centro,
            text="",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_COMBO_1
        )
        self.label_combo.pack(pady=10)
        
        # =============== BOTÃO INICIAR ===============
        self.btn_pronto = tk.Button(
            self.frame_centro,
            text="🚀 INICIAR",
            font=config.FONTE_TEXTO_GRANDE,
            bg=config.COR_SUCESSO,
            fg=config.COR_BOTAO_TEXTO,
            activebackground=config.COR_SUCESSO_CLARO,
            activeforeground=config.COR_BOTAO_TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.comecar,
            width=20,
            height=2
        )
        self.btn_pronto.pack(pady=20)
        
        self.btn_pronto.bind("<Enter>", lambda e: self.btn_pronto.config(bg=config.COR_SUCESSO_CLARO))
        self.btn_pronto.bind("<Leave>", lambda e: self.btn_pronto.config(bg=config.COR_SUCESSO))
        
        # =============== FRAMES DE RESULTADO ===============
        self.frame_resultado = tk.Frame(self.frame_centro, bg=config.COR_FRAME)
        self.frame_resultado.pack(pady=5, fill="x")
        
        self.frame_botoes_finais = tk.Frame(self.frame_centro, bg=config.COR_FRAME)
        self.frame_botoes_finais.pack(pady=5)

    # =============== RANKING ===============
    def atualizar_ranking_lateral(self):
        """Atualiza o ranking lateral"""
        for item in self.tree_lateral.get_children():
            self.tree_lateral.delete(item)
        
        ranking_completo = ranked.carregar_ranking()
        ranking_modo = [r for r in ranking_completo if len(r) >= 5 and r[4] == self.modo_jogo]
        ranking_modo.sort(key=lambda x: x[1], reverse=True)
        
        top = ranking_modo[:config.RANKING_TOP_EXIBIR]
        
        for idx, entrada in enumerate(top, 1):
            nome = entrada[0] if len(entrada) > 0 else "Jogador"
            pontos = entrada[1] if len(entrada) > 1 else 0
            
            if idx == 1:
                pos_text = "🥇"
            elif idx == 2:
                pos_text = "🥈"
            elif idx == 3:
                pos_text = "🥉"
            else:
                pos_text = f"{idx}º"
            
            self.tree_lateral.insert("", "end", values=(pos_text, nome, f"{int(pontos)}"))
        
        if len(top) == 0:
            self.tree_lateral.insert("", "end", values=("", "Nenhum registro", 0))

    # =============== CONTROLE DO JOGO ===============
    def definir_texto(self, texto):
        """Define o texto e prepara a interface"""
        # Limpa bindings anteriores
        try:
            self.root.unbind("<Return>")
            self.root.unbind("<space>")
        except:
            pass
        
        self.texto = texto
        self.label_texto.config(text="Clique em INICIAR para começar")
        self.caixa_digitacao.delete(0, tk.END)
        self.caixa_digitacao.configure(state="disabled")
        self.caixa_digitacao.pack_forget()
        
        self.tempo_restante = config.TEMPO_POR_MODO.get(self.modo_jogo, config.TEMPO)
        self.label_tempo.config(text=f"⏱️ {self.tempo_restante}s")
        
        self.combo_atual = 0
        self.combo_maximo = 0
        self.caracteres_digitados = 0
        self.label_combo.config(text="")
        
        for w in self.frame_resultado.winfo_children():
            w.destroy()
        for w in self.frame_botoes_finais.winfo_children():
            w.destroy()
        
        self.atualizar_barra_progresso(0)
        self.btn_pronto.pack_forget()
        self.btn_pronto.config(state="normal")
        self.btn_pronto.pack(pady=20)
        
        self.root.bind("<Return>", lambda e: self.comecar())
        self.root.bind("<space>", lambda e: self.comecar())

    def comecar(self):
        """Inicia o jogo"""
        try:
            self.root.unbind("<Return>")
            self.root.unbind("<space>")
        except:
            pass
        
        self.btn_pronto.pack_forget()
        self.label_texto.config(text=self.texto)
        
        self.caixa_digitacao.pack(pady=15, ipady=12)
        self.caixa_digitacao.configure(state="normal")
        self.caixa_digitacao.delete(0, tk.END)
        self.caixa_digitacao.focus_set()
        
        self.tempo_inicio = time.time()
        self.tempo_restante = config.TEMPO_POR_MODO.get(self.modo_jogo, config.TEMPO)
        self.atualizar_cronometro()

    def atualizar_cronometro(self):
        if self.tempo_restante <= 10:
            cor_tempo = config.COR_ERRO
        elif self.tempo_restante <= 20:
            cor_tempo = config.COR_AVISO
        else:
            cor_tempo = config.COR_INFO
        
        self.label_tempo.config(text=f"⏱️ {self.tempo_restante}s", fg=cor_tempo)
        
        if self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.timer_id = self.root.after(1000, self.atualizar_cronometro)
        else:
            self.caixa_digitacao.configure(state="disabled")
            self.finalizar_digitacao()

    # =============== FEEDBACK TEMPO REAL ===============
    def verificar_digitacao_tempo_real(self, event=None):
        """Atualiza WPM, progresso e combo"""
        if not self.tempo_inicio:
            return
        
        digitado = self.caixa_digitacao.get()
        self.caracteres_digitados = len(digitado)
        
        tempo_decorrido = time.time() - self.tempo_inicio
        if tempo_decorrido > 0:
            self.wpm_atual = (len(digitado) / 5) / (tempo_decorrido / 60.0)
            self.label_wpm.config(text=f"⚡ {int(self.wpm_atual)} WPM")
        
        progresso = min(len(digitado) / len(self.texto), 1.0) if len(self.texto) > 0 else 0
        self.atualizar_barra_progresso(progresso)
        
        corretos_consecutivos = 0
        for i, char in enumerate(digitado):
            if i < len(self.texto) and char == self.texto[i]:
                corretos_consecutivos += 1
            else:
                corretos_consecutivos = 0
        
        self.combo_atual = corretos_consecutivos
        if self.combo_atual > self.combo_maximo:
            self.combo_maximo = self.combo_atual
        
        self.atualizar_label_combo()
        
        if self.modo_jogo == "morte_subita":
            for i, char in enumerate(digitado):
                if i < len(self.texto) and char != self.texto[i]:
                    self.caixa_digitacao.configure(state="disabled")
                    self.root.after(300, self.finalizar_digitacao)
                    break

    def atualizar_label_combo(self):
        """Atualiza o label de combo"""
        if self.combo_atual < 10:
            self.label_combo.config(text="")
            return
        
        cor = config.COR_COMBO_1
        texto = f"🔥 Combo: {self.combo_atual}"
        
        for nivel, mensagem, cor_nivel in reversed(config.NIVEIS_COMBO):
            if self.combo_atual >= nivel:
                cor = cor_nivel
                texto = f"{mensagem} Combo: {self.combo_atual}!"
                break
        
        self.label_combo.config(text=texto, fg=cor)

    def atualizar_barra_progresso(self, progresso):
        """Atualiza a barra de progresso"""
        self.canvas_progresso.delete("all")
        largura = self.canvas_progresso.winfo_width()
        if largura <= 1:
            largura = 800
        altura = 12
        
        largura_progresso = int(largura * progresso)
        
        if largura_progresso > 0:
            if progresso < 0.3:
                cor = config.COR_ERRO
            elif progresso < 0.7:
                cor = config.COR_AVISO
            else:
                cor = config.COR_SUCESSO
            
            self.canvas_progresso.create_rectangle(0, 0, largura_progresso, altura, fill=cor, outline="")

    def esconder_cabecalho(self):
        """Esconde elementos do cabeçalho"""
        self.label_tempo.pack_forget()
        self.label_texto.pack_forget()
        self.caixa_digitacao.delete(0, tk.END)
        self.caixa_digitacao.pack_forget()
        self.label_combo.pack_forget()
        self.label_wpm.pack_forget()
        self.canvas_progresso.pack_forget()

    # =============== FINALIZAÇÃO ===============
    def finalizar_digitacao(self, event=None):
        """Finaliza a rodada"""
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        digitado = self.caixa_digitacao.get().strip()
        self.caixa_digitacao.configure(state="disabled")
        
        if not self.tempo_inicio:
            self.mostrar_mensagem("Clique em INICIAR para começar.", erro=True)
            return
        
        tempo_total = time.time() - self.tempo_inicio
        original = self.texto.strip()
        
        corretos, errados, total, lista_flags, combo_max = self.comparar_textos(original, digitado)
        
        if total == 0:
            self.mostrar_mensagem("Você não digitou nada.", erro=True)
            self.esconder_cabecalho()
            self.mostrar_botoes_finais()
            return
        
        pontos, bonus_combo = self.calcular_pontos(corretos, errados, tempo_total, combo_max)
        precisao = (corretos / total * 100) if total > 0 else 0.0
        wpm = (corretos / 5) / (tempo_total / 60.0) if tempo_total > 0 else 0
        
        if self.modo_jogo == "morte_subita" and errados > 0:
            pontos = 0
        
        self.mostrar_resultado(corretos, errados, total, tempo_total, pontos, wpm, precisao, combo_max, bonus_combo)

    # =============== COMPARAÇÃO E PONTUAÇÃO ===============
    def comparar_textos(self, original: str, digitado: str):
        """Compara caractere a caractere"""
        lista_flags = []
        tamanho = max(len(original), len(digitado))
        corretos = 0
        errados = 0
        combo_atual = 0
        combo_max = 0
        
        for i in range(tamanho):
            c_orig = original[i] if i < len(original) else ""
            c_dig = digitado[i] if i < len(digitado) else ""
            
            if c_orig == c_dig and c_orig != "":
                corretos += 1
                combo_atual += 1
                if combo_atual > combo_max:
                    combo_max = combo_atual
                lista_flags.append((c_orig, c_dig, True))
            else:
                if c_orig != "" or c_dig != "":
                    errados += 1
                    combo_atual = 0
                    lista_flags.append((c_orig, c_dig, False))
                
                if self.modo_jogo == "morte_subita" and errados > 0:
                    for j in range(i + 1, tamanho):
                        c_orig2 = original[j] if j < len(original) else ""
                        if c_orig2 != "":
                            errados += 1
                            lista_flags.append((c_orig2, "", False))
                    break
        
        total = corretos + errados
        return corretos, errados, total, lista_flags, combo_max

    def calcular_pontos(self, caracteres_corretos, caracteres_errados, tempo_segundos, combo_max):
        """Calcula pontos"""
        pesos = config.PESOS_PONTOS.get(self.modo_jogo, config.PESOS_PONTOS["normal"])
        
        base = caracteres_corretos * pesos["ponto_por_correto"]
        penalidade_erros = caracteres_errados * pesos["penalidade_por_erro"]
        penalidade_tempo = int(tempo_segundos / 5) * pesos["penalidade_tempo_5s"]
        
        pontos = base - penalidade_erros - penalidade_tempo
        
        bonus_combo = 0
        if combo_max >= 50:
            bonus_combo = int(pontos * 0.3)
        elif combo_max >= 30:
            bonus_combo = int(pontos * 0.2)
        elif combo_max >= 20:
            bonus_combo = int(pontos * 0.1)
        
        pontos += bonus_combo
        
        return max(pontos, 0), bonus_combo

    # =============== CONQUISTAS E XP ===============
    def verificar_conquistas(self, wpm, precisao, errados, combo_max):
        """Verifica conquistas"""
        if not self.usuario:
            return [], 0
        
        stats = login.obter_stats_usuario(self.usuario)
        if not stats:
            return [], 0
        
        conquistas_atuais = stats.get("conquistas", [])
        novas_conquistas = []
        xp_total_conquistas = 0
        
        if "velocista" not in conquistas_atuais and wpm >= 60:
            xp_ganho = login.adicionar_conquista(self.usuario, "velocista")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("velocista")
        
        if "mestre" not in conquistas_atuais and wpm >= 80:
            xp_ganho = login.adicionar_conquista(self.usuario, "mestre")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("mestre")
        
        if "perfeito" not in conquistas_atuais and errados == 0:
            xp_ganho = login.adicionar_conquista(self.usuario, "perfeito")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("perfeito")
        
        if "flash" not in conquistas_atuais and wpm >= 100:
            xp_ganho = login.adicionar_conquista(self.usuario, "flash")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("flash")
        
        if "combo_master" not in conquistas_atuais and combo_max >= 50:
            xp_ganho = login.adicionar_conquista(self.usuario, "combo_master")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("combo_master")
        
        if "resistencia" not in conquistas_atuais and stats["total_partidas"] >= 10:
            xp_ganho = login.adicionar_conquista(self.usuario, "resistencia")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("resistencia")
        
        if "dedicacao" not in conquistas_atuais and stats["total_partidas"] >= 50:
            xp_ganho = login.adicionar_conquista(self.usuario, "dedicacao")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("dedicacao")
        
        if "maratonista" not in conquistas_atuais and stats["total_partidas"] >= 100:
            xp_ganho = login.adicionar_conquista(self.usuario, "maratonista")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("maratonista")
        
        if "primeira_vitoria" not in conquistas_atuais and stats["total_partidas"] == 1:
            xp_ganho = login.adicionar_conquista(self.usuario, "primeira_vitoria")
            xp_total_conquistas += xp_ganho
            novas_conquistas.append("primeira_vitoria")
        
        return novas_conquistas, xp_total_conquistas

    def processar_xp_e_conquistas(self, wpm, precisao, errados, combo_max):
        """Processa XP e conquistas"""
        novas_conquistas, xp_conquistas = self.verificar_conquistas(wpm, precisao, errados, combo_max)
        
        xp_partida = config.XP_POR_PARTIDA
        xp_partida += int(wpm * config.XP_POR_WPM)
        xp_partida += int(precisao * config.XP_POR_PRECISAO)
        
        if errados == 0:
            xp_partida += config.XP_BONUS_PERFEITO
        
        subiu_nivel, novo_nivel, xp_atual = login.ganhar_xp(self.usuario, xp_partida)
        
        self.mostrar_xp_ganho(xp_partida, subiu_nivel, novo_nivel, xp_atual)
        
        if novas_conquistas:
            self.mostrar_conquistas_desbloqueadas(novas_conquistas)

    # =============== UI DE RESULTADO (COMPACTA) ===============
    def mostrar_mensagem(self, texto, erro=False):
        for w in self.frame_resultado.winfo_children():
            w.destroy()
        
        cor = config.COR_ERRO if erro else config.COR_TEXTO
        tk.Label(self.frame_resultado, text=texto, font=config.FONTE_TEXTO, bg=config.COR_FRAME, fg=cor, justify="center").pack()

    def mostrar_resultado(self, corretos, errados, total, tempo_gasto, pontos, wpm, precisao, combo_max, bonus_combo):
        """Exibe os resultados finais - VERSÃO COMPACTA"""
        for widget in self.frame_resultado.winfo_children():
            widget.destroy()
        
        self.esconder_cabecalho()
        
        # =============== TÍTULO COMPACTO ===============
        if precisao == 100:
            titulo = "🏆 PERFEITO!"
            cor_titulo = config.COR_SUCESSO
        elif precisao >= 90:
            titulo = "⭐ EXCELENTE!"
            cor_titulo = config.COR_SUCESSO
        elif precisao >= 75:
            titulo = "👍 BOM!"
            cor_titulo = config.COR_INFO
        else:
            titulo = "📊 RESULTADO"
            cor_titulo = config.COR_AVISO
        
        tk.Label(
            self.frame_resultado,
            text=titulo,
            font=("Segoe UI", 16, "bold"),
            bg=config.COR_FRAME,
            fg=cor_titulo
        ).pack(pady=(0, 8))
        
        # =============== GRID 2x3 COMPACTO ===============
        container_stats = tk.Frame(self.frame_resultado, bg=config.COR_FRAME)
        container_stats.pack(pady=3, padx=10, fill="x")
        
        def criar_stat_compacto(parent, icone, valor, label, cor, row, col):
            card = tk.Frame(
                parent,
                bg=config.COR_CARD_DESTAQUE,
                bd=0,
                highlightthickness=1,
                highlightbackground=cor,
                padx=8,
                pady=5
            )
            card.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
            
            tk.Label(
                card,
                text=f"{icone} {valor}",
                font=("Segoe UI", 14, "bold"),
                bg=config.COR_CARD_DESTAQUE,
                fg=cor
            ).pack()
            
            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 10),
                bg=config.COR_CARD_DESTAQUE,
                fg=config.COR_TEXTO_SECUNDARIO
            ).pack()
        
        container_stats.grid_columnconfigure(0, weight=1)
        container_stats.grid_columnconfigure(1, weight=1)
        
        # Grid 2x3
        criar_stat_compacto(container_stats, "⚡", f"{wpm:.1f}", "WPM", config.COR_INFO, 0, 0)
        criar_stat_compacto(container_stats, "🎯", f"{precisao:.1f}%", "Precisão", config.COR_SUCESSO if precisao >= 90 else config.COR_AVISO, 0, 1)
        criar_stat_compacto(container_stats, "✅", f"{corretos}", "Corretos", config.COR_SUCESSO, 1, 0)
        criar_stat_compacto(container_stats, "❌", f"{errados}", "Errados", config.COR_ERRO, 1, 1)
        criar_stat_compacto(container_stats, "⏱️", f"{tempo_gasto:.1f}s", "Tempo", config.COR_TEXTO_SECUNDARIO, 2, 0)
        criar_stat_compacto(container_stats, "🏆", f"{pontos}", "Pontos", config.COR_OURO, 2, 1)
        
        # =============== COMBO COMPACTO ===============
        if combo_max >= 10:
            card_combo = tk.Frame(
                self.frame_resultado,
                bg=config.COR_CARD_DESTAQUE,
                bd=0,
                highlightthickness=1,
                highlightbackground=config.COR_COMBO_3,
                padx=8,
                pady=4
            )
            card_combo.pack(pady=4, fill="x", padx=10)
            
            texto_combo = f"🔥 Combo: {combo_max}"
            if bonus_combo > 0:
                texto_combo += f"  (+{bonus_combo} pts)"
            
            tk.Label(
                card_combo,
                text=texto_combo,
                font=("Segoe UI", 12, "bold"),
                bg=config.COR_CARD_DESTAQUE,
                fg=config.COR_COMBO_3
            ).pack()
        
        # =============== MENSAGEM MOTIVACIONAL ===============
        mensagem = ""
        for faixa, msg in config.MENSAGENS_WPM.items():
            if faixa[0] <= wpm < faixa[1]:
                mensagem = msg
                break
        
        if mensagem:
            tk.Label(
                self.frame_resultado,
                text=mensagem,
                font=("Segoe UI", 12),
                bg=config.COR_FRAME,
                fg=config.COR_TEXTO_DESTAQUE
            ).pack(pady=4)
        
        # =============== XP E CONQUISTAS ===============
        if self.usuario and self.sessao_multi is None:
            self.processar_xp_e_conquistas(wpm, precisao, errados, combo_max)
            login.atualizar_stats_usuario(self.usuario, wpm, precisao)
            ranked.salvar_pontos(self.usuario, pontos, wpm, precisao, self.modo_jogo)
            self.atualizar_ranking_lateral()
        elif self.sessao_multi:
            self.sessao_multi.adicionar_resultado(self.usuario, pontos, wpm, precisao, tempo_gasto)
            
            # ✅ MENSAGEM PARA PRÓXIMO JOGADOR
            if not self.sessao_multi.sessao_completa():
                proximo_numero = self.sessao_multi.jogador_atual
                
                frame_proximo = tk.Frame(self.frame_resultado, bg=config.COR_INFO, padx=15, pady=10)
                frame_proximo.pack(pady=8, fill="x", padx=10)
                
                tk.Label(
                    frame_proximo,
                    text=f"👉 Aguardando Jogador {proximo_numero}",
                    font=("Segoe UI", 16, "bold"),
                    bg=config.COR_INFO,
                    fg=config.COR_BOTAO_TEXTO
                ).pack()
                
                tk.Label(
                    frame_proximo,
                    text="Clique em 'Próximo Jogador' quando estiver pronto!",
                    font=("Segoe UI", 12),
                    bg=config.COR_INFO,
                    fg=config.COR_BOTAO_TEXTO
                ).pack(pady=(5, 0))
            else:
                # Último jogador - todos já jogaram
                frame_final = tk.Frame(self.frame_resultado, bg=config.COR_SUCESSO, padx=15, pady=10)
                frame_final.pack(pady=8, fill="x", padx=10)
                
                tk.Label(
                    frame_final,
                    text="✅ Todos os jogadores terminaram!",
                    font=("Segoe UI", 16, "bold"),
                    bg=config.COR_SUCESSO,
                    fg=config.COR_BOTAO_TEXTO
                ).pack()
                
                tk.Label(
                    frame_final,
                    text="Clique em 'Ver Resultados' para ver o ranking final!",
                    font=("Segoe UI", 12),
                    bg=config.COR_SUCESSO,
                    fg=config.COR_BOTAO_TEXTO
                ).pack(pady=(5, 0))
        
        # =============== BOTÕES FINAIS ===============
        self.mostrar_botoes_finais()

    def mostrar_xp_ganho(self, xp_ganho, subiu_nivel, novo_nivel, xp_atual):
        """Mostra XP ganho - COMPACTO"""
        xp_frame = tk.Frame(self.frame_resultado, bg=config.COR_INFO, padx=12, pady=6)
        xp_frame.pack(pady=4, fill="x", padx=10)
        
        if subiu_nivel:
            tk.Label(
                xp_frame, 
                text=f"🎉 NÍVEL UP! {novo_nivel[2]} {novo_nivel[1]}!",
                font=("Segoe UI", 13, "bold"),
                bg=config.COR_INFO, 
                fg=config.COR_BOTAO_TEXTO
            ).pack()
        
        tk.Label(
            xp_frame, 
            text=f"⭐ +{xp_ganho} XP",
            font=("Segoe UI", 11),
            bg=config.COR_INFO, 
            fg=config.COR_BOTAO_TEXTO
        ).pack()
        
        nivel_atual = config.calcular_nivel(xp_atual)
        xp_faltante = config.xp_para_proximo_nivel(xp_atual)
        
        if xp_faltante > 0:
            info_text = f"Nível: {nivel_atual[2]} {nivel_atual[1]} | XP: {xp_atual} | Faltam {xp_faltante} XP para próximo nível"
        else:
            info_text = f"NÍVEL MÁXIMO | XP: {xp_atual}"
        
        tk.Label(
            xp_frame, 
            text=info_text,
            font=("Segoe UI", 9),
            bg=config.COR_INFO, 
            fg=config.COR_BOTAO_TEXTO
        ).pack(pady=(2, 0))

    def mostrar_conquistas_desbloqueadas(self, conquistas_ids):
        """Mostra conquistas - COMPACTO"""
        for conquista_id in conquistas_ids:
            conquista_info = config.CONQUISTAS.get(conquista_id, {})
            
            frame_conquista = tk.Frame(self.frame_resultado, bg=config.COR_OURO, padx=12, pady=5)
            frame_conquista.pack(pady=3, fill="x", padx=10)
            
            tk.Label(
                frame_conquista,
                text=f"🏆 {conquista_info.get('nome', '')} (+{conquista_info.get('xp', 0)} XP)",
                font=("Segoe UI", 11),
                bg=config.COR_OURO,
                fg="#000000"
            ).pack()

    def mostrar_botoes_finais(self):
        """Mostra botões finais"""
        for w in self.frame_botoes_finais.winfo_children():
            w.destroy()
        
        # ✅ VERIFICA SE É MULTIPLAYER
        if self.sessao_multi:
            # Verifica se é o último jogador
            if self.sessao_multi.sessao_completa():
                texto_botao = "📊 Ver Resultados Finais"
                cor_botao = config.COR_BOTAO
            else:
                proximo_numero = self.sessao_multi.jogador_atual
                texto_botao = f"➡️ Próximo: Jogador {proximo_numero}"
                cor_botao = config.COR_SUCESSO
        else:
            # Modo solo
            texto_botao = "🔄 Jogar Novamente"
            cor_botao = config.COR_BOTAO
        
        btn_repetir = tk.Button(
            self.frame_botoes_finais,
            text=texto_botao,
            font=("Segoe UI", 13),
            bg=cor_botao,
            fg=config.COR_BOTAO_TEXTO,
            activebackground=config.COR_BOTAO_HOVER,
            activeforeground=config.COR_BOTAO_TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.on_fim,
            width=25,
            height=1,
            pady=8
        )
        btn_repetir.pack(side="left", padx=8)
        
        btn_repetir.bind("<Enter>", lambda e: btn_repetir.config(bg=config.COR_BOTAO_HOVER))
        btn_repetir.bind("<Leave>", lambda e: btn_repetir.config(bg=cor_botao))
        
        btn_menu = tk.Button(
            self.frame_botoes_finais,
            text="🏠 Menu Principal",
            font=("Segoe UI", 13),
            bg=config.COR_BOTAO_SECUNDARIO,
            fg=config.COR_BOTAO_TEXTO,
            activebackground=config.COR_BOTAO_HOVER,
            activeforeground=config.COR_BOTAO_TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.on_voltar_menu,
            width=18,
            height=1,
            pady=8
        )
        btn_menu.pack(side="left", padx=8)
        
        btn_menu.bind("<Enter>", lambda e: btn_menu.config(bg=config.COR_BOTAO_HOVER))
        btn_menu.bind("<Leave>", lambda e: btn_menu.config(bg=config.COR_BOTAO_SECUNDARIO))
