import pygame
import sys
import constantes as cst
from entities import Player
from entities import Moeda
from entities import Espinho

pygame.init()
pygame.mixer.init()

class Game:

    def __init__(self):

        #DEFINE UMA TELA
        self.screen = pygame.display.set_mode((cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #DEFINE UM RELÓGIO
        self.clock = pygame.time.Clock()

        #DEFINE UM CONTADOR
        self.contagem_frames = 0

        self.tela_anterior = None
        self.tela_atual = 'menu inicial'

        self.estado = 'jogando'

        self.fonte = pygame.font.Font(None, 50)

        self.plataformas = [
            pygame.Rect(0, 800, 1800, 160), #Chão
        ]

        self.msg = pygame.transform.scale(pygame.image.load('Assets/mensagem_inicial.png'), (1500, 512))

        self.tela_menu = pygame.transform.scale(pygame.image.load('Assets/Tela inicial.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        self.tela_tutorial = pygame.transform.scale(pygame.image.load('Assets/cin_frente.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        self.chao = pygame.transform.scale(pygame.image.load('Assets/chao.png'), (cst.SCREEN_WIDTH, 200))

    def MenuInicial(self):

        while True:
            self.screen.blit(self.tela_menu, (0, 0))
            self.screen.blit(self.msg, (150, 500))
            pygame.display.update()

            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        return self.TelaTutorial()
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    def TelaTutorial(self):

        player = Player((100, 600), self.screen, 3)

        while True:

            #Ordem de ações para fazer as telas:
            #1: Desenhar o cenário e o chão (se tiver plataformas é só botar la na lista do self.plataformas pra adicionar as colisões delas) e quando forem checar a
            # colisão com o boneco, só vc botar self.plataformas[indice:indice] pra determinar quais colisões serão consideradas naquela tela específica

            #2: Atualizar as informações do jogador se ele ainda não tiver morrido

            #3: Checar as colisões com as plataformas (chão incluso)

            #4: Por fim desenhar o player e no final de tudo ver se ele morre para chamar a função reiniciar(), que coloca o player de volta na primeira tela do jogo

            #Observações:
            #Se forem adicionar alguma constante nova, modifiquem o arquivo constantes.py, e para usar essa constante em outros arquivos é só usar 'cst.(nome da constante)'
            #Para criar os coletáveis é só ir no arquivo entities.py, criar uma nova classe que herda da classe Entidade(que tem apenas posição e colisão) e adicionar atributos que serão necessários
            #Pedro Alves pra tu fazer as mudanças de sprites pode ir na entites.py na classe Player e ir no método de atualizar_animacao() que la é onde tudo acontece

            self.screen.fill((0, 0, 0))

            self.screen.blit(self.tela_tutorial, (0, 0))
            self.screen.blit(self.chao, (0, 800))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.estado == 'Game over':
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                self.reiniciar(player)

                elif self.estado == 'jogando':
                    player.processar_evento(event)

            if self.estado == 'jogando':
                player.atualizar_animacao()
                player.movimento()

            if player.invulnerabilidade > 0:
                player.invulnerabilidade -= 1

            player.no_chao = False

            player.atualizar_vida()

            if player.cooldown_atq > 0:
                player.cooldown_atq -= 1

            #Ver a colisão do pé do personagem e só considerar ela para ver se ele está em cima de uma plataforma
            for plataforma in self.plataformas:
                pe_anterior = player.y_anterior + player.colisao.height
                pe_atual = player.colisao.bottom

                #Isso vê se o personagem está exatamente em cima da plataforma analisando as bordas dos sprites
                if player.colisao.right > plataforma.left and player.colisao.left < plataforma.right and pe_anterior <= plataforma.top and pe_atual >= plataforma.top and player.vel_y >= 0:
                    player.vel_y = 0
                    player.pos[1] = plataforma.top - player.colisao.height
                    player.colisao.y = player.pos[1]
                    player.no_chao = True
                    player.pulo_duplo = True
                    break

            if self.estado == 'jogando':
                player.desenhar()

            if player.vida <= 0:
                self.estado = 'Game over'
                texto = self.fonte.render("GAME OVER - Aperte R para reiniciar", True, (255, 255, 255))
                self.screen.blit(texto, (400, 300))
            pygame.display.update()
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