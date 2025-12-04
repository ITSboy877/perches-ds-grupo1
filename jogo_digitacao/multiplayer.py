class SessaoMultiplayer:
    def __init__(self, num_jogadores, modo_jogo, tipo_teclado, texto):
        self.num_jogadores = num_jogadores
        self.modo_jogo = modo_jogo
        self.tipo_teclado = tipo_teclado
        self.texto = texto
        self.resultados = []
        self.jogador_atual = 1
    
    def adicionar_resultado(self, nome_jogador, pontos, wpm, precisao, tempo):
        self.resultados.append({
            "jogador": nome_jogador,
            "numero": self.jogador_atual,
            "pontos": pontos,
            "wpm": wpm,
            "precisao": precisao,
            "tempo": tempo
        })
        self.jogador_atual += 1
    
    def sessao_completa(self):
        return len(self.resultados) >= self.num_jogadores
    
    def obter_vencedor(self):
        if not self.resultados:
            return None
        return max(self.resultados, key=lambda x: x["pontos"])
    
    def obter_ranking(self):
        return sorted(self.resultados, key=lambda x: x["pontos"], reverse=True)
