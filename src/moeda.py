import pygame

class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        imagem_original = pygame.image.load("imagens/moeda.png").convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (25, 25))
        self.rect = self.image.get_rect(center=(x, y))