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

    def __init__(self, pos, screen, vida, especial):
        super().__init__(pos)

        self.vida = vida
        self.especial = especial
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

        self.desbloqueou_dash = False
        self.desbloqueou_pulo_duplo = False

        self.andando_direita = True
        self.no_chao = False

        self.y_anterior = 700

        self.vel_x = 0
        self.vel_y = 0

        self.time_dash = 0

        self.pulo = 0

        self.y_anterior = pos[1]
        
        self.contagem_frames = 0

        self.som_dano = pygame.mixer.Sound('Assets/Sons/tomou_dano.wav')
        self.som_dano.set_volume(0.8)

        self.coracao_cheio = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_3-3.png'), (500, 170))
        self.coracao_2_3 = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_2-3.png'), (500, 170))
        self.coracao_1_3 = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_1-3.png'), (500, 170))
        self.coracao_vazio = pygame.transform.scale(pygame.image.load('Assets/Personagem/vida_0-3.png'), (500, 170))

        self.especial_vazio = pygame.transform.scale(pygame.image.load('Assets/Personagem/especial_apagado.png'), (288, 100))
        self.especial_1_3 = pygame.transform.scale(pygame.image.load('Assets/Personagem/especial_vermelho.png'), (288, 100))
        self.especial_2_3 = pygame.transform.scale(pygame.image.load('Assets/Personagem/especial_amarelo.png'), (288, 100))
        self.especial_cheio = pygame.transform.scale(pygame.image.load('Assets/Personagem/especial_verde.png'), (288, 100))
        
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
            if event.key == pygame.K_p and self.cooldown_dash == 0 and self.desbloqueou_dash:
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

            self.hitbox_atq = None #Destrói a hitbox quando acaba o ataque

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
        elif self.state == 'dash' and self.desbloqueou_dash:
            self.animacao = self.dash
        elif self.state == 'andando':
            self.animacao = self.andando
        elif self.state == 'pulando':
            self.animacao = self.pulando
        elif self.state == 'idle':
            self.animacao = self.idle
        elif self.state == 'pulo duplo' and self.desbloqueou_pulo_duplo:
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

            elif self.pulo > 0 and self.pulo_duplo and self.vel_y >= 0 and self.desbloqueou_pulo_duplo:
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
        #Desce a hitbox (em relação à cabeça) em 60 pixels para ir para o braço
        altura_soco = self.pos[1] + 30

        #DEFINE A COLISÃO DO ATAQUE PARA A DIREITA
        if self.andando_direita:
            self.hitbox_atq = pygame.Rect(self.pos[0] + 100, altura_soco, 125, 64)

        #DEFINE A COLISÃO DO ATAQUE PARA A ESQUERDA
        else:
            #Empurra a hitbox mais para a esquerda para acompanhar o soco
            self.hitbox_atq = pygame.Rect(self.pos[0] - 125, altura_soco, 125, 64)

    def atualizar_vida(self):
        if self.vida == 3:
            self.screen.blit(self.coracao_cheio, (15, 15))
        elif self.vida == 2:
            self.screen.blit(self.coracao_2_3, (15, 15))
        elif self.vida == 1:
            self.screen.blit(self.coracao_1_3, (15, 15))
        else:
            self.screen.blit(self.coracao_vazio, (15, 15))

    def atualizar_especial(self):
        if self.especial == 0:
            self.screen.blit(self.especial_vazio, (42, 150))
        elif self.especial == 1:
            self.screen.blit(self.especial_1_3, (42, 150))
        elif self.especial == 2:
            self.screen.blit(self.especial_2_3, (42, 150))
        elif self.especial >= 3:
            self.screen.blit(self.especial_cheio, (42, 150))

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

        #variável para armazenar a posição onde a imagem será desenhada
        pos_desenho = list(self.pos)

        if not self.andando_direita:
            frame = pygame.transform.flip(frame, True, False)
            
            #Move o sprite do soco 100 pixels para a frente, pq o sprite do soco é 100 pixels maior que o do idle, e quando dava flip eles tavam ficando no mesmo lugar
            if self.state == 'atacando':
                pos_desenho[0] = pos_desenho[0] - 100

        #Usa pos_desenho para renderizar o personagem
        self.screen.blit(frame, pos_desenho)
        
        #testar a hitbox
        if self.hitbox_atq is not None:
            pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox_atq, 2)

    def emparalax(self):

        #ISSO FAZ COM QUE O PERSONAGEM MANTENHA AS ANIMAÇÕES MAS NÃO SE MOVA DURANTE O PARALAX
        cst.VEL_PERSONAGEM = 0.000001
        cst.VELDASH = 0.000001

    def semparalax(self, empulso):

        cst.VEL_PERSONAGEM = self.velocidade_antes_paralax
        cst.VELDASH = self.dash_antes_paralax
        self.pos[0] += empulso

