import pygame
import constantes as cst

class Entidade:
    def __init__(self, pos):
        self.pos = list(pos)
        self.animacao = None

        self.vel_x = 0
        self.vel_y = 0

        self.velocidade_antes_paralax = cst.VEL_PERSONAGEM
        self.dash_antes_paralax = cst.VELDASH

        self.contagem_frames = 0

class Player(Entidade):

    def __init__(self, pos, screen, vida):
        super().__init__(pos)

        self.vida = vida
        self.invulnerabilidade = 0

        self.screen = screen

        self.colisao = pygame.Rect(pos[0], pos[1], 160, 170)

        self.contagem_moeda = 0

        self.hitbox_atq = None

        self.state = 'idle'
        self.state_antes = None
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

        self.coracao_cheio = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_3-3.png'), (500, 170))
        self.coracao_2_3 = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_2-3.png'), (500, 170))
        self.coracao_1_3 = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_1-3.png'), (500, 170))
        self.coracao_vazio = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_0-3.png'), (500, 170))
        
        #DEFINIÇÃO DOS SPRITES DO PERSONAGEM
        self.idle = [pygame.transform.scale(pygame.image.load("Assets/Personagem/parado.png"), (100, 180))]
        
        self.andando = [pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_andando_0.png"), (200, 200)),
                        pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_andando_1.png"), (200, 200)),
                        pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_andando_2.png"), (200, 200)),
                        pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_andando_3.png"), (200, 200))]

        self.pulando = [pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_pulando_0.png"), (200, 200)),
                        pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_pulando_1.png"), (200, 200))]


        self.puloduplo =[pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_pulo_duplo_0.png"), (200, 200)),
                        pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_pulo_duplo_1.png"), (200, 200)),
                        pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_pulo_duplo_3.png"), (200, 200)),
                        pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_pulo_duplo_2.png"), (200, 200))]

        self.dash = [pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_dash_0.png"), (200, 200)),
                    pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_dash_1.png"), (200, 200)),
                    pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_dash_2.png"), (200, 200)),
                    pygame.transform.scale(pygame.image.load("Assets/Personagem/sprite_dash_3.png"), (200, 200))]
        
        self.ataque = [
            pygame.transform.scale(pygame.image.load("Assets/Personagem/atacando.png"), (200, 200))
        ]
        
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

            #EVENTO DE DAR DASH
            if event.key == pygame.K_p and self.cooldown_dash == 0:
                self.time_dash = cst.TEMPODASH
                self.cooldown_dash = cst.COOLDOWN_DASH
                self.state_antes_dash = self.state
                self.state = 'dash'

            #EVENTO DE ATACAR
            if event.key == pygame.K_o and self.state != 'dash' and self.cooldown_atq == 0:
                self.atacar()
                self.cooldown_atq = cst.COOLDOWN_ATQ
                self.vel_x = 0

    def atualizar_animacao(self):

        if self.cooldown_atq > 0:
            self.state = 'atacando'
        else:
            if self.state != 'atacando':
                self.state_antes = self.state
            self.state = self.state_antes

        #Atualizando os estados para mudar a animação
        if self.vel_y != 0 and self.state != 'pulo duplo' and self.state != 'dash' and self.state != 'atacando':
            self.state = 'pulando'
        elif self.vel_x != 0 and self.vel_y == 0 and self.state != 'dash' and self.state != 'atacando':
            self.state = 'andando'
        elif self.vel_x == 0 and self.vel_y == 0 and self.state != 'dash' and self.state != 'atacando':
            self.state = 'idle'

        if self.state != self.state_antes:
            self.contagem_frames = 0

        if self.no_chao and self.state == 'pulando' and self.vel_y == 0:
            self.state = 'idle'

        if self.state == 'atacando':
            self.animacao = self.ataque
        elif self.state == 'dash':
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

        #REINICIA O DASH RAPIDO PORÉM APENAS NO CHÃO
        if (self.cooldown_dash > 0 and self.no_chao):
            self.cooldown_dash -= 5

            if (self.cooldown_dash < 0):
                self.cooldown_dash = 0

        self.y_anterior = self.pos[1]

        self.vel_x = 0

        if self.state != 'atacando':
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

        #DEFINE A COLISÃO DO ATAQUE PARA A DIREITA
        if self.andando_direita:
            self.hitbox_atq = pygame.Rect(self.pos[0] + 40, self.pos[1], 50, 64)

        #DEFINE A COLISÃO DO ATAQUE PARA A ESQUERDA
        else:
            self.hitbox_atq = pygame.Rect(self.pos[0] - 35, self.pos[1], 50, 64)

    def atualizar_vida(self):
        if self.vida == 3:
            self.screen.blit(self.coracao_cheio, (15, 15))
        elif self.vida == 2:
            self.screen.blit(self.coracao_2_3, (15, 15))
        elif self.vida == 1:
            self.screen.blit(self.coracao_1_3, (15, 15))
        else:
            self.screen.blit(self.coracao_vazio, (15, 15))

    def desenhar(self):
        
        #linhas adicionais, pois estava dando erro de index out of range
        #para solucionar coloquei o if que reseta a contagem de frames
        #impedindo o erro de index out of range
        if self.contagem_frames >= len(self.animacao):
            self.contagem_frames = 0

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

    def emparalax(self):

        #ISSO FAZ COM QUE O PERSONAGEM MANTENHA AS ANIMAÇÕES MAS NÃO SE MOVA DURANTE O PARALAX
        cst.VEL_PERSONAGEM = 0.000001
        cst.VELDASH = 0.000001

    def semparalax(self, empulso):

        cst.VEL_PERSONAGEM = self.velocidade_antes_paralax
        cst.VELDASH = self.dash_antes_paralax
        self.pos[0] += empulso

class Inimigo1(Entidade):
    def __init__(self, pos, screen, vida):
        super().__init__(pos)
        self.screen = screen
        self.vida = vida