import tkinter as tk
from tkinter import ttk
import config
import time
import ranked
import login

class InterfaceJogo:
    def __init__(self, root, tipo_teclado, modo_jogo, on_fim, on_voltar_menu, usuario=None, logo_img=None):
        self.root = root
        self.tipo_teclado = tipo_teclado
        self.modo_jogo = modo_jogo
        self.on_fim = on_fim
        self.on_voltar_menu = on_voltar_menu
        self.usuario = usuario
        self.logo_img = logo_img
        
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
        
        # ==================== LAYOUT PRINCIPAL ====================
        frame_main = tk.Frame(root, bg=config.COR_FUNDO)
        frame_main.pack(expand=True, fill="both", padx=15, pady=15)
        
        # ==================== PAINEL ESQUERDO - RANKING ====================
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
        
        # Título do ranking com nome do modo
        modo_nome = next(
            (nome for mid, nome in config.MODOS_JOGO if mid == self.modo_jogo),
            "Normal"
        )
        
        # Cor do modo
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
            text=f"Modo {modo_nome}",
            font=config.FONTE_MINI,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=(0, 15))
        
        # Treeview estilizado para ranking
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
        
        # ==================== PAINEL DIREITO - JOGO ====================
        frame_direita = tk.Frame(frame_main, bg=config.COR_FUNDO)
        frame_direita.pack(side="right", expand=True, fill="both")
        
        # Card do jogo
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
        
        # Logo
        if self.logo_img is not None:
            lbl_logo = tk.Label(self.frame_centro, image=self.logo_img, bg=config.COR_FRAME)
            lbl_logo.place(relx=0.98, rely=0.02, anchor="ne")
        
        # ==================== HEADER - INFO DO JOGO ====================
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
        
        # WPM em tempo real
        self.label_wpm = tk.Label(
            header_frame,
            text="⚡ 0 WPM",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        )
        self.label_wpm.pack(side="right")
        
        # ==================== BARRA DE PROGRESSO ====================
        self.canvas_progresso = tk.Canvas(
            self.frame_centro,
            height=12,
            bg=config.COR_PROGRESSO_BG,
            highlightthickness=0
        )
        self.canvas_progresso.pack(fill="x", pady=(0, 20))
        
        # ==================== TEXTO DA FRASE ====================
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
        
        # ==================== CAMPO DE DIGITAÇÃO ====================
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
        self.caixa_digitacao.pack(pady=15, ipady=12)
        self.caixa_digitacao.bind("<KeyRelease>", self.verificar_digitacao_tempo_real)
        self.caixa_digitacao.bind("<Return>", self.finalizar_digitacao)
        
        # ==================== INDICADOR DE COMBO ====================
        self.label_combo = tk.Label(
            self.frame_centro,
            text="",
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_COMBO_1
        )
        self.label_combo.pack(pady=10)
        
        # ==================== BOTÃO INICIAR ====================
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
        
        # Hover effect
        self.btn_pronto.bind("<Enter>", lambda e: self.btn_pronto.config(bg=config.COR_SUCESSO_CLARO))
        self.btn_pronto.bind("<Leave>", lambda e: self.btn_pronto.config(bg=config.COR_SUCESSO))
        
        # ==================== FRAMES DE RESULTADO ====================
        self.frame_resultado = tk.Frame(self.frame_centro, bg=config.COR_FRAME)
        self.frame_resultado.pack(pady=10, fill="x")
        
        self.frame_botoes_finais = tk.Frame(self.frame_centro, bg=config.COR_FRAME)
        self.frame_botoes_finais.pack(pady=10)
    
    # ==================== RANKING ====================
    def atualizar_ranking_lateral(self):
        """Atualiza o ranking lateral com apenas o modo atual"""
        for item in self.tree_lateral.get_children():
            self.tree_lateral.delete(item)
        
        # Carrega todos os rankings
        ranking_completo = ranked.carregar_ranking()
        
        # Filtra apenas o modo atual
        ranking_modo = [r for r in ranking_completo if len(r) > 4 and r[4] == self.modo_jogo]
        
        # Ordena por pontos (índice 1)
        ranking_modo.sort(key=lambda x: x[1], reverse=True)
        
        # Pega os top 10
        top = ranking_modo[:config.RANKING_TOP_EXIBIR]
        
        for idx, entrada in enumerate(top, 1):
            nome = entrada[0] if len(entrada) > 0 else "Jogador"
            pontos = entrada[1] if len(entrada) > 1 else 0
            
            # Formata a posição com emoji
            if idx == 1:
                pos_text = "🥇"
            elif idx == 2:
                pos_text = "🥈"
            elif idx == 3:
                pos_text = "🥉"
            else:
                pos_text = f"{idx}º"
            
            # Insere no ranking
            self.tree_lateral.insert(
                "", 
                "end", 
                values=(pos_text, nome, f"{int(pontos)}")
            )
        
        # Se não tiver nenhum registro
        if len(top) == 0:
            self.tree_lateral.insert(
                "",
                "end",
                values=("", "Nenhum registro", "0")
            )
    
    # ==================== CONTROLE DO JOGO ====================
    def definir_texto(self, texto):
        self.texto = texto
        self.label_texto.config(text="Clique em INICIAR para começar")
        self.caixa_digitacao.delete(0, tk.END)
        self.tempo_restante = config.TEMPO_POR_MODO.get(self.modo_jogo, config.TEMPO)
        self.label_tempo.config(text=f"⏱️ {self.tempo_restante}s")
        self.btn_pronto.config(state="normal")
        self.combo_atual = 0
        self.combo_maximo = 0
        self.caracteres_digitados = 0
        
        # Limpa frames
        for w in self.frame_resultado.winfo_children():
            w.destroy()
        for w in self.frame_botoes_finais.winfo_children():
            w.destroy()
        
        # Atualiza barra de progresso
        self.atualizar_barra_progresso(0)
    
    def iniciar(self):
        self.caixa_digitacao.configure(state="disabled")
    
    def comecar(self):
        self.btn_pronto.config(state="disabled")
        self.btn_pronto.pack_forget()
        
        self.label_texto.config(text=self.texto)
        self.caixa_digitacao.configure(state="normal")
        self.caixa_digitacao.delete(0, tk.END)
        self.caixa_digitacao.focus_set()
        
        self.tempo_inicio = time.time()
        self.tempo_restante = config.TEMPO_POR_MODO.get(self.modo_jogo, config.TEMPO)
        self.atualizar_cronometro()
    
    def atualizar_cronometro(self):
        # Cor do tempo baseada no restante
        if self.tempo_restante <= 10:
            cor_tempo = config.COR_ERRO
        elif self.tempo_restante <= 20:
            cor_tempo = config.COR_AVISO
        else:
            cor_tempo = config.COR_INFO
        
        self.label_tempo.config(
            text=f"⏱️ {self.tempo_restante}s",
            fg=cor_tempo
        )
        
        if self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.timer_id = self.root.after(1000, self.atualizar_cronometro)
        else:
            self.caixa_digitacao.configure(state="disabled")
            self.finalizar_digitacao()
    
    # ==================== FEEDBACK TEMPO REAL ====================
    def verificar_digitacao_tempo_real(self, event=None):
        """Atualiza WPM, progresso e combo em tempo real"""
        if not self.tempo_inicio:
            return
        
        digitado = self.caixa_digitacao.get()
        self.caracteres_digitados = len(digitado)
        
        # Calcula WPM em tempo real
        tempo_decorrido = time.time() - self.tempo_inicio
        if tempo_decorrido > 0:
            self.wpm_atual = (len(digitado) / 5) / (tempo_decorrido / 60.0)
            self.label_wpm.config(text=f"⚡ {int(self.wpm_atual)} WPM")
        
        # Atualiza barra de progresso
        progresso = min(len(digitado) / len(self.texto), 1.0) if len(self.texto) > 0 else 0
        self.atualizar_barra_progresso(progresso)
        
        # Verifica combo (caracteres corretos consecutivos)
        corretos_consecutivos = 0
        for i, char in enumerate(digitado):
            if i < len(self.texto) and char == self.texto[i]:
                corretos_consecutivos += 1
            else:
                corretos_consecutivos = 0
        
        self.combo_atual = corretos_consecutivos
        if self.combo_atual > self.combo_maximo:
            self.combo_maximo = self.combo_atual
        
        # Mostra combo
        self.atualizar_label_combo()
        
        # Em modo morte súbita, verifica erro
        if self.modo_jogo == "morte_subita":
            for i, char in enumerate(digitado):
                if i < len(self.texto) and char != self.texto[i]:
                    # Erro detectado! Finaliza imediatamente
                    self.caixa_digitacao.configure(state="disabled")
                    self.root.after(300, self.finalizar_digitacao)
                    break
    
    def atualizar_label_combo(self):
        """Atualiza o label de combo com cor baseada no nível"""
        if self.combo_atual < 10:
            self.label_combo.config(text="")
            return
        
        # Encontra o nível do combo
        cor = config.COR_COMBO_1
        texto = f"🔥 Combo: {self.combo_atual}"
        
        for nivel, mensagem, cor_nivel in reversed(config.NIVEIS_COMBO):
            if self.combo_atual >= nivel:
                cor = cor_nivel
                texto = f"🔥 {mensagem} Combo: {self.combo_atual}!"
                break
        
        self.label_combo.config(text=texto, fg=cor)
    
    def atualizar_barra_progresso(self, progresso):
        """Atualiza a barra de progresso visual"""
        self.canvas_progresso.delete("all")
        
        largura = self.canvas_progresso.winfo_width()
        if largura <= 1:
            largura = 800  # Valor padrão
        
        altura = 12
        
        # Fundo
        self.canvas_progresso.create_rectangle(
            0, 0, largura, altura,
            fill=config.COR_PROGRESSO_BG,
            outline=""
        )
        
        # Barra de progresso
        largura_progresso = int(largura * progresso)
        if largura_progresso > 0:
            # Gradiente de cor baseado no progresso
            if progresso < 0.5:
                cor = config.COR_INFO
            elif progresso < 0.8:
                cor = config.COR_AVISO
            else:
                cor = config.COR_SUCESSO
            
            self.canvas_progresso.create_rectangle(
                0, 0, largura_progresso, altura,
                fill=cor,
                outline=""
            )
    
    # ==================== COMPARAÇÃO E PONTUAÇÃO ====================
    def comparar_textos(self, original: str, digitado: str):
        """Compara caractere a caractere e retorna estatísticas"""
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
                
                # Morte súbita: para no primeiro erro
                if self.modo_jogo == "morte_subita" and errados > 0:
                    for j in range(i + 1, tamanho):
                        c_orig2 = original[j] if j < len(original) else ""
                        c_dig2 = ""
                        if c_orig2 != "":
                            errados += 1
                        lista_flags.append((c_orig2, c_dig2, False))
                    break
        
        total = corretos + errados
        return corretos, errados, total, lista_flags, combo_max
    
    def calcular_pontos(self, caracteres_corretos, caracteres_errados, tempo_segundos, combo_max):
        """Calcula pontos com sistema de bônus"""
        pesos = config.PESOS_PONTOS.get(self.modo_jogo, config.PESOS_PONTOS["normal"])
        
        base = caracteres_corretos * pesos["ponto_por_correto"]
        penalidade_erros = caracteres_errados * pesos["penalidade_por_erro"]
        penalidade_tempo = int(tempo_segundos / 5) * pesos["penalidade_tempo_5s"]
        
        pontos = base - penalidade_erros - penalidade_tempo
        
        # Bônus de combo
        bonus_combo = 0
        if combo_max >= 50:
            bonus_combo = pesos.get("bonus_combo_50", 0)
        elif combo_max >= 25:
            bonus_combo = pesos.get("bonus_combo_25", 0)
        elif combo_max >= 10:
            bonus_combo = pesos.get("bonus_combo_10", 0)
        
        pontos += bonus_combo
        
        # Bônus perfeito
        if caracteres_errados == 0 and caracteres_corretos > 0:
            pontos += pesos.get("bonus_perfeito", 0)
        
        # Morte súbita: erro zera
        if self.modo_jogo == "morte_subita" and caracteres_errados > 0:
            pontos = 0
        
        return max(pontos, 0), bonus_combo
    
    def esconder_cabecalho(self):
        """Esconde elementos do cabeçalho após finalização"""
        self.label_tempo.pack_forget()
        self.label_texto.pack_forget()
        self.caixa_digitacao.delete(0, tk.END)
        self.caixa_digitacao.pack_forget()
        self.label_combo.pack_forget()
        self.label_wpm.pack_forget()
        self.canvas_progresso.pack_forget()
    
    def finalizar_digitacao(self, event=None):
        """Finaliza a rodada e mostra resultados"""
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        digitado = self.caixa_digitacao.get().strip()
        self.caixa_digitacao.configure(state="disabled")
        
        if not self.tempo_inicio:
            self.mostrar_mensagem("⚠️ Clique em 'INICIAR' para começar.", erro=True)
            return
        
        tempo_total = time.time() - self.tempo_inicio
        original = self.texto.strip()
        
        corretos, errados, total, lista_flags, combo_max = self.comparar_textos(original, digitado)
        
        if total == 0:
            self.mostrar_mensagem("❌ Você não digitou nada.", erro=True)
            self.esconder_cabecalho()
            self.mostrar_botoes_finais()
            return
        
        pontos, bonus_combo = self.calcular_pontos(corretos, errados, tempo_total, combo_max)
        precisao = (corretos / total) * 100 if total > 0 else 0.0
        
        # WPM
        if tempo_total > 0:
            wpm = (corretos / 5) / (tempo_total / 60.0)
        else:
            wpm = 0.0
        
        # Esconde elementos de jogo
        self.esconder_cabecalho()
        
        # Define status por modo
        if self.modo_jogo == "morte_subita":
            if errados == 0:
                status = "💎 PERFEITO - Morte Súbita Completa!"
                status_cor = config.COR_SUCESSO
            else:
                status = "💀 FALHOU - Erro no Modo Morte Súbita"
                status_cor = config.COR_ERRO
        elif self.modo_jogo == "hardcore":
            if errados == 0:
                status = "🔥 HARDCORE DOMINADO - SEM ERROS!"
                status_cor = config.COR_SUCESSO
            else:
                status = "🔥 Modo Hardcore Concluído"
                status_cor = config.COR_AVISO
        else:
            if errados == 0:
                status = "✨ PERFEITO - Sem Erros!"
                status_cor = config.COR_SUCESSO
            elif precisao >= 90:
                status = "🎯 EXCELENTE Resultado!"
                status_cor = config.COR_SUCESSO
            elif precisao >= 70:
                status = "👍 BOM Trabalho!"
                status_cor = config.COR_INFO
            else:
                status = "📚 Continue Praticando!"
                status_cor = config.COR_AVISO
        
        self.mostrar_resultado(
            tempo_total, corretos, errados, precisao, pontos,
            original, digitado, lista_flags, combo_max, wpm,
            status, status_cor, bonus_combo
        )
        
        # Salva pontuação e atualiza stats
        if pontos > 0:
            self.salvar_no_ranking(pontos, wpm, precisao)
            if self.usuario:
                login.atualizar_stats_usuario(self.usuario, wpm, precisao)
                self.verificar_conquistas(wpm, precisao, errados, combo_max)
        
        self.mostrar_botoes_finais()
    
    # ==================== CONQUISTAS ====================
    def verificar_conquistas(self, wpm, precisao, errados, combo_max):
        """Verifica e adiciona conquistas desbloqueadas"""
        if not self.usuario:
            return
        
        stats = login.obter_stats_usuario(self.usuario)
        if not stats:
            return
        
        conquistas_atuais = stats.get("conquistas", [])
        novas_conquistas = []
        
        # Primeira vitória
        if "primeira_vitoria" not in conquistas_atuais and stats["total_partidas"] >= 1:
            login.adicionar_conquista(self.usuario, "primeira_vitoria")
            novas_conquistas.append("primeira_vitoria")
        
        # Velocista
        if "velocista" not in conquistas_atuais and wpm >= 60:
            login.adicionar_conquista(self.usuario, "velocista")
            novas_conquistas.append("velocista")
        
        # Mestre
        if "mestre" not in conquistas_atuais and wpm >= 80:
            login.adicionar_conquista(self.usuario, "mestre")
            novas_conquistas.append("mestre")
        
        # Perfeito
        if "perfeito" not in conquistas_atuais and errados == 0:
            login.adicionar_conquista(self.usuario, "perfeito")
            novas_conquistas.append("perfeito")
        
        # Combo Master
        if "combo_master" not in conquistas_atuais and combo_max >= 50:
            login.adicionar_conquista(self.usuario, "combo_master")
            novas_conquistas.append("combo_master")
        
        # Resistência
        if "resistencia" not in conquistas_atuais and stats["total_partidas"] >= 10:
            login.adicionar_conquista(self.usuario, "resistencia")
            novas_conquistas.append("resistencia")
        
        # Mostra conquistas desbloqueadas
        if novas_conquistas:
            self.mostrar_conquistas_desbloqueadas(novas_conquistas)
    
    def mostrar_conquistas_desbloqueadas(self, conquistas_ids):
        """Mostra popup de conquistas desbloqueadas"""
        for conquista_id in conquistas_ids:
            conquista_info = config.CONQUISTAS.get(conquista_id, {})
            
            # Cria label animado
            label_conquista = tk.Label(
                self.frame_centro,
                text=f"{conquista_info.get('icone', '🏆')} {conquista_info.get('nome', 'Conquista')}",
                font=config.FONTE_SUBTITULO,
                bg=config.COR_OURO,
                fg=config.COR_TEXTO,
                padx=20,
                pady=10
            )
            label_conquista.place(relx=0.5, rely=0.1, anchor="center")
            
            # Remove após 3 segundos
            self.root.after(3000, label_conquista.destroy)
    
    # ==================== UI DE RESULTADO ====================
    def mostrar_mensagem(self, texto, erro=False):
        for w in self.frame_resultado.winfo_children():
            w.destroy()
        
        cor = config.COR_ERRO if erro else config.COR_TEXTO
        
        tk.Label(
            self.frame_resultado,
            text=texto,
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=cor,
            justify="center"
        ).pack()
    
    def mostrar_resultado(self, tempo_total, corretos, errados, precisao, pontos,
                         original, digitado, lista_flags, combo_max, wpm,
                         status, status_cor, bonus_combo):
        
        for w in self.frame_resultado.winfo_children():
            w.destroy()
        
        # Status grande
        tk.Label(
            self.frame_resultado,
            text=status,
            font=("Segoe UI", 32, "bold"),
            bg=config.COR_FRAME,
            fg=status_cor,
            pady=15
        ).pack()
        
        # Grid de estatísticas
        stats_frame = tk.Frame(self.frame_resultado, bg=config.COR_CARD_DESTAQUE, padx=30, pady=20)
        stats_frame.pack(pady=15, fill="x")
        
        # Linha 1
        row1 = tk.Frame(stats_frame, bg=config.COR_CARD_DESTAQUE)
        row1.pack(fill="x", pady=5)
        
        self.criar_stat_box(row1, "⏱️ Tempo", f"{tempo_total:.2f}s").pack(side="left", expand=True, padx=5)
        self.criar_stat_box(row1, "✅ Corretos", str(corretos)).pack(side="left", expand=True, padx=5)
        self.criar_stat_box(row1, "❌ Erros", str(errados)).pack(side="left", expand=True, padx=5)
        
        # Linha 2
        row2 = tk.Frame(stats_frame, bg=config.COR_CARD_DESTAQUE)
        row2.pack(fill="x", pady=5)
        
        self.criar_stat_box(row2, "🎯 Precisão", f"{precisao:.1f}%").pack(side="left", expand=True, padx=5)
        self.criar_stat_box(row2, "⚡ WPM", f"{wpm:.1f}").pack(side="left", expand=True, padx=5)
        self.criar_stat_box(row2, "🔥 Combo Máx", str(combo_max)).pack(side="left", expand=True, padx=5)
        
        # Pontuação final
        pontos_frame = tk.Frame(self.frame_resultado, bg=config.COR_SUCESSO, padx=20, pady=15)
        pontos_frame.pack(pady=10, fill="x")
        
        tk.Label(
            pontos_frame,
            text=f"🏆 PONTUAÇÃO: {pontos}",
            font=("Segoe UI", 28, "bold"),
            bg=config.COR_SUCESSO,
            fg=config.COR_BOTAO_TEXTO
        ).pack()
        
        if bonus_combo > 0:
            tk.Label(
                pontos_frame,
                text=f"(+{bonus_combo} bônus de combo)",
                font=config.FONTE_STATS,
                bg=config.COR_SUCESSO,
                fg=config.COR_BOTAO_TEXTO
            ).pack()
        
        # Mensagem motivacional
        mensagem_wpm = self.obter_mensagem_wpm(wpm)
        mensagem_precisao = self.obter_mensagem_precisao(precisao)
        
        tk.Label(
            self.frame_resultado,
            text=f"{mensagem_wpm} | {mensagem_precisao}",
            font=config.FONTE_TEXTO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack(pady=10)
    
    def criar_stat_box(self, parent, titulo, valor):
        """Cria uma caixa de estatística"""
        frame = tk.Frame(parent, bg=config.COR_FRAME, padx=15, pady=10)
        
        tk.Label(
            frame,
            text=titulo,
            font=config.FONTE_MINI,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_SECUNDARIO
        ).pack()
        
        tk.Label(
            frame,
            text=valor,
            font=config.FONTE_SUBTITULO,
            bg=config.COR_FRAME,
            fg=config.COR_TEXTO_DESTAQUE
        ).pack()
        
        return frame
    
    def obter_mensagem_wpm(self, wpm):
        """Retorna mensagem baseada no WPM"""
        for (min_wpm, max_wpm), mensagem in config.MENSAGENS_WPM.items():
            if min_wpm <= wpm < max_wpm:
                return mensagem
        return "Continue praticando!"
    
    def obter_mensagem_precisao(self, precisao):
        """Retorna mensagem baseada na precisão"""
        for (min_prec, max_prec), mensagem in config.MENSAGENS_PRECISAO.items():
            if min_prec <= precisao <= max_prec:
                return mensagem
        return "Foque na precisão!"
    
    # ==================== RANKING E BOTÕES FINAIS ====================
    def salvar_no_ranking(self, pontos, wpm, precisao):
        nome = self.usuario or "Jogador"
        ranked.salvar_pontos(nome, pontos, wpm, precisao, self.modo_jogo)
        self.atualizar_ranking_lateral()
    
    def mostrar_botoes_finais(self):
        for widget in self.frame_botoes_finais.winfo_children():
            widget.destroy()
        
        btn_frame = tk.Frame(self.frame_botoes_finais, bg=config.COR_FRAME)
        btn_frame.pack()
        
        # Botão Repetir
        btn_repetir = tk.Button(
            btn_frame,
            text="🔄 Jogar Novamente",
            font=config.FONTE_TEXTO_GRANDE,
            bg=config.COR_BOTAO,
            fg=config.COR_BOTAO_TEXTO,
            activebackground=config.COR_BOTAO_HOVER,
            activeforeground=config.COR_BOTAO_TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.on_fim,
            width=18,
            height=2
        )
        btn_repetir.pack(side="left", padx=10, pady=5)
        btn_repetir.bind("<Enter>", lambda e: btn_repetir.config(bg=config.COR_BOTAO_HOVER))
        btn_repetir.bind("<Leave>", lambda e: btn_repetir.config(bg=config.COR_BOTAO))
        
        # Botão Voltar
        btn_voltar = tk.Button(
            btn_frame,
            text="🏠 Menu Principal",
            font=config.FONTE_TEXTO,
            bg=config.COR_BOTAO_SECUNDARIO,
            fg=config.COR_TEXTO,
            activebackground=config.COR_BOTAO_SECUNDARIO_HOVER,
            activeforeground=config.COR_TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.on_voltar_menu,
            width=18,
            height=2
        )
        btn_voltar.pack(side="left", padx=10, pady=5)
        btn_voltar.bind("<Enter>", lambda e: btn_voltar.config(bg=config.COR_BOTAO_SECUNDARIO_HOVER))
        btn_voltar.bind("<Leave>", lambda e: btn_voltar.config(bg=config.COR_BOTAO_SECUNDARIO))
