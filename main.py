import pygame
import random
import pytmx
import pytmx.util_pygame
from settings import WIDTH, HEIGHT, FPS, PLAYER_SPEED
from src.player import Player
from src.slime import Slime
from src.pao import Pao
from src.ui.hud import HUD
from src.ui.tela_pause import TelaPause
from src.ui.tela_game_over import TelaGameOver
from src.moeda import Moeda
from src.ui.tela_menu import TelaMenu

def posicao_aleatoria(colisoes):
    while True:
        x = random.randint(0, map_width - 45)
        y = random.randint(0, map_height - 45)

        area_spawn = pygame.Rect(x, y, 45, 45)

        colidiu = False

        for colisao in colisoes:
            if area_spawn.colliderect(colisao):
                colidiu = True
                break

        if not colidiu:
            return x, y
        
        if area_spawn.colliderect(player.hitbox.inflate(300, 300)):
            colidiu = True
        
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teste")
clock = pygame.time.Clock()
running = True
hud = HUD()
tela_pause = TelaPause()
tela_game_over = TelaGameOver()
tela_menu = TelaMenu()

slimes_abatidos = 0
tempo_morte = 0

#cria um grupo
slimes = pygame.sprite.Group()
drops = pygame.sprite.Group()
moedas = pygame.sprite.Group()

ESTADO_MENU = "menu"
ESTADO_VILA = "vila"
ESTADO_JOGANDO = "jogando"
ESTADO_PAUSADO = "pausado"
ESTADO_GAME_OVER = "game_over"

MAPA_VILA = "vila"
MAPA_FLORESTA = "floresta"
mapa_atual = MAPA_VILA # Começa na vila

tmx_data = pytmx.util_pygame.load_pygame("mapas/Mapa_principal.tmx")

mapa_background = pygame.image.load("mapas/mapa_inicial.png").convert()
mapa_overlay = None

colisoes_vila = []
for obj in tmx_data.get_layer_by_name("COLISÕES"):
    colisoes_vila.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


altar_rect = pygame.Rect(1200, 1415, 130, 130) # Ajuste a posição X, Y aqui
fonte_msg = pygame.font.SysFont("Arial", 24, bold=True)

player = Player("P1")
player.colisoes = colisoes_vila

player.hitbox.topleft = (800, 800)
player.rect.center = player.hitbox.center

players = pygame.sprite.Group()
players.add(player)

estado = ESTADO_MENU

