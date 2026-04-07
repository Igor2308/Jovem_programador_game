import pygame
import math

class Pao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("imagens/PAO.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-10, -10)
        self.rect.center = (x, y)       
        self.vel_y = -3  # força pra cima (pulo)
        self.gravidade = 0.15
        self.base_y = y  # posição base
        self.chao = y  # altura onde ele deve parar
        self.rect.center = (x, y)

        self.tempo = 0  # controla animação

    def update(self):
        # física do pulo
        self.vel_y += self.gravidade
        self.base_y += self.vel_y

         # faz o pão trava no "chão"
        if self.base_y >= self.chao:
            self.base_y = self.chao
            self.vel_y = 0

        # flutuação suave
        self.tempo += 0.1
        deslocamento = math.sin(self.tempo) * 5

        self.rect.centery = self.base_y + deslocamento