class Inimigo_Corpo_a_Corpo(Entidade):

    def __init__(self, pos, screen, sprites_vida):

        super().__init__(pos)
        self.screen = screen
        self.vida = 3
        self.sprites_vida = sprites_vida

        #DEFINE O SPRITE ATUAL DE MOVIMENTO DO INIMIGO
        self.sprite_atual = None

        self.colisao = pygame.Rect(self.pos[0], self.pos[1], 160, 170)
        self.invulnerabilidade = 0
        self.y_anterior = self.pos[1]

        #BOOLEANA QUE MANTE O INIMIGO ATACANDO
        self.atacando = False
        self.atacando_contador = 20
        self.atacou = False

        #VARIÁVES QUE PARAM O INIMIGO QUANDO ELE TOMA UM DANO
        self.tomoudano = False
        self.cooldown = 100

        #BOOLEANA QUE INVERTE A IMAGEM DO INIMIGO CONFORME A DIREÇÃO DO INIMIGO
        self.direita = False

        #CONTADOR PARA O SPRITE ANDANDO DO INIMIGO
        self.contador_inimigo = 0

        #DEFINE OS SPRITES DO INIMIGO ANDANDO
        self.sprites_andando = [
            pygame.transform.scale(pygame.image.load("Assets/Inimigo/inimigo-andando00.png"), (160, 170)),
            pygame.transform.scale(pygame.image.load("Assets/Inimigo/inimigo-andando01.png"), (160, 170)),
            pygame.transform.scale(pygame.image.load("Assets/Inimigo/inimigo-andando02.png"), (160, 170)),
            pygame.transform.scale(pygame.image.load("Assets/Inimigo/inimigo-andando03.png"), (160, 170))

        ]

        #DEFINE OS SPRITES DO INIMIGO ATACANDO
        self.sprite_atacando = pygame.transform.scale(pygame.image.load('Assets/Inimigo/inimigo-atacando.png'), (280, 230))

    def atualizar(self, player, plataformas):
        # Se a vida for 0, ele morre e não faz mais nada
        if self.vida <= 0:
            return

        #Persegue o jogador no eixo X
        if self.pos[0] < player.pos[0]:
            self.vel_x = cst.VEL_INIMIGO
            self.direita = True

            #TEMPORIZADOR QUE PARA O INIMIGO QUANDO ELE TOMA DANO
            if ((self.tomoudano == True) or (self.atacou == True)) and (self.cooldown > 0):
                self.vel_x = 0
                self.cooldown -= 10

            else:
                self.atacou = False
                self.tomoudano = False
                self.cooldown = 100

        elif self.pos[0] > player.pos[0]:
            
            self.vel_x = -cst.VEL_INIMIGO
            self.direita = False

            #TEMPORIZADOR QUE PARA O INIMIGO QUANDO ELE TOMA DANO
            if ((self.tomoudano == True) or (self.atacou == True)) and (self.cooldown > 0):
                self.vel_x = 0
                self.cooldown -= 10

            else:
                self.atacou = False
                self.tomoudano = False
                self.cooldown = 100

        # Aplica gravidade para ele não voar
        self.vel_y += cst.GRAVIDADE
        
        self.y_anterior = self.pos[1]
        self.pos[0] += self.vel_x
        self.pos[1] += self.vel_y
        
        self.colisao.x = self.pos[0]
        self.colisao.y = self.pos[1]

        # Colisão do inimigo com o chão
        for plataforma in plataformas:
            pe_anterior = self.y_anterior + self.colisao.height
            pe_atual = self.colisao.bottom
            if self.colisao.right > plataforma.left and self.colisao.left < plataforma.right and pe_anterior <= plataforma.top and pe_atual >= plataforma.top and self.vel_y >= 0:
                self.vel_y = 0
                self.pos[1] = plataforma.top - self.colisao.height
                self.colisao.y = self.pos[1]
                break

        # Reduz o tempo de invulnerabilidade
        if self.invulnerabilidade > 0:
            self.invulnerabilidade -= 1

    def desenhar(self):
        if self.vida > 0:

            # Efeito de piscar quando toma dano
            if self.invulnerabilidade > 0 and (self.invulnerabilidade // 5) % 2 == 0:

                #Inimigo dá uma parada quando toma dano
                if self != 'player':
                    cst.VEL_INIMIGO = 0

                pass 
            else:
                #Velocidade volta ao normal depois de parar de piscar
                if self != 'player' and self.invulnerabilidade == 0:
                    cst.VEL_INIMIGO = 3

                #SOMA O CONTADOR PARA MUDAR O SPRITE ANDANDO DO INIMIGO
                self.contador_inimigo += 0.14

                #CONTROLE PARA NÃO TER OUT OF INDEX
                if (self.contador_inimigo > 3):
                    self.contador_inimigo = 0

                #DESENHA O SPRITE DO INIMIGO
                if (self.direita == False):
                    
                    #VERIFICA SE O INIMIGO ESTÁ ATACANDO OU NÃO
                    if (self.atacando == True and self.atacando_contador > 0):
                        self.sprite_atual = pygame.transform.flip(self.sprite_atacando, True, False)
                        self.atacando_contador -= 1

                    elif (self.atacando_contador <= 0):
                        self.atacando_contador = 20
                        self.atacando = False

                    else:
                        self.sprite_atual = pygame.transform.flip(self.sprites_andando[int(self.contador_inimigo)], True, False)

                else:

                    #VERIFICA SE O INIMIGO ESTÁ ATACANDO OU NÃO
                    if (self.atacando == True and self.atacando_contador > 0):
                        self.sprite_atual = self.sprite_atacando
                        self.atacando_contador -= 1

                    elif (self.atacando_contador <= 0):
                        self.atacando_contador = 20
                        self.atacando = False

                    else:
                        self.sprite_atual = self.sprites_andando[int(self.contador_inimigo)]

                pos_x = self.pos[0] + (self.colisao.width / 2) - (self.sprite_atual.get_width() / 2)
                pos_y = self.pos[1] + 13

                if self.atacando == True:
                    self.screen.blit(self.sprite_atual, (pos_x, pos_y - 20))

                else:
                    self.screen.blit(self.sprite_atual, (pos_x, pos_y))

            # Lógica da Barra de Vida Flutuante
            indice_sprite = 3 - self.vida
            if 0 <= indice_sprite <= 2:
                sprite = self.sprites_vida[indice_sprite]

                # Centraliza a barra acima do inimigo
                pos_x = self.pos[0] + (self.colisao.width / 2) - (sprite.get_width() / 2)
                pos_y = self.pos[1] - 60 
                
                self.screen.blit(sprite, (pos_x, pos_y))
                
    def aplicar_paralax(self, deslocamento):
        self.pos[0] += deslocamento
        self.colisao.x = self.pos[0]

class Inimigo_Longa_Distancia(Entidade):
    def __init__(self, pos, screen, vida):
        super().__init__(pos)
        self.screen = screen
        self.vida = vida