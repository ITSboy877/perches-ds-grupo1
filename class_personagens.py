import pygame as pg
import os
from enum import Enum


class personagemEstado(Enum):
    PARADO = 1
    ANDANDO = 2
    PULANDO = 3
    batendo = 4
    especial = 5

class Personagem:
    def __init__(self, x, y, tipo_personagem):
        self.x = x
        self.y = y
        self.estado = personagemEstado.PARADO
        self.tipo_personagem = tipo_personagem
    
        if tipo_personagem == "Guilherme Ribeiro":
            caminho_imagem = os.path.join("Desenhos 2D", "gui_ribeiro.png")
        elif tipo_personagem == "Pedro Souza":
            caminho_imagem = os.path.join("Desenhos 2D", "pedro.png")
        elif tipo_personagem == "Guilherme Dias":
            caminho_imagem = os.path.join("Desenhos 2D", "dias.png")
        elif tipo_personagem == "Diego lombardi":
            caminho_imagem = os.path.join("Desenhos 2D", "diego.png")

        self.imagem = pg.image.load(caminho_imagem).convert_alpha()

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))
        
