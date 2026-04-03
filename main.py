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

# fundo de morte FIXO
fundo_morte = pygame.image.load("imagens/TELA_GAMEOVER.png").convert()
fundo_morte = pygame.transform.scale(fundo_morte, (WIDTH, HEIGHT))  # ajuste ao tamanho da tela

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
tempo_morte_iniciada = 0
DELAY_GAME_OVER = 1000  # 2 segundos

tela_morte_selecionada = None
animacao_morte_concluida = False

while running:
    delta = clock.tick(FPS) / 1000.0
    velocidade = PLAYER_SPEED * delta 

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                running = False
            # Reiniciar depois da animação
            if game_over and animacao_morte_concluida and evento.key == pygame.K_r:
                player.vida = 100
                player.hitbox.center = (WIDTH / 2, HEIGHT / 2)
                player.rect.center = player.hitbox.center
                player.morto = False
                for slime in slimes:
                    slime.rect.topleft = posicao_aleatoria()
                game_over = False
                animacao_morte_concluida = False

      # Verifica game over
    if player.vida <= 0 and not game_over:
        player.morto = True
        tempo_morte_iniciada = pygame.time.get_ticks()
        game_over = True


    # Atualiza jogo apenas se não estiver game over
    # SEMPRE desenha o fundo primeiro
    screen.blit(background, (0, 0))

    if not game_over:
        player.update(velocidade, slimes)
        slimes.update(player)

        # 🔥 CONTADOR
        for slime in slimes:
            if slime.morto and not hasattr(slime, "contado"):
                slimes_abatidos += 1
                slime.contado = True

        # 🔥 SPAWN (IMPORTANTE FICAR AQUI)
        for slime in list(slimes):
            if slime.morto:
                x, y = posicao_aleatoria()
                novo_slime = Slime(x, y)
                slimes.add(novo_slime)
                slimes.remove(slime)

        # contador e spawn continuam iguais...
    else:
        # animação de morte continua rodando
        status = player.update(velocidade, slimes)
        if status == "fim_animacao_morte":
            animacao_morte_concluida = True

         

    # Desenha sprites
    slimes.draw(screen)
    players.draw(screen)

    # HUD
    texto_slimes = fonte.render(f"Slimes abatidos: {slimes_abatidos}", True, (255, 255, 0))
    screen.blit(texto_slimes, (WIDTH - texto_slimes.get_width() - 10, 10))
    texto_vida = fonte.render(f"Vida: {player.vida}", True, (255, 255, 255))
    screen.blit(texto_vida, (10, 10))

    # Mensagens de game over
    if game_over:

        tempo_atual = pygame.time.get_ticks()

        # DEBUG (opcional, pode apagar depois)
        # print(tempo_atual - tempo_morte_iniciada)

        if tempo_atual - tempo_morte_iniciada >= DELAY_GAME_OVER:
            # DESENHA POR CIMA DE TUDO
            screen.blit(fundo_morte, (0, 0))
        
    pygame.display.flip()

pygame.quit()