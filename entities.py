import pygame
import constantes as cst

class Entidade:
    def __init__(self, pos):
        self.pos = list(pos)
        self.animacao = None

        self.vel_x = 0
        self.vel_y = 0

        self.contagem_frames = 0

class Player(Entidade):
    def __init__(self, pos, screen, vida):
        super().__init__(pos)

        self.vida = vida
        self.invulnerabilidade = 0

        self.screen = screen

        self.colisao = pygame.Rect(pos[0], pos[1], 80, 80)

        self.contagem_moeda = 0

        self.hitbox_atq = None

        self.state = 'idle'
        self.state_antes = 'idle'
        self.state_antes_dash = 'idle'
        self.cooldown_dash = 0

        self.cooldown_atq = 0

        self.pulo_duplo = False

        self.andando_direita = True
        self.no_chao = False

        self.vel_x = 0
        self.vel_y = 0

        self.time_dash = 0

        self.pulo = 0

        self.contagem_frames = 0

        self.som_dano = pygame.mixer.Sound('Assets/Sons/tomou_dano.wav')

        self.coracao_cheio = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_cheia.png'), (64, 64))
        self.coracao_vazio = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_vazia.png'), (64, 64))
        
        #carregango o spritesheet
        self.sprite_totals= pygame.image.load("Assets/Personagem/sprite_1.png").convert_alpha()
        self.sprite_dash= pygame.image.load("Assets/Personagem/sprite_3.png").convert_alpha()
        
        self.idle = []
        for i in range(1,2):
            imagem=self.sprite_totals.subsurface((200*i,750),(200,250))
            imagem=pygame.transform.scale(imagem,(80,80))
            self.idle.append(imagem)

        self.andando = []
        for i in range(4):
            imagem=self.sprite_totals.subsurface((200*i,0),(200,250))
            imagem=pygame.transform.scale(imagem,(80,80))
            self.andando.append(imagem)

        self.pulando = []
        for i in range(4,6):
            imagem=self.sprite_totals.subsurface((200*i,0),(200,250))
            imagem=pygame.transform.scale(imagem,(80,80))
            self.pulando.append(imagem)

        self.puloduplo =[]
        for i in range(5,7):
            imagem=self.sprite_totals.subsurface((200*i,0),(200,250))
            imagem=pygame.transform.scale(imagem,(80,80))
            self.puloduplo.append(imagem)
        
        self.dash = []
        for i in range(4):
            imagem=self.sprite_dash.subsurface((384*i,0),(384,338))
            imagem=pygame.transform.scale(imagem,(80,80))
            self.dash.append(imagem)

        self.animacao = self.idle
        self.state = 'idle'

    #Muda as animações e os estados
    def processar_evento(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w and self.no_chao:
                self.pulo = cst.BUFFERPULO

            elif event.key == pygame.K_w and self.pulo_duplo and self.vel_y >= 0:
                self.pulo = cst.BUFFERPULO
                self.state = 'pulo duplo'

            if event.key == pygame.K_p and self.cooldown_dash == 0:
                self.time_dash = cst.TEMPODASH
                self.cooldown_dash = cst.COOLDOWN_DASH
                self.state_antes_dash = self.state
                self.state = 'dash'

            if event.key == pygame.K_o and self.state != 'dash' and self.cooldown_atq == 0:
                self.atacar()
                self.cooldown_atq = cst.COOLDOWN_ATQ
                self.vel_x = 0

    def atualizar_animacao(self):

        state_antes = self.state

        #Atualizando os estados para mudar a animação
        if self.vel_y != 0 and self.state != 'pulo duplo' and self.state != 'dash':
            self.state = 'pulando'
        elif self.vel_x != 0 and self.vel_y == 0 and self.state != 'dash':
            self.state = 'andando'
        elif self.vel_x == 0 and self.vel_y == 0 and self.state != 'dash':
            self.state = 'idle'

        if self.state != state_antes:
            self.contagem_frames = 0

        if self.no_chao and self.state == 'pulando' and self.vel_y == 0:
            self.state = 'idle'

        if self.state == 'dash':
            self.animacao = self.dash
        elif self.state == 'andando':
            self.animacao = self.andando
        elif self.state == 'pulando':
            self.animacao = self.pulando
        elif self.state == 'idle':
            self.animacao = self.idle
        elif self.state == 'pulo duplo':
            self.animacao = self.puloduplo

        if self.state != 'pulando':
            self.contagem_frames += 0.2
            if self.contagem_frames >= len(self.animacao):
                self.contagem_frames = 0
        else:
            if self.contagem_frames < 1:
                self.contagem_frames += 0.2

    def movimento(self):

        self.y_anterior = self.pos[1]

        self.vel_x = 0

        if self.cooldown_dash > 0:
            self.cooldown_dash -= 1

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            self.vel_x = -cst.VEL_PERSONAGEM
            self.andando_direita = False
        elif teclas[pygame.K_d]:
            self.vel_x = cst.VEL_PERSONAGEM
            self.andando_direita = True
        if self.pulo > 0:
            self.pulo -= 1

        if self.pulo > 0 and self.no_chao:
            self.vel_y = cst.PULO

        elif self.pulo > 0 and self.pulo_duplo and self.vel_y >= 0:
            self.vel_y = cst.PULO
            self.pulo_duplo = False

        if self.time_dash > 0:
            self.time_dash -= 1
            self.vel_y = 0
            if self.andando_direita:
                self.vel_x = cst.VELDASH
            elif not self.andando_direita:
                self.vel_x = -cst.VELDASH
            if self.time_dash == 0:
                self.state = self.state_antes_dash

        self.pos[0] += self.vel_x

        #Gravidade

        if self.state != 'dash':
            self.vel_y += cst.GRAVIDADE
            self.pos[1] += self.vel_y

        self.colisao.x = self.pos[0]
        self.colisao.y = self.pos[1]

    def atacar(self):
        if self.andando_direita:
            self.hitbox_atq = pygame.Rect(self.pos[0] + 140, self.pos[1], 50, 128)
            pygame.draw.rect(self.screen, cst.AMARELO, self.hitbox_atq)
        else:
            self.hitbox_atq = pygame.Rect(self.pos[0] - 50, self.pos[1], 50, 128)
            pygame.draw.rect(self.screen, cst.AMARELO, self.hitbox_atq)

    def atualizar_vida(self):
        if self.vida == 3:
            self.screen.blit(self.coracao_cheio, (15, 15))
            self.screen.blit(self.coracao_cheio, (45, 15))
            self.screen.blit(self.coracao_cheio, (75, 15))
        elif self.vida == 2:
            self.screen.blit(self.coracao_cheio, (15, 15))
            self.screen.blit(self.coracao_cheio, (45, 15))
            self.screen.blit(self.coracao_vazio, (75, 15))
        elif self.vida == 1:
            self.screen.blit(self.coracao_cheio, (15, 15))
            self.screen.blit(self.coracao_vazio, (45, 15))
            self.screen.blit(self.coracao_vazio, (75, 15))
        else:
            self.screen.blit(self.coracao_vazio, (15, 15))
            self.screen.blit(self.coracao_vazio, (45, 15))
            self.screen.blit(self.coracao_vazio, (75, 15))

    def desenhar(self):

        frame = self.animacao[int(self.contagem_frames)]

        if self.invulnerabilidade > 0:

            if (self.invulnerabilidade // 5) % 2 == 0:
                frame.set_alpha(100)
            else:
                frame.set_alpha(255)
        else:
            frame.set_alpha(255)

        if not self.andando_direita:
            frame = pygame.transform.flip(frame, True, False)

        self.screen.blit(frame, self.pos)

class Moeda(Entidade):
    def __init__(self, pos, screen):
        super().__init__(pos)
        self.screen = screen

        self.som_moeda = pygame.mixer.Sound('Assets/Sons/som_moeda.wav')

        self.colisao = pygame.Rect(pos[0], pos[1], 25, 25)

        self.animacao = [
            pygame.transform.scale(pygame.image.load('Assets/Coletáveis/moeda_00.png').convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load('Assets/Coletáveis/moeda_01.png').convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load('Assets/Coletáveis/moeda_02.png').convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load('Assets/Coletáveis/moeda_03.png').convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load('Assets/Coletáveis/moeda_04.png').convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load('Assets/Coletáveis/moeda_05.png').convert_alpha(), (64, 64))
        ]

        self.contagem_frames = 0
    
    def desenhar(self):

        self.contagem_frames += 0.1

        if self.contagem_frames >= len(self.animacao):
            self.contagem_frames = 0

        frame = self.animacao[int(self.contagem_frames)]

        self.screen.blit(frame, self.pos)

class Espinho(Entidade):
    def __init__(self, pos, screen):
        super().__init__(pos)

        self.screen = screen

        self.colisao = pygame.Rect(pos[0], pos[1] - 32, 30, 30)

    def desenhar(self):
        self.imagem = pygame.image.load('Assets/Ambiente/espinho.png')
        self.screen.blit(self.imagem, (self.pos[0], self.pos[1] - 32))