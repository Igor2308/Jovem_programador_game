import pygame
import random

from settings import WIDTH, HEIGHT, FPS, PLAYER_SIZE, PLAYER_SPEED
from pygame.sprite import Sprite
import os
from src.player import Player
from src.coin import Coin

def posicao_aleatoria():
    x = random.randint(0, WIDTH - 45)
    y = random.randint(0, HEIGHT - 45)
    return x, y 


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Teste")
clock = pygame.time.Clock()
running = True
background = pygame.image.load("imagens/fundo.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

#grupo de jogadores
players = pygame.sprite.Group()
player = Player("P1")
players.add(player)

#grupo moedas
coins = pygame.sprite.Group()
for _ in range(15):
    x, y = posicao_aleatoria()
    coins.add(Coin(x, y))


while running:
    delta = clock.tick(FPS)/1000.0
    velocidade = delta * PLAYER_SPEED
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                running = False
 
    screen.blit(background, (0, 0))
    #colisão
    colisao = pygame.sprite.spritecollide(player,coins,True,pygame.sprite.collide_mask)
    if colisao:
        for _ in colisao:
            x, y = posicao_aleatoria()
            coins.add(Coin(x, y))
        print("Colisão")
        

    players.update(velocidade)
    player.rect.clamp_ip(screen.get_rect())
    players.draw(screen)
    coins.update()
    coins.draw(screen)
    
    player.hitbox.clamp_ip(screen.get_rect())
    #pygame.draw.rect(screen, (0,255,0), player.hitbox, 2)
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    
   
pygame.quit()

