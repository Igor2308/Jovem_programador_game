import pygame
from settings import WIDTH

class HUD:
    def __init__(self):
        self.fonte = pygame.font.SysFont(None, 45)

    def draw(self, screen, player, slimes_abatidos):
        # TEXTO SLIMES
        texto_slimes = self.fonte.render(
            f"Slimes abatidos: {slimes_abatidos}", True, (255, 255, 0)
        )
        screen.blit(texto_slimes, (WIDTH - texto_slimes.get_width() - 10, 10))

        # TEXTO VIDA
        texto_vida = self.fonte.render(
            f"Vida: {player.vida}", True, (255, 255, 255)
        )
        screen.blit(texto_vida, (10, 10))