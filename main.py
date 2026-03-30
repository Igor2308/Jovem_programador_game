import pygame

from settings import WIDTH, HEIGHT, FPS,PLAYER_SIZE,PLAYER_SPEED
from pygame.sprite import Sprite
import os
from src.player import Player
from src.coin import Coin


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Teste")
clock = pygame.time.Clock()
running = True

#grupo de jogadores
players = pygame.sprite.Group()
player = Player("P1")
players.add(player)

#grupo moedas
coins = pygame.sprite.Group()
for a in range(15):
    coin = Coin(a*10,a*10)
    coins.add(coin)


while running:
    delta = clock.tick(FPS)/1000.0
    velocidade = delta * PLAYER_SPEED
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                running = False
 
    player.rect.clamp_ip(screen.get_rect())
    screen.fill((45,156,200))
    #colisão
    colisao = pygame.sprite.spritecollide(player,coins,True,pygame.sprite.collide_mask)
    if colisao:
        print("Colisão")

    players.update(velocidade)
    players.draw(screen)
    coins.update()
    coins.draw(screen)
    
    player.rect.clamp_ip(screen.get_rect())
    
    screen.blit(player.image, player.rect)
    pygame.display.flip()

   
pygame.quit()

