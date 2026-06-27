#IMPORTANDO OS MÓDULOS A SEREM UTILIZADOS
import pygame
import sys
import constantes as cst
from entities import Player
from entities import Moeda
from entities import Espinho

#INICIA O PYGAME
pygame.init()

#INICIA O MIXER DO PYGAME PARA TOCAR SONS
pygame.mixer.init()

class Game:

    def __init__(self):

        #DEFINE A TELA E UM RELÓGIO
        self.screen = pygame.display.set_mode((cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        #DEFINE UM CONTADOR DE FRAMES QUE SERÁ UTILIZADO PARA COOLDOWN
        self.contagem_frames = 0

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

        #IMAGEM DO MENO
        self.tela_menu = pygame.transform.scale(pygame.image.load('Assets/Cenários/Tela-menu.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #IMAGEM DO TUTORIAL
        self.tela_tutorial = pygame.transform.scale(pygame.image.load('Assets/Cenários/Tela-Tutorial.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #SPRITE DO CHÃO
        self.chao = pygame.transform.scale(pygame.image.load('Assets/Ambiente/chao.png'), (cst.SCREEN_WIDTH, 200))

        #SPRITE DA CATRACA
        self.catraca = pygame.transform.scale(pygame.image.load('Assets/Ambiente/catraca1.png'), (150, 150))

        #SPRITE DO CRACHÁ
        self.cracha = pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha.png'), (90, 90))

    #ORDEM PARA ESCREVER OS CENÁRIOS
    #1: Desenhar o cenário e o chão (se tiver plataformas é só botar la na lista do self.plataformas pra adicionar as colisões delas) e quando forem checar a
    # colisão com o boneco, só vc botar self.plataformas[indice:indice] pra determinar quais colisões serão consideradas naquela tela específica.

    #2: Atualizar as informações do jogador se ele ainda não tiver morrido.

    #3: Checar as colisões com as plataformas (chão incluso)

    #4: Por fim desenhar o player e no final de tudo ver se ele morre para chamar a função reiniciar(), que coloca o player de volta na primeira tela do jogo

    #Observações:
    #Se forem adicionar alguma constante nova, modifiquem o arquivo constantes.py, e para usar essa constante em outros arquivos é só usar 'cst.(nome da constante)'
    #Para criar os coletáveis é só ir no arquivo entities.py, criar uma nova classe que herda da classe Entidade(que tem apenas posição e colisão) e adicionar atributos que serão necessários
    #Pedro Alves pra tu fazer as mudanças de sprites pode ir na entites.py na classe Player e ir no método de atualizar_animacao() que la é onde tudo acontece

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

        #OBJETO DE COLISÃO PARA A PRÓXIMA FASE
        transicao_1_2 = pygame.Rect(1100, 560, 150, 150)

        #OBJETO DO CRACHÁ
        cracha_obj = pygame.Rect(950, 580, 90, 90)
        cracha_coletado = False

        #DEFINE O OBJETO DO PLAYER
        player = Player((100, 510), self.screen, 3)

        while True:

            #DEFINE A TELA ATUAL
            self.tela_atual == 'Tela Tutorial'

            #DESENHA NA TELA O CENÁRIO
            self.screen.blit(self.tela_tutorial, (0, 0))

            #DESENHA O OBJETO DE COLISÃO
            self.screen.blit(self.catraca, (1100, 560))

            #DESENHA O CHÃO
            self.screen.blit(self.chao, (0, 710))

            #DESENHA O CRACHÁ CASO ELE NÃO TENHA SIDO COLETADO
            if (cracha_coletado == False):
                self.screen.blit(self.cracha, (950, 580))

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
                                return self.CorredorInfinito()
                            
                    #COLISÃO COM O CRACHÁ:
                    if (player.colisao.colliderect(cracha_obj)):
                        cracha_coletado = True

                    player.processar_evento(event)

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

        #OBJETO DE COLISÃO PARA A PRÓXIMA FASE
        transicao_1_2 = pygame.Rect(1150, 600, 50, 200)

        #DEFINE O OBJETO DO PLAYER
        player = Player((100, 510), self.screen, 3)


        while True:

            #DEFINE A TELA ATUAL
            self.tela_atual == 'Tela Tutorial'

            #DESENHA NA TELA O CENÁRIO
            self.screen.blit(self.tela_tutorial, (0, 0))

            #DESENHA O OBJETO DE COLISÃO
            pygame.draw.rect(self.screen, cst.AMARELO, transicao_1_2)

            #DESENHA O CHÃO
            self.screen.blit(self.chao, (0, 710))

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
                            if (event.key == pygame.K_c):
                                return self.CorredorInfinito()

                    player.processar_evento(event)

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

       

    def Tela_1(self):

        while True:
            self.screen.blit(self.chao, (0, 800))

    def Reiniciar(self, player):
            player.pos = [100, 500]
            player.colisao.x = 100
            player.colisao.y = 500

            player.vida = 3
            player.vel_x = 0
            player.vel_y = 0
            player.contagem_moeda = 0
            player.invulnerabilidade = 0

            self.moedas = [
                Moeda((865, 525), self.screen),
                Moeda((1215, 450), self.screen)
            ]

            return self.TelaTutorial()

game = Game()
game.MenuInicial()