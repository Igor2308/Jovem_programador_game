import pygame
import random
from settings import WIDTH, HEIGHT, FPS, PLAYER_SIZE, PLAYER_SPEED
from src.player import Player
from src.slime import Slime
from src.pao import Pao
from src.ui.hud import HUD
from src.ui.tela_pause import TelaPause
from src.ui.tela_game_over import TelaGameOver

def posicao_aleatoria():
    x = random.randint(0, WIDTH - 45)
    y = random.randint(0, HEIGHT - 45)
    return x, y

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teste")
clock = pygame.time.Clock()
running = True
hud = HUD()
tela_pause = TelaPause()
tela_game_over = TelaGameOver()

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

#pao
drops = pygame.sprite.Group()

for _ in range(2):
    x, y = posicao_aleatoria()
    novo_slime = Slime(x, y)
    slimes.add(novo_slime)

ESTADO_JOGANDO = "jogando"
ESTADO_PAUSADO = "pausado"
ESTADO_GAME_OVER = "game_over"

estado = ESTADO_JOGANDO

while running:
    delta = clock.tick(FPS) / 1000.0
    velocidade = PLAYER_SPEED * delta 

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if estado == ESTADO_JOGANDO:
                    estado = ESTADO_PAUSADO
                elif estado == ESTADO_PAUSADO:
                    estado = ESTADO_JOGANDO
            if estado == ESTADO_GAME_OVER and evento.key == pygame.K_r:
                player.vida = 100
                player.hitbox.center = (WIDTH / 2, HEIGHT / 2)
                player.rect.center = player.hitbox.center
                player.morto = False

                for slime in slimes:
                    slime.rect.topleft = posicao_aleatoria()

                estado = ESTADO_JOGANDO
                # Verifica game over

    if player.vida <= 0 and estado != ESTADO_GAME_OVER:
        player.morto = True
        estado = ESTADO_GAME_OVER

    # Atualiza jogo apenas se não estiver game over
    # SEMPRE desenha o fundo primeiro
    screen.blit(background, (0, 0))

    if estado == ESTADO_JOGANDO:
        player.update(velocidade, slimes)
        slimes.update(player)
        drops.update()  

        # CONTADOR
        for slime in slimes:
            if slime.morto and not hasattr(slime, "contado"):
                slimes_abatidos += 1
                slime.contado = True

        # SPAWN 
        for slime in list(slimes):
            if slime.morto:
                if random.random() <= 0.5:
                    offset_x = random.randint(-30, 30)
                    offset_y = random.randint(-20, 0)
                    drop = Pao(slime.rect.centerx + offset_x, slime.rect.centery + offset_y)
                    drops.add(drop)

                x, y = posicao_aleatoria()
                novo_slime = Slime(x, y)
                slimes.add(novo_slime)
                slimes.remove(slime)

        coletado = []

        for drop in drops:
            if player.hitbox.colliderect(drop.rect):
                coletado.append(drop)
                drop.kill()

        for item in coletado:
            player.vida += 50
            if player.vida > 100:
                player.vida = 100

        # contador e spawn continuam iguais...
    elif estado == ESTADO_GAME_OVER:
        pass

    # Desenha sprites
    slimes.draw(screen)
    players.draw(screen)
    drops.draw(screen)

    # HUD sempre fica por cima de tudo
    hud.draw(screen, player, slimes_abatidos)

    if estado == ESTADO_PAUSADO:
        tela_pause.draw(screen)

    if estado == ESTADO_GAME_OVER:
        tela_game_over.draw(screen)

    pygame.display.flip()

pygame.quit()