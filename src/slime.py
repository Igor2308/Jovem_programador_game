import pygame

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # -----------------------------
        # animações
        self.frames_parado = self.carregar_frames('imagens/slime_parado.png', 9)
        self.frames_andando = self.carregar_frames('imagens/slime_andando.png', 8)
        self.frames_dano = self.carregar_frames('imagens/slime_dano.png', 6)
        self.frames_morte = self.carregar_frames('imagens/slime_morrendo.png', 10)

        # -----------------------------
        # estado
        self.estado = "parado"
        self.frame_atual = 0
        self.velocidade_animacao = 0.13

        # sprite inicial
        self.image = self.frames_parado[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # movimento
        self.velocidade = 100
        self.direcao = pygame.Vector2(0, 0)
        self.olhando_direita = True

        # ataque
        self.tempo_ataque = 0
        self.cooldown_ataque = 1000
        self.dano = 5
        self.DISTANCIA_ATAQUE = 60

        # vida
        self.vida = 50
        self.tomando_dano = False
        self.morto = False
        self.tempo_dano = 0
        self.cooldown_dano = 300  # evita receber dano muito rápido

    # --------------------------------
    # carregar frames
    def carregar_frames(self, caminho, quantidade):
        frames = []
        sprite_sheet = pygame.image.load(caminho).convert_alpha()
        largura_frame = sprite_sheet.get_width() // quantidade
        altura_frame = sprite_sheet.get_height()

        for i in range(quantidade):
            frame = sprite_sheet.subsurface(
                (i * largura_frame, 0, largura_frame, altura_frame)
            )
            frames.append(frame)
        return frames

    # --------------------------------
    # receber dano
    def levar_dano(self, dano):
        if self.morto:
            return
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_dano > self.cooldown_dano:
            self.vida -= dano
            self.tomando_dano = True
            self.frame_atual = 0
            self.tempo_dano = tempo_atual
            # verifica se morreu
            if self.vida <= 0:
                self.estado = "morrendo"
                self.frame_atual = 0
                self.morto = True

    # --------------------------------
    # update do slime
    def update(self, player):
        if self.morto:
            # animação de morte
            self.frame_atual += self.velocidade_animacao
            if self.frame_atual >= len(self.frames_morte):
                self.frame_atual = len(self.frames_morte) - 1  # fica na última frame
            self.image = self.frames_morte[int(self.frame_atual)]
            return

        # direção até o player
        direcao = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        distancia = direcao.length()
        if distancia > 0:
            direcao = direcao.normalize()

        # decide se anda ou para
        if distancia > self.DISTANCIA_ATAQUE:
            self.direcao = direcao
        else:
            self.direcao = pygame.Vector2(0, 0)

        # estado andando/parado
        if self.tomando_dano:
            # animação de dano
            self.frame_atual += self.velocidade_animacao
            if self.frame_atual >= len(self.frames_dano):
                self.frame_atual = 0
                self.tomando_dano = False
            self.image = self.frames_dano[int(self.frame_atual)]
        else:
            novo_estado = "andando" if self.direcao.length() > 0 else "parado"
            if novo_estado != self.estado:
                self.estado = novo_estado
                self.frame_atual = 0

            self.frame_atual += self.velocidade_animacao
            if self.estado == "parado":
                if self.frame_atual >= len(self.frames_parado):
                    self.frame_atual = 0
                self.image = self.frames_parado[int(self.frame_atual)]
            elif self.estado == "andando":
                if self.frame_atual >= len(self.frames_andando):
                    self.frame_atual = 0
                self.image = self.frames_andando[int(self.frame_atual)]

        # flip horizontal
        if self.direcao.x < 0:
            self.olhando_direita = False
        elif self.direcao.x > 0:
            self.olhando_direita = True
        if not self.olhando_direita:
            self.image = pygame.transform.flip(self.image, True, False)

        # movimento
        self.rect.x += self.direcao.x * self.velocidade * 0.016
        self.rect.y += self.direcao.y * self.velocidade * 0.016

        # ataque do slime ao player
       # slime.py → dentro do update
        tempo_atual = pygame.time.get_ticks()

        # verifica se Player está a X pixels de distância
        if distancia <= self.DISTANCIA_ATAQUE:
            if tempo_atual - self.tempo_ataque > self.cooldown_ataque:
                player.levar_dano(self.dano, self)
                self.tempo_ataque = tempo_atual