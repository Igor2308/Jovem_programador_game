import pygame
from settings import WIDTH

class HUD:
    def __init__(self):
        self.fonte = pygame.font.SysFont(None, 45)

    def draw(self, screen, player, slimes_abatidos):
        # BARRA DE VIDA 

        largura = 230
        altura = 30

        x = screen.get_width() - largura - 20
        y = 20  # um pouco abaixo do texto

        vida_ratio = player.vida / 100

        if vida_ratio > 0.6:
            cor = (0, 255, 0)
        elif vida_ratio > 0.3:
            cor = (255, 255, 0)
        else:
            cor = (255, 0, 0)

        # fundo
        pygame.draw.rect(screen, (50, 50, 50), (x, y, largura, altura))

        # vida atual
        pygame.draw.rect(screen, cor, (x, y, largura * vida_ratio, altura))

        # borda
        pygame.draw.rect(screen, (255, 255, 255), (x, y, largura, altura), 2)

        # DINHEIRO
        texto_dinheiro = self.fonte.render(
            f"R$ {player.score}", True, (255, 215, 0)
        )

        screen.blit(texto_dinheiro, (20, 20))