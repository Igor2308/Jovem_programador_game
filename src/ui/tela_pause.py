import pygame
from settings import WIDTH, HEIGHT

class TelaPause:
    def __init__(self):
        self.fonte_titulo = pygame.font.SysFont(None, 80)
        self.fonte_opcoes = pygame.font.SysFont(None, 40)

    def draw(self, screen):
        # overlay escuro
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # textos
        titulo = self.fonte_titulo.render("PAUSADO", True, (255, 255, 255))
        opcao1 = self.fonte_opcoes.render("ESC - Continuar", True, (200, 200, 200))

        # posições
        screen.blit(titulo, titulo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        screen.blit(opcao1, opcao1.get_rect(center=(WIDTH // 2, HEIGHT // 2)))