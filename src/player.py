import pygame 
from  settings import PLAYER_SIZE,WIDTH,HEIGHT,FPS,PLAYER_SPEED
import os 

class Player(pygame.sprite.Sprite): #o Sprite é a classe pai 
    def __init__(self,name):
        super().__init__()
        self.name = name          #self refere-se a class player 
        self.score = 0 
        self.image = pygame.Surface(PLAYER_SIZE)

        try:
            image_path = os.path.join('imagens','gato_down.png') # carrega o sprite da pasta 
            image_loaded  = pygame.image.load(image_path).convert_alpha()
            self.image = image_loaded
        except pygame.error as e:
            print(f"erro encontrado {e}")
            self.image.fill((255,120,255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.image = image_loaded
        self.original_image = self.image.copy()
    
def update(self,velocidade):
    keys = pygame.key.get_pressed()
    angulo = 0 

    if keys[pygame.K_s]:
        player.rect.y += velocidade
        angulo = 360
    elif keys[pygame.K_w]:
        player.rect.y -= velocidade
        angulo = 180
    elif keys[pygame.K_d]:
        player.rect.x += velocidade
        angulo = 90
    elif keys[pygame.K_a]:
        player.rect.x -= velocidade
        angulo = -90

    if angulo is not 0:
        centro = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, angulo)
        self.rect = self.image.get_rect(center=centro)

