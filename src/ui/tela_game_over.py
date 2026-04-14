import pygame
from settings import WIDTH, HEIGHT

class TelaGameOver:
    def __init__(self):
        self.fundo = pygame.image.load("imagens/TELA_GAMEOVER.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (WIDTH, HEIGHT))

    def draw(self, screen):
        screen.blit(self.fundo, (0, 0))