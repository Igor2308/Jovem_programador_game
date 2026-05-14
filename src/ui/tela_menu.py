import pygame
import cv2
from settings import WIDTH, HEIGHT

class TelaMenu:
    def __init__(self):

        self.video = cv2.VideoCapture("videos/menu.mp4")

        self.frame_delay = 0
        self.frame_surface = pygame.Surface((WIDTH, HEIGHT))

        # botão de iniciar 
        self.botao_iniciar = pygame.image.load(
            "imagens/botao_iniciar.png"
        ).convert_alpha()
        self.botao_iniciar = pygame.transform.scale(
            self.botao_iniciar,
            (300, 90)
        )

        self.botao_iniciar_hover = pygame.image.load(
            "imagens/botao_iniciar_selecionado.png"
        ).convert_alpha()
        self.botao_iniciar_hover = pygame.transform.scale(
            self.botao_iniciar_hover,
            (300, 90)
        )

        # botão de sair
        self.botao_sair = pygame.image.load(
            "imagens/botao_sair.png"
        ).convert_alpha()
        self.botao_sair = pygame.transform.scale(
            self.botao_sair,
            (300, 90)
        )

        self.botao_sair_hover = pygame.image.load(
            "imagens/botao_sair_selecionado.png"
        ).convert_alpha()
        self.botao_sair_hover = pygame.transform.scale(
            self.botao_sair_hover,
                (300, 90)
            )

        # posições
        self.rect_iniciar = self.botao_iniciar.get_rect(center=(WIDTH // 2, 250))
        self.rect_sair = self.botao_sair.get_rect(center=(WIDTH // 2, 500))

    def draw(self, screen):

        self.frame_delay += 1

        # só atualiza o frame a cada 2 loops
        if self.frame_delay >= 2:

            ret, frame = self.video.read()

            if not ret:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.transpose(frame)

            self.frame_surface = pygame.surfarray.make_surface(frame)
            self.frame_surface = pygame.transform.scale(
                self.frame_surface,
                (WIDTH, HEIGHT)
            )

            self.frame_delay = 0
                # desenha no fundo

        screen.blit(self.frame_surface, (0, 0))
    
        mouse_pos = pygame.mouse.get_pos()

        if self.rect_iniciar.collidepoint(mouse_pos):
            screen.blit(self.botao_iniciar_hover, self.rect_iniciar)
        else:
            screen.blit(self.botao_iniciar, self.rect_iniciar)

        if self.rect_sair.collidepoint(mouse_pos):
            screen.blit(self.botao_sair_hover, self.rect_sair)
        else:
            screen.blit(self.botao_sair, self.rect_sair)

    def verificar_clique(self, evento):

        if evento.type == pygame.MOUSEBUTTONDOWN:
            
            # clique esquerdo
            if evento.button == 1:

                # botão iniciar
                if self.rect_iniciar.collidepoint(evento.pos):
                    return "iniciar"

                # botão sair
                if self.rect_sair.collidepoint(evento.pos):
                    return "sair"
                
    def fechar_video(self):
        self.video.release()