import pygame 
from  settings import PLAYER_SIZE,WIDTH,HEIGHT,FPS,PLAYER_SPEED
import os 

class Coin(pygame.sprite.Sprite): #o Sprite é a classe pai 
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill((255,200,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        try:
            self.image = pygame.image.load (os.path.join('imagens','coin.png')).convert_alpha() # carrega o sprite da pasta 
        except:
            self.image = pygame.Surface((20,20))
            self.image.fill((255,255,0))
