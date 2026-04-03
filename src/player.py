import pygame
from settings import WIDTH, HEIGHT, ANIMACAO_SPEED, PLAYER_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.score = 0
        
        # animações
        self.frames_parado = self.carregar_frames('imagens/PARADO.png', 7)
        self.frames_andando = self.carregar_frames('imagens/ANDA.png', 8)
        self.frames_hit = self.carregar_frames('imagens/PLAYER_DANO.png', 4)
        self.frames_ataque = self.carregar_frames('imagens/PLAYER_ATAQUE1.png', 6)
        self.frames_morte = self.carregar_frames('imagens/PLAYER_MORTE.png', 12)
        self.morto = False
        # estado e controle de animação
        self.estado = "parado"
        self.frame_atual = 0
        self.velocidade_animacao = ANIMACAO_SPEED

        # sprite inicial
        self.image = self.frames_parado[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

        # HITBOX separada
        self.hitbox = pygame.Rect(0, 0, 30, 40)
        self.hitbox.center = self.rect.center

        # vida
        self.vida = 100

        # direção
        self.direcao = "direita"

        # dano recebido
        self.tomando_dano = False
        self.tempo_dano = 0
        self.cooldown_dano = 800  # ms

        # ataque do player
        self.atacando = False
        self.tempo_ataque = 0
        self.cooldown_ataque = 500  # ms entre ataques
        self.distancia_ataque = 60  # alcance em pixels
        self.dano_ataque = 10

    def carregar_frames(self, caminho, num_frames):
        sprite_sheet = pygame.image.load(caminho).convert_alpha()
        largura_frame = sprite_sheet.get_width() // num_frames
        altura_frame = sprite_sheet.get_height()
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
            frame = pygame.transform.scale(frame, PLAYER_SIZE)
            frames.append(frame)
        return frames

    def update(self, velocidade, slimes):
        tempo_atual = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if self.morto:
            self.frame_atual += self.velocidade_animacao
            if self.frame_atual >= len(self.frames_morte):
                self.frame_atual = len(self.frames_morte) - 1  # mantém o último frame
                return "fim_animacao_morte"  # sinaliza que a animação terminou
            self.image = self.frames_morte[int(self.frame_atual)]
            if self.direcao == "esquerda":
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center=self.hitbox.center)
            return  # trava tudo até animação acabar

        # -----------------------------
        # 1️⃣ Trava de dano
        if self.tomando_dano:
            self.frame_atual += self.velocidade_animacao

            if self.frame_atual >= len(self.frames_hit):
                self.frame_atual = 0
                self.tomando_dano = False

            self.image = self.frames_hit[int(self.frame_atual)]

            # mantém direção
            if self.direcao == "esquerda":
                self.image = pygame.transform.flip(self.image, True, False)

            return  # sai sem mover nem atacar

        # -----------------------------
        # 2️⃣ Iniciar ataque
        if keys[pygame.K_SPACE] and not self.atacando and (tempo_atual - self.tempo_ataque > self.cooldown_ataque):
            self.atacando = True
            self.frame_atual = 0
            self.tempo_ataque = tempo_atual

        # -----------------------------
        # 3️⃣ Ataque
        # Atacar quando tecla SPACE for pressionada
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.atacando:
            self.atacando = True
            self.tempo_ataque = pygame.time.get_ticks()
            self.frame_atual = 0

        # Executa animação de ataque
        if self.atacando:
            self.frame_atual += self.velocidade_animacao
            if self.frame_atual >= len(self.frames_ataque):
                self.frame_atual = 0
                self.atacando = False

            self.image = self.frames_ataque[int(self.frame_atual)]
            if self.direcao == "esquerda":
                self.image = pygame.transform.flip(self.image, True, False)

            # Aplica dano só no primeiro frame da animação ou quando quiser
            if int(self.frame_atual) == 1:  # frame de impacto da espada
                for slime in slimes:
                    if slime and hasattr(slime, "rect") and hasattr(slime, "levar_dano"):
                        direcao = pygame.Vector2(slime.rect.center) - pygame.Vector2(self.hitbox.center)
                        distancia = direcao.length()
                        # verifica se está na mesma direção que o Player
                        olhando_certo = (self.direcao == "direita" and direcao.x >= 0) or \
                                        (self.direcao == "esquerda" and direcao.x <= 0)
                        if distancia <= self.distancia_ataque and olhando_certo:
                            slime.levar_dano(self.dano_ataque)

            return  # trava movimento durante ataque

        # -----------------------------
        # 4️⃣ Movimento normal
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
            self.direcao = "esquerda"

        # -----------------------------
        # 5️⃣ Animação andar/parado
        novo_estado = "andando" if movendo else "parado"
        if novo_estado != self.estado:
            self.frame_atual = 0
        self.estado = novo_estado

        self.frame_atual += self.velocidade_animacao

        if self.estado == "andando":
            frames = self.frames_andando
        else:
            frames = self.frames_parado

        if self.frame_atual >= len(frames):
            self.frame_atual = 0

        self.image = frames[int(self.frame_atual)]

        if self.direcao == "esquerda":
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=self.hitbox.center)

    # -----------------------------
    # 6️⃣ Receber dano
    def levar_dano(self, dano, origem=None):
        if self.morto:
            return

        tempo_atual = pygame.time.get_ticks()

        # cria dicionário se não existir
        if not hasattr(self, "cooldowns_por_inimigo"):
            self.cooldowns_por_inimigo = {}

        # pega último hit desse inimigo
        ultimo_hit = self.cooldowns_por_inimigo.get(origem, 0)

        if tempo_atual - ultimo_hit > self.cooldown_dano:
            self.vida -= dano

            if self.vida <= 0:
                self.vida = 0
                self.morto = True
                self.frame_atual = 0
                return

            self.cooldowns_por_inimigo[origem] = tempo_atual
            self.tomando_dano = True
            self.frame_atual = 0