while running:
    delta = clock.tick(FPS) / 1000.0
    velocidade = PLAYER_SPEED * delta 

    if estado == ESTADO_VILA: #se estiver no mapa da vila não spawna slimes
        slimes.empty()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if estado == ESTADO_MENU:

            acao = tela_menu.verificar_clique(evento)# verifica se o player clicou no botão 

            if acao == "iniciar":
                tela_menu.fechar_video()
                estado = ESTADO_VILA

            elif acao == "sair":
                running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e:
                # Se estou na vila e no altar, vou para a floresta
                if mapa_atual == MAPA_VILA and player.hitbox.colliderect(altar_rect):
                    trocar_mapa(MAPA_FLORESTA, "mapa_floresta_sombria.tmx", "floresta_sombria.png", (420, 650))
                    estado = ESTADO_JOGANDO # Aqui ele entra no modo de combate
            if evento.key == pygame.K_ESCAPE:
                if estado == ESTADO_JOGANDO:
                    estado = ESTADO_PAUSADO
                elif estado == ESTADO_PAUSADO:
                    estado = ESTADO_JOGANDO
            if estado == ESTADO_GAME_OVER and evento.key == pygame.K_r:
                player.vida = 100
                player.hitbox.topleft = (420, 650)
                player.rect.center = player.hitbox.center

                player.morto = False
                player.frame_atual = 0
                player.estado = "parado"
                player.tomando_dano = False
                player.atacando = False

                for slime in slimes:
                    slime.rect.topleft = posicao_aleatoria(colisoes_vila)

                estado = ESTADO_JOGANDO
                # Verifica game over

    def trocar_mapa(novo_mapa, arquivo_tmx, arquivo_png, pos_inicial):
        global tmx_data, mapa_background, colisoes_vila, mapa_atual, mapa_overlay
        
        # Atualiza qual é o mapa agora
        mapa_atual = novo_mapa
        
        # Carrega os novos arquivos
        tmx_data = pytmx.util_pygame.load_pygame(f"mapas/{arquivo_tmx}")
        mapa_background = pygame.image.load(f"mapas/{arquivo_png}").convert()
        
        if novo_mapa == MAPA_FLORESTA:
            mapa_overlay = pygame.image.load("mapas/overlay_floresta.png").convert_alpha()
        else:
            mapa_overlay = None
        
        # Reseta e carrega as novas colisões
        colisoes_vila.clear()
        for obj in tmx_data.get_layer_by_name("COLISÕES"):
            colisoes_vila.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # Atualiza o player
        player.colisoes = colisoes_vila
        player.hitbox.topleft = pos_inicial

    if player.morto and tempo_morte == 0:
        tempo_morte = pygame.time.get_ticks()

    if player.morto:
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - tempo_morte >= 2000:
            estado = ESTADO_GAME_OVER

    map_width = mapa_background.get_width()
    map_height = mapa_background.get_height()

    camera_x = player.rect.centerx - WIDTH // 2
    camera_y = player.rect.centery - HEIGHT // 2

    # trava nos limites
    camera_x = max(0, min(camera_x, map_width - WIDTH))
    camera_y = max(0, min(camera_y, map_height - HEIGHT))

    if estado == ESTADO_MENU:
        tela_menu.draw(screen)

        pygame.display.flip()
        continue

    screen.blit(mapa_background, (-camera_x, -camera_y))

        # player na vila
    if estado == ESTADO_VILA:
        player.update(velocidade, [])

    # combate
    if estado == ESTADO_JOGANDO:

        # spawn slimes
        if len(slimes) == 0:
            for _ in range(2):
                x, y = posicao_aleatoria(colisoes_vila)

                novo_slime = Slime(x, y)
                novo_slime.colisoes = colisoes_vila

                slimes.add(novo_slime)

        player.update(velocidade, slimes)
        slimes.update(player)
        drops.update()

    # lista dos slimes mortos
    slimes_mortos = []

    for slime in slimes:

        if slime.morto:

            # conta kill uma vez
            if not hasattr(slime, "contado"):
                slimes_abatidos += 1
                slime.contado = True

            # drop pão
            if random.random() <= 0.5:

                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-20, 0)

                drop = Pao(
                    slime.rect.centerx + offset_x,
                    slime.rect.centery + offset_y
                )

                drops.add(drop)

            # drop moeda
            if random.random() <= 0.7:

                offset_x = random.randint(-20, 20)
                offset_y = random.randint(-20, 0)

                moeda = Moeda(
                    slime.rect.centerx + offset_x,
                    slime.rect.centery + offset_y
                )

                moedas.add(moeda)

            # adiciona na lista pra remover depois
            slimes_mortos.append(slime)

    # remove e respawna depois do loop
    for slime in slimes_mortos:

        slimes.remove(slime)

        x, y = posicao_aleatoria(colisoes_vila)

        novo_slime = Slime(x, y)
        novo_slime.colisoes = colisoes_vila

        slimes.add(novo_slime)

    # coleta pão
    coletado = []

    for drop in drops:
        if player.hitbox.colliderect(drop.rect):
            coletado.append(drop)
            drop.kill()

    # coleta moedas
    for moeda in moedas:
        if player.hitbox.colliderect(moeda.rect):
            moeda.kill()
            player.score += 1

    # cura player
    for item in coletado:
        player.vida += 50

        if player.vida > 100:
            player.vida = 100

    # desenha player
    for p in players:
        screen.blit(
            p.image,
            (p.rect.x - camera_x, p.rect.y - camera_y)
        )

    # desenha slimes
    for slime in slimes:
        screen.blit(
            slime.image,
            (slime.rect.x - camera_x, slime.rect.y - camera_y)
        )

    # desenha drops
    for drop in drops:
        screen.blit(
            drop.image,
            (drop.rect.x - camera_x, drop.rect.y - camera_y)
        )

    # desenha moedas
    for moeda in moedas:
        screen.blit(
            moeda.image,
            (moeda.rect.x - camera_x, moeda.rect.y - camera_y)
        )

    # overlay floresta
    if mapa_atual == MAPA_FLORESTA and mapa_overlay:
        screen.blit(mapa_overlay, (-camera_x, -camera_y))

    # HUD
    hud.draw(screen, player, slimes_abatidos)

    # mensagem altar
    if estado == ESTADO_VILA and player.hitbox.colliderect(altar_rect):

        texto = fonte_msg.render(
            "Pressione E para teleportar para a Floresta Sombria",
            True,
            (255, 255, 255)
        )

        pos_x = WIDTH // 2 - texto.get_width() // 2

        screen.blit(texto, (pos_x, 50))

    # pause
    if estado == ESTADO_PAUSADO:
        tela_pause.draw(screen)

    # game over
    if estado == ESTADO_GAME_OVER:
        tela_game_over.draw(screen)

    pygame.display.flip()

    pygame.display.flip()

pygame.quit()