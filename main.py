import pygame
import random
import pytmx
import pytmx.util_pygame
from settings import WIDTH, HEIGHT, FPS, PLAYER_SIZE, PLAYER_SPEED
from src.player import Player
from src.slime import Slime
from src.pao import Pao
from src.ui.hud import HUD
from src.ui.tela_pause import TelaPause
from src.ui.tela_game_over import TelaGameOver
from src.moeda import Moeda

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

slimes_abatidos = 0

#cria um grupo
slimes = pygame.sprite.Group()
drops = pygame.sprite.Group()
moedas = pygame.sprite.Group()

ESTADO_VILA = "vila"
ESTADO_JOGANDO = "jogando"
ESTADO_PAUSADO = "pausado"
ESTADO_GAME_OVER = "game_over"

MAPA_VILA = "vila"
MAPA_FLORESTA = "floresta"
mapa_atual = MAPA_VILA # Começamos na vila

tmx_data = pytmx.util_pygame.load_pygame("mapas/Mapa_principal.tmx")

mapa_background = pygame.image.load("mapas/mapa_inicial.png").convert()

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

estado = ESTADO_VILA

while running:
    delta = clock.tick(FPS) / 1000.0
    velocidade = PLAYER_SPEED * delta 

    if estado == ESTADO_VILA:
        slimes.empty()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e:
                # Se estou na vila e no altar, vou para a floresta
                if mapa_atual == MAPA_VILA and player.hitbox.colliderect(altar_rect):
                    trocar_mapa(MAPA_FLORESTA, "mapa_floresta_sombria.tmx", "floresta_sombria.png", (200, 300))
                    estado = ESTADO_JOGANDO # Aqui ele entra no modo de combate
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

    def trocar_mapa(novo_mapa, arquivo_tmx, arquivo_png, pos_inicial):
        global tmx_data, mapa_background, colisoes_vila, mapa_atual
        
        # 1. Atualiza qual é o mapa agora
        mapa_atual = novo_mapa
        
        # 2. Carrega os novos arquivos
        tmx_data = pytmx.util_pygame.load_pygame(f"mapas/{arquivo_tmx}")
        mapa_background = pygame.image.load(f"mapas/{arquivo_png}").convert()
        
        # 3. Reseta e carrega as novas colisões
        colisoes_vila.clear()
        for obj in tmx_data.get_layer_by_name("COLISÕES"):
            colisoes_vila.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # 4. Atualiza o player
        player.colisoes = colisoes_vila
        player.hitbox.topleft = pos_inicial

    if player.vida <= 0 and estado != ESTADO_GAME_OVER:
        player.morto = True
        estado = ESTADO_GAME_OVER

    map_width = mapa_background.get_width()
    map_height = mapa_background.get_height()

    # Atualiza jogo apenas se não estiver game over
    # SEMPRE desenha o fundo primeiro
    camera_x = player.rect.centerx - WIDTH // 2
    camera_y = player.rect.centery - HEIGHT // 2

    # trava nos limites
    camera_x = max(0, min(camera_x, map_width - WIDTH))
    camera_y = max(0, min(camera_y, map_height - HEIGHT))

    screen.blit(mapa_background, (-camera_x, -camera_y))
    
    #comando para ver as colisões dos objetos
    for colisao in colisoes_vila:
        pygame.draw.rect(screen, (255, 0, 0),
            (colisao.x - camera_x, colisao.y - camera_y, colisao.width, colisao.height), 2)
        
        pygame.draw.rect(screen, (0, 0, 255), 
        (altar_rect.x - camera_x, altar_rect.y - camera_y, altar_rect.width, altar_rect.height), 2)
    if estado == ESTADO_VILA:
        player.update(velocidade, [])  # player funciona, mas sem inimigos

    if estado == ESTADO_JOGANDO:

     # para spawnar slimes
        if len(slimes) == 0:
            for _ in range(2):
                x, y = posicao_aleatoria()
                novo_slime = Slime(x, y)
                novo_slime.colisoes = colisoes_vila
                slimes.add(novo_slime)

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

                #vai spawnar a moeda quando o player morrer
                if random.random() <= 0.7:
                    offset_x = random.randint(-20, 20)
                    offset_y = random.randint(-20, 0)

                    moeda = Moeda(
                        slime.rect.centerx + offset_x,
                        slime.rect.centery + offset_y
                    )
                    moedas.add(moeda)
                #vai respawnar o slime
                x, y = posicao_aleatoria()
                novo_slime = Slime(x, y)
                novo_slime.colisoes = colisoes_vila
                slimes.add(novo_slime)
                slimes.remove(slime)

        coletado = []

        for drop in drops:
            if player.hitbox.colliderect(drop.rect):
                coletado.append(drop)
                drop.kill()
                
        for moeda in moedas:
            if player.hitbox.colliderect(moeda.rect):
                moeda.kill()
                player.score += 1

        for item in coletado:
            player.vida += 50
            if player.vida > 100:
                player.vida = 100

        # contador e spawn continuam iguais...
    elif estado == ESTADO_GAME_OVER:
        pass

    # Desenha sprites
    for p in players:
        screen.blit(p.image, (p.rect.x - camera_x, p.rect.y - camera_y))

    for slime in slimes:
        screen.blit(slime.image, (slime.rect.x - camera_x, slime.rect.y - camera_y))

    for drop in drops:
        screen.blit(drop.image, (drop.rect.x - camera_x, drop.rect.y - camera_y))

    for moeda in moedas:
        screen.blit(moeda.image, (moeda.rect.x - camera_x, moeda.rect.y - camera_y))

    pygame.draw.rect(
        screen,
        (0, 255, 0),  # verde
        (player.hitbox.x - camera_x,
        player.hitbox.y - camera_y,
        player.hitbox.width,
        player.hitbox.height),
        2  # espessura da borda
    )

    # HUD sempre fica por cima de tudo
    hud.draw(screen, player, slimes_abatidos)

    if estado == ESTADO_VILA and player.hitbox.colliderect(altar_rect):
        texto = fonte_msg.render("Pressione E para teleportar para a Floresta Sombria", True, (255, 255, 255))
        # Centraliza o texto na parte superior
        pos_x = WIDTH // 2 - texto.get_width() // 2
        screen.blit(texto, (pos_x, 50))

    if estado == ESTADO_PAUSADO:
        tela_pause.draw(screen)

    if estado == ESTADO_GAME_OVER:
        tela_game_over.draw(screen)

    pygame.display.flip()

pygame.quit()