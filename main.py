import pygame
import random
from settings import WIDTH, HEIGHT, FPS, PLAYER_SIZE, PLAYER_SPEED
from src.player import Player
from src.slime import Slime

def posicao_aleatoria():
    x = random.randint(0, WIDTH - 45)
    y = random.randint(0, HEIGHT - 45)
    return x, y

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teste")
clock = pygame.time.Clock()
running = True

# fundo
background = pygame.image.load("imagens/fundo.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

slimes_abatidos = 0

# player
player = Player("P1")

# grupo de jogadores
players = pygame.sprite.Group()
players.add(player)

# slimes
slimes = pygame.sprite.Group()

for _ in range(2):
    x, y = posicao_aleatoria()
    novo_slime = Slime(x, y)
    slimes.add(novo_slime)

# fonte
fonte = pygame.font.SysFont(None, 45)
game_over = False

while running:
    delta = clock.tick(FPS) / 1000.0
    velocidade = delta * PLAYER_SPEED

    # eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                running = False
            if game_over and evento.key == pygame.K_r:
                player.vida = 100
                player.hitbox.center = (WIDTH / 2, HEIGHT / 2)
                player.rect.center = player.hitbox.center
                for slime in slimes:
                    slime.rect.topleft = (300, 300)
                game_over = False

    # fundo
    screen.blit(background, (0, 0))

    if not game_over:
    # Atualiza player e slimes
        player.update(velocidade, slimes)
        slimes.update(player)

        # -------------------------
        # Contador de Slimes abatidos
        for slime in slimes:
            if slime.morto and not hasattr(slime, "contado"):
                slimes_abatidos += 1
                slime.contado = True

        # -------------------------
        # Spawn de novos Slimes ao morrer
        for slime in list(slimes):  # list() evita conflito ao remover
            if slime.morto:
                x, y = posicao_aleatoria()
                novo_slime = Slime(x, y)
                slimes.add(novo_slime)
                slimes.remove(slime)

    # Ordem de desenho: slimes atrás do player
   # Ordem de desenho: Slimes atrás do Player
    slimes.draw(screen)
    players.draw(screen)

    # HUD do contador
    texto_slimes = fonte.render(f"Slimes abatidos: {slimes_abatidos}", True, (255, 255, 0))
    screen.blit(texto_slimes, (WIDTH - texto_slimes.get_width() - 10, 10))

    # HUD vida
    texto_vida = fonte.render(f"Vida: {player.vida}", True, (255, 255, 255))
    screen.blit(texto_vida, (10, 10))

    # verifica game over
    if player.vida <= 0:
        game_over = True

    # tela game over
    if game_over:
        texto1 = fonte.render("GAME OVER", True, (255, 0, 0))
        texto2 = fonte.render("Pressione R para reiniciar", True, (255, 255, 255))
        texto3 = fonte.render("ESC para sair", True, (255, 255, 255))

        screen.blit(texto1, (WIDTH // 2 - 100, HEIGHT // 2 - 40))
        screen.blit(texto2, (WIDTH // 2 - 150, HEIGHT // 2))
        screen.blit(texto3, (WIDTH // 2 - 100, HEIGHT // 2 + 40))

    pygame.display.flip()

pygame.quit()