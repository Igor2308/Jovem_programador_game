import pygame 
from settings import WIDTH,HEIGHT,ANIMACAO_SPEED,PLAYER_SIZE
import os 

class Player(pygame.sprite.Sprite): #o Sprite é a classe pai 
    def __init__(self,name):
        super().__init__()
        self.name = name          #self refere-se a class player 
        self.score = 0 
        self.frames_parado = self.carregar_frames('imagens/PARADO.png',7)        
        self.frames_andando = self.carregar_frames('imagens/ANDA.png',8)
        self.direcao = "direita"

        self.estado = "parado"
        self.frame_atual = 0
        self.velocidade_animacao = ANIMACAO_SPEED

        self.image = self.frames_parado[0]  
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

        # HITBOX separada 
        self.hitbox = pygame.Rect(0, 0, 30, 40)  # ajusta depois
        self.hitbox.center = self.rect.center
        

    
    def carregar_frames(self,caminho, num_frames):
        sprite_sheet = pygame.image.load(caminho).convert_alpha()

        largura_frame = sprite_sheet.get_width() // num_frames
        altura_frame =  sprite_sheet.get_height()

        frames = []

        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
            frame = pygame.transform.scale(frame, PLAYER_SIZE)
            frames.append(frame)
    
        return frames

    def update(self, velocidade):

        keys = pygame.key.get_pressed()

        movendo = False

        if keys[pygame.K_s]:
            self.hitbox.y += velocidade
            movendo = True
        if keys[pygame.K_w]:
            self.hitbox.y -= velocidade
            movendo = True
        if keys[pygame.K_d]:
            self.hitbox.x += velocidade
            movendo = True
            self.direcao = "direita"
        if keys[pygame.K_a]:
            self.hitbox.x -= velocidade
            movendo = True
            self.direcao = "esquerda" # diz pra que lado o sprite deve ficar apontado

        #aqui vai ler se ele ta parado ou andando
        novo_estado = "andando" if movendo else "parado"

        if novo_estado != self.estado:
            self.frame_atual = 0

        self.estado = novo_estado

        #animação
        self.frame_atual += self.velocidade_animacao

        if self.estado == "andando":
            frames = self.frames_andando
        else:
            frames = self.frames_parado

        if self.frame_atual >= len(frames):
            self.frame_atual = 0

        #self.hitbox.center = self.rect.center

        self.image = frames[int(self.frame_atual)]

        if self.direcao == "esquerda":
            self.image = pygame.transform.flip(self.image, True, False)

        # mantém o sprite centralizado na hitbox
        self.rect = self.image.get_rect(center=self.hitbox.center)

        