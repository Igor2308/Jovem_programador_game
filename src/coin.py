import pygame 
from  settings import PLAYER_SIZE,WIDTH,HEIGHT,FPS,PLAYER_SPEED
import os 

class Coin(pygame.sprite.Sprite): #o Sprite é a classe pai 
    def __init__(self,x,y):
        super().__init__()
     
        try:
            image_path = os.path.join('imagens','coin.png')
            self.image = pygame.image.load (image_path).convert_alpha() # carrega o sprite da pasta 
            self.image = pygame.transform.scale(self.image, (45,45))
            self.mask = pygame.mask.from_surface(self.image)
        except:
            self.image = pygame.Surface((32,32))
            self.image.fill((255,255,0))

        self.original_image = self.image
        self.angulo = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def update(self):
        self.angulo += 2

        centro = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angulo)
        self.rect = self.image.get_rect(center=centro)