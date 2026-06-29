#IMPORTANDO OS MÓDULOS A SEREM UTILIZADOS
import pygame
from pygame.locals import *
import sys
import constantes as cst
from entities import Player

#INICIA O PYGAME
pygame.init()

#INICIA O MIXER DO PYGAME PARA TOCAR SONS
pygame.mixer.init()

class Game:

    def __init__(self):

        #DEFINE A TELA E UM RELÓGIO
        self.screen = pygame.display.set_mode((cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        #DEFINE UM CONTADOR PARA AS MENSAGENS DO TUTORIAL
        self.contagem_tutorial = 0

        #DEFINE UM CONTADOR DE FRAMES QUE SERÁ UTILIZADO PARA ANIMAÇÕES
        self.contagem_frames = 0

        #DEFINE UM CONTADOR DE FRAMES QUE SERÁ UTILIZADO PARA FAZER AS ANIMAÇÕES DOS BOTÕES DO TUTORIAL
        self.contagem_frames_botoes = 0

        #DEFINE UM CONTADOR PARA A ANIMAÇÃO DA SETA DO TUTORIAL
        self.contagem_frames_seta = 0

        #DEFINE UM CONTADOR DE FRAMES QUE SERÁ UTILIZADO PARA FAZER AS ANIMAÇÕES DO CRACHA
        self.contagem_frames_cracha = 0

        #DEFINE UM CONTADOR DE FRAMES QUE SERÁ UTILIZADO PARA FAZER AS ANIMAÇÕES DE STEFAN
        self.contagem_frames_stefan = 0 

        self.som_catraca_girando = pygame.mixer.Sound('Assets/Sons/som_catraca_girando.wav')
        self.som_pegou_cracha = pygame.mixer.Sound('Assets/Sons/som_pegou_cracha.wav')
        self.som_pegou_cracha.set_volume(0.3)

        #DEFINE VARIÁVEIS INICIAIS
        self.tela_anterior = None
        self.tela_atual = None
        self.estado = 'jogando'

        #DEFINE UMA FONTE
        self.fonte = pygame.font.Font(None, 50)

        #DEFINE UM CHÃO
        self.plataformas = [
            pygame.Rect(0, 700, 1800, 160)
        ]

        self.tela_x = None

        #IMAGEM DO MENU
        self.tela_menu = pygame.transform.scale(pygame.image.load('Assets/Cenários/Tela-menu.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #IMAGEM DA TELA 2 - TUTORIAL
        self.tela_tutorial = pygame.transform.scale(pygame.image.load('Assets/Cenários/Tela-Tutorial.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #IMAGEM DA TELA 2 - CORREDOR INFINITO
        self.tela_corredor_infinito = pygame.transform.scale(pygame.image.load('Assets/Cenários/Corredor-Infinito.png'), (7123, 800))

        #SPRITE DO CHÃO
        self.chao = pygame.transform.scale(pygame.image.load('Assets/Ambiente/chao.png'), (cst.SCREEN_WIDTH, 200))

        #SPRITE DO CHÃO DA TELA 2
        self.chao2 = pygame.transform.scale(pygame.image.load('Assets/Ambiente/chao_tela2.png'), (9000, 200))

        #SPRITE DA CATRACA
        self.catraca = pygame.transform.scale(pygame.image.load('Assets/Ambiente/catraca1.png'), (150, 150))

        #SPRITE DO CRACHÁ
        self.cracha = [
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_00.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_01.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_02.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_03.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_04.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_05.png'), (90, 90))
        ]

    def MenuInicial(self):

        while True:
            self.screen.blit(self.tela_menu, (0, 0))
            pygame.display.update()

            self.clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        return self.TelaTutorial()
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    def TelaTutorial(self):

        #DEFINE OS SPRITES QUE SERÃO UTILIZADOS NAS ANIMAÇÕES
        animacoes_botao_C = [
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_00.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_01.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_02.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_03.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_04.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_05.png'), (128, 128))
        ]

        mensagens_tutorial = [
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/tutorial_00.png'), (700, 256)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/tutorial_01.png'), (700, 256)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/tutorial_02.png'), (700, 256)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/tutorial_03.png'), (700, 256))
        ]

        seta_baixo = [
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/seta_baixo_00.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/seta_baixo_01.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/seta_baixo_02.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/seta_baixo_03.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/seta_baixo_04.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/seta_baixo_05.png'), (200, 200))
            ]
        
        cabeca_stefan = [
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/stefan1.png'), (140, 140)),
            pygame.transform.scale(pygame.image.load('Assets/Tutorial/stefan2.png'), (140, 140))
        ]

        #OBJETO DE COLISÃO PARA A PRÓXIMA FASE
        transicao_1_2 = pygame.Rect(1100, 560, 150, 150)

        #OBJETO DO CRACHÁ
        cracha_coletado = False

        #DEFINE O OBJETO DO PLAYER
        player = Player((100, 510), self.screen, 3, 0)

        while True:

            #DEFINE A TELA ATUAL
            self.tela_atual == 'Tela Tutorial'

            #DESENHA NA TELA O CENÁRIO
            self.screen.blit(self.tela_tutorial, (0, 0))

            #DESENHA O OBJETO DE COLISÃO
            self.screen.blit(self.catraca, (1100, 560))

            #DESENHA O CHÃO
            self.screen.blit(self.chao, (0, 710))

            self.contagem_tutorial += 0.017

            #VERIFICA EVENTOS
            for event in pygame.event.get():

                #EVENTO DE SAÍDA
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #JOGADOR MORREU
                if self.estado == 'Game over':
                        
                        if event.type == pygame.KEYDOWN:

                            #REINICIA O JOGO
                            if event.key == pygame.K_r:
                                self.reiniciar(player)

                            #ENCERRA O JOGO
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                #JOGADOR VIVO
                elif self.estado == 'jogando':

                    #COLISÃO COM A CATRACA PARA O PRÓXIMO ESTÁDO
                    if (player.colisao.colliderect(transicao_1_2)):

                        if (event.type == pygame.KEYDOWN):

                            #AVANÇA PARA A PRÓXIMA FASE CASO PASSE O CRACHÁ NA CATRACA
                            if (event.key == pygame.K_c) and (cracha_coletado == True):
                                self.som_catraca_girando.play()
                                return self.CorredorInfinito()

                    player.processar_evento(event)

            #SOMADOR QUE FAZ A ANIMAÇÃO DE STEFAN
            self.contagem_frames_stefan += 0.1

            #FAZ UM LOOP NOS SPRITES DA CABEÇA DE STEFAN
            if self.contagem_frames_stefan >= len(cabeca_stefan):
                self.contagem_frames_stefan = 0

            #INICIA AS MENSAGENS DO TUTORIAL
            if self.contagem_tutorial > 2 and self.contagem_tutorial < 6:
                
                #SOMADOR QUE FAZ A ANIMAÇÃO DA SETA
                self.contagem_frames_seta += 0.2

                #FAZ UM LOOP NOS SPRITES DA SETA
                if self.contagem_frames_seta >= len(seta_baixo):
                    self.contagem_frames_seta = 0

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 145))

                #DESENHA A PRIMEIRA MENSAGEM
                self.screen.blit(mensagens_tutorial[0], (350, 35))

                #DESENHA A SETA
                self.screen.blit(seta_baixo[int(self.contagem_frames_seta)], (player.pos[0] - 45, player.pos[1] - 130))

            #SEGUNDA MENSAGEM
            if self.contagem_tutorial > 6 and self.contagem_tutorial < 12:

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 145))

                self.screen.blit(mensagens_tutorial[1], (350, 35))

            #TERCEIRA MENSAGEM
            if self.contagem_tutorial > 12 and self.contagem_tutorial < 18:

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 145))

            
                self.screen.blit(mensagens_tutorial[2], (350, 35))

            #CRIAR O CRACHÁ QUANDO AS MENSAGENS DE TUTORIAL NÃO ACABAREM
            if self.contagem_tutorial > 18 and cracha_coletado == False:
                cracha_obj = pygame.Rect(950, 580, 90, 90)

                #DESENHA O CRACHÁ CASO ELE NÃO TENHA SIDO COLETADO
                if (cracha_coletado == False):
                    self.contagem_frames_cracha += 0.1
                    if self.contagem_frames_cracha >= len(self.cracha):
                        self.contagem_frames_cracha = 0
                    self.screen.blit(self.cracha[int(self.contagem_frames_cracha)], (950, 580))

                self.contagem_frames_seta += 0.2
                if self.contagem_frames_seta >= len(seta_baixo):
                    self.contagem_frames_seta = 0

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 145))

                self.screen.blit(mensagens_tutorial[3], (350, 35))
                self.screen.blit(seta_baixo[int(self.contagem_frames_seta)], (cracha_obj.x - 50, cracha_obj.y - 110))

                #COLISÃO COM O CRACHÁ:
                if (player.colisao.colliderect(cracha_obj)):
                    cracha_obj = None
                    self.som_pegou_cracha.play()
                    cracha_coletado = True

            if (player.colisao.colliderect(transicao_1_2) and cracha_coletado):
                self.contagem_frames_botoes += 0.3
                if self.contagem_frames_botoes > len(animacoes_botao_C):
                    self.contagem_frames_botoes = 0
                self.screen.blit(animacoes_botao_C[int(self.contagem_frames_botoes)], (1120, 450))

            #ATUALIZA A ANIMAÇÃO CONFORME O EVENTO
            if self.estado == 'jogando':
                player.atualizar_animacao()
                player.movimento()

            #CONTADOR PARA O PLAYER NÃO LEVAR DANO INFINITO
            if player.invulnerabilidade > 0:
                player.invulnerabilidade -= 1

            player.no_chao = False

            #DESENHA A VIDA NA TELA
            player.atualizar_vida()

            #DESENHA A BARRA DE ESPECIAL
            player.atualizar_especial()

            #CONTADOR PARA NÃO TER ATAQUE INFINITO
            if player.cooldown_atq > 0:
                player.cooldown_atq -= 1

            #VERIFICA A COLISÃO DO PERSONAGEM
            for plataforma in self.plataformas:
                pe_anterior = player.y_anterior + player.colisao.height
                pe_atual = player.colisao.bottom

                #VERIFICA SE O PLAYER ESTÁ EXATAMENTE EM CIMA DA PLATAFORMA
                if player.colisao.right > plataforma.left and player.colisao.left < plataforma.right and pe_anterior <= plataforma.top and pe_atual >= plataforma.top and player.vel_y >= 0:
                    player.vel_y = 0
                    player.pos[1] = plataforma.top - player.colisao.height
                    player.colisao.y = player.pos[1]
                    player.no_chao = True
                    player.pulo_duplo = True
                    break
            
            #DESENHA O JOGADOR
            if self.estado == 'jogando':
                player.desenhar()

            #VERIFICA SE O JOGADOR MORREU
            if player.vida <= 0:
                self.estado = 'Game over'
                texto = self.fonte.render("GAME OVER - Aperte R para reiniciar", True, (255, 255, 255))
                self.screen.blit(texto, (400, 300))

            #ATUALIZA A TELA
            pygame.display.update()

            #TICK NO RELÓGIO
            self.clock.tick(60)

    #SALA ONDE OCORRERÁ O CAMINHO ATÉ O BOSS
    def CorredorInfinito(self):

        #DEFINE O OBJETO DO PLAYER
        player = Player((50, 510), self.screen, 3, 0)

        #OBJETO E VARIAVEL NECESSÁRIO PARA REALIZAR O PARALAX
        obj_paralax = pygame.Rect(650, 0, 1, 900)
        paralax = False

        self.tela_x = 0

        while True:

            #VERIFICA EVENTOS
            for event in pygame.event.get():

                #EVENTO DE SAÍDA
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #JOGADOR MORREU
                if self.estado == 'Game over':
                        
                        if event.type == pygame.KEYDOWN:

                            #REINICIA O JOGO
                            if event.key == pygame.K_r:
                                self.reiniciar(player)

                            #ENCERRA O JOGO
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                #JOGADOR VIVO
                elif self.estado == 'jogando':

                    player.processar_evento(event)

            self.screen.fill((0,0,0))

            #DESENHA NA TELA O CENÁRIO
            self.screen.blit(self.tela_corredor_infinito, (self.tela_x, 0))

            #DESENHA O CHÃO
            self.screen.blit(self.chao2, (self.tela_x, 710))

            #DESATIVA O PARALAX NO INÍCIO
            if (self.tela_x >= 0 and paralax == True):
                paralax = False
                self.tela_x = 0
                player.semparalax(-8)

            #ATIVA O PARALAX NO INÍCIO
            if (player.colisao.right == obj_paralax.left):
                paralax = True
                player.emparalax()

            #DESAATIVA O PARALAX NO FIM DA TELA
            if (self.tela_x <= -5823 and paralax == True):
                paralax = False
                self.tela_x = -5823
                player.semparalax(+8)

            #ATIVA O PARALAX NO FIM DA TELA
            if (player.colisao.colliderect(obj_paralax)):
                paralax = True
                player.emparalax()

            #PARALAX PARA A DIREITA
            if (pygame.key.get_pressed()[K_d] and paralax == True):

                self.tela_x -= 8

            if player.state == 'dash' and player.andando_direita and paralax == True:
                self.tela_x -= 25

            #PARALAX PARA A ESQUERDA
            if (pygame.key.get_pressed()[K_a] and paralax == True):
                
                self.tela_x += 8

            if player.state == 'dash' and not player.andando_direita and paralax == True:
                self.tela_x += 25

            #ATUALIZA A ANIMAÇÃO CONFORME O EVENTO
            if self.estado == 'jogando':
                player.atualizar_animacao()
                player.movimento()

            #CONTADOR PARA O PLAYER NÃO LEVAR DANO INFINITO
            if player.invulnerabilidade > 0:
                player.invulnerabilidade -= 1

            player.no_chao = False

            #DESENHA A VIDA NA TELA
            player.atualizar_vida()

            #DESENHA BARRA DE ESPECIAL NA TELA
            player.atualizar_especial()

            #CONTADOR PARA NÃO TER ATAQUE INFINITO
            if player.cooldown_atq > 0:
                player.cooldown_atq -= 1

            #VERIFICA A COLISÃO DO PERSONAGEM
            for plataforma in self.plataformas:
                pe_anterior = player.y_anterior + player.colisao.height
                pe_atual = player.colisao.bottom

                #VERIFICA SE O PLAYER ESTÁ EXATAMENTE EM CIMA DA PLATAFORMA
                if player.colisao.right > plataforma.left and player.colisao.left < plataforma.right and pe_anterior <= plataforma.top and pe_atual >= plataforma.top and player.vel_y >= 0:
                    player.vel_y = 0
                    player.pos[1] = plataforma.top - player.colisao.height
                    player.colisao.y = player.pos[1]
                    player.no_chao = True
                    player.pulo_duplo = True
                    break
            
            #DESENHA O JOGADOR
            if self.estado == 'jogando':
                player.desenhar()

            #VERIFICA SE O JOGADOR MORREU
            if player.vida <= 0:
                self.estado = 'Game over'
                texto = self.fonte.render("GAME OVER - Aperte R para reiniciar", True, (255, 255, 255))
                self.screen.blit(texto, (400, 300))

            #ATUALIZA A TELA
            pygame.display.update()

            #TICK NO RELÓGIO
            self.clock.tick(60)

    def Reiniciar(self, player):
            player.pos = [100, 500]
            player.colisao.x = 100
            player.colisao.y = 500

            player.vida = 3
            player.especial = 0
            player.vel_x = 0
            player.vel_y = 0
            player.contagem_moeda = 0
            player.invulnerabilidade = 0

            return self.TelaTutorial()

game = Game()
game.MenuInicial()