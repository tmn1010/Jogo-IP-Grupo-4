#IMPORTANDO OS MÓDULOS A SEREM UTILIZADOS
import pygame
import random
from pygame.locals import *
import sys
import constantes as cst
from entities import Player, Inimigo_Corpo_a_Corpo, Boss

#INICIA O PYGAME
pygame.init()

#INICIA O MIXER DO PYGAME PARA TOCAR SONS
pygame.mixer.init()

class Game:

    def __init__(self):

        #DEFINE A TELA E UM RELÓGIO
        self.screen = pygame.display.set_mode((cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        #DEFINE SONS
        self.som_catraca_girando = pygame.mixer.Sound('Assets/Sons/som_catraca_girando.wav')
        self.som_pegou_coletavel = pygame.mixer.Sound('Assets/Sons/som_pegou_coletavel.wav')
        self.som_moeda = pygame.mixer.Sound('Assets/Sons/som_moeda.wav')
        self.som_pegou_coletavel.set_volume(0.8)
        self.ost_principal = pygame.mixer.music.load('Assets/Sons/ostprincipal.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        #DEFINE VARIÁVEIS INICIAIS
        self.tela_anterior = None
        self.tela_atual = None
        self.tela_x = None
        self.estado = 'jogando'

        #DEFINE UMA FONTE
        self.fonte = pygame.font.Font(None, 50)

        #DEFINE UM CHÃO
        self.plataformas = [
            pygame.Rect(0, 700, 1800, 160)
        ]

        #OBJETOS PARA NÃO SAIR DA TELA
        self.limite_esquerdo = pygame.Rect(-10, 0, 10, 800)
        self.limite_direito = pygame.Rect(1360, 0, 10, 800)

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

        #IMAGEM DO MENU
        self.tela_menu = pygame.transform.scale(pygame.image.load('Assets/Cenários/Tela-menu.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #IMAGEM DA TELA 1 - TUTORIAL
        self.tela_tutorial = pygame.transform.scale(pygame.image.load('Assets/Cenários/Tela-Tutorial.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #IMAGEM DA TELA 2 - CORREDOR INFINITO
        self.tela_corredor_infinito = pygame.transform.scale(pygame.image.load('Assets/Cenários/Corredor-Infinito.png'), (7123, 800))

        #IMAGEM DA TELA 3 - GRAD5
        self.tela_grad5 = pygame.transform.scale(pygame.image.load('Assets/Cenários/grad5.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #IMAGEM DA TELA 4 - LABORATÓRIO DE HARDWARE
        self.tela_labhardware = pygame.transform.scale(pygame.image.load('Assets/Cenários/LabHardware.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))
        
        #IMAGEM DA TELA 5 - LANFITEATRO
        self.tela_anfiteatro = pygame.transform.scale(pygame.image.load('Assets/Cenários/Anfiteatro.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #IMAGEM DA TELA 6 - CRÉDITOS
        self.tela_creditos = pygame.transform.scale(pygame.image.load('Assets/Cenários/Creditos.png'), (cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))

        #SPRITE DO CHÃO
        self.chao = pygame.transform.scale(pygame.image.load('Assets/Ambiente/chao.png'), (cst.SCREEN_WIDTH, 200))

        #SPRITE DO CHÃO DA SEGUNDA TELA
        self.chao2 = pygame.transform.scale(pygame.image.load('Assets/Ambiente/chao_tela2.png'), (10400, 200))

        #SPRITE DO CRACHÁ
        self.cracha = [
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_00.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_01.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_02.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_03.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_04.png'), (90, 90)),
        pygame.transform.scale(pygame.image.load('Assets/Coletáveis/cracha_05.png'), (90, 90))
        ]

        #SPRITE DOS BOTÕES C
        self.animacoes_botao_C = [
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_00.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_01.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_02.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_03.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_04.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_05.png'), (128, 128))
        ]

        #SPRITE DA CABEÇA DE STEFAN
        self.cabeca_stefan = [
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/stefan1.png'), (140, 140)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/stefan2.png'), (140, 140))
        ]

        #SPRITE DA SETA PARA BAIXO
        self.seta_baixo = [
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_00.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_01.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_02.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_03.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_04.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_05.png'), (200, 200))
            ]

        #SPRITE DOS BOTÕES C
        self.animacoes_botao_C = [
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_00.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_01.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_02.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_03.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_04.png'), (128, 128)),
            pygame.transform.scale(pygame.image.load('Assets/Sprite_botoes/botao_C_05.png'), (128, 128))
        ]

        #SPRITE DA CABEÇA DE STEFAN
        self.cabeca_stefan = [
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/stefan1.png'), (140, 140)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/stefan2.png'), (140, 140))
        ]

        #SPRITE DA SETA PARA BAIXO
        self.seta_baixo = [
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_00.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_01.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_02.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_03.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_04.png'), (200, 200)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/seta_baixo_05.png'), (200, 200))
            ]

        # Sprites da barra de vida do inimigo
        self.sprites_vida_inimigo = [
            pygame.transform.scale(pygame.image.load('Assets/Inimigo/vida_inimigo_00.png'), (200, 100)), # 0 dano
            pygame.transform.scale(pygame.image.load('Assets/Inimigo/vida_inimigo_01.png'), (200, 100)), # 1 dano
            pygame.transform.scale(pygame.image.load('Assets/Inimigo/vida_inimigo_02.png'), (200, 100))  # 2 danos
        ]

    def MenuInicial(self):

        while True:
            #DESENHA A TELA DO MENU
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
        mensagens_tutorial = [
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/tutorial_00.png'), (700, 210)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/tutorial_01.png'), (700, 210)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/tutorial_02.png'), (700, 210)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/tutorial_03.png'), (700, 210))
        ]

        #SPRITE DA CATRACA
        catraca = pygame.transform.scale(pygame.image.load('Assets/Ambiente/catraca1.png'), (150, 150))
        
        #OBJETO DE COLISÃO DA CATRACA
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
            self.screen.blit(catraca, (1100, 560))

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
                                self.Reiniciar(player)

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
                                return self.CorredorInfinito(0)

                    player.processar_evento(event)

            #SOMADOR QUE FAZ A ANIMAÇÃO DE STEFAN
            self.contagem_frames_stefan += 0.1

            #FAZ UM LOOP NOS SPRITES DA CABEÇA DE STEFAN
            if self.contagem_frames_stefan >= len(self.cabeca_stefan):
                self.contagem_frames_stefan = 0

            #INICIA AS MENSAGENS DO TUTORIAL
            if self.contagem_tutorial > 2 and self.contagem_tutorial < 6:
                
                #SOMADOR QUE FAZ A ANIMAÇÃO DA SETA
                self.contagem_frames_seta += 0.2

                #FAZ UM LOOP NOS SPRITES DA SETA
                if self.contagem_frames_seta >= len(self.seta_baixo):
                    self.contagem_frames_seta = 0

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

                #DESENHA A PRIMEIRA MENSAGEM
                self.screen.blit(mensagens_tutorial[0], (350, 35))

                #DESENHA A SETA
                self.screen.blit(self.seta_baixo[int(self.contagem_frames_seta)], (player.pos[0] - 45, player.pos[1] - 130))

            #SEGUNDA MENSAGEM
            if self.contagem_tutorial > 6 and self.contagem_tutorial < 12:

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

                self.screen.blit(mensagens_tutorial[1], (350, 35))

            #TERCEIRA MENSAGEM
            if self.contagem_tutorial > 12 and self.contagem_tutorial < 18:

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

            
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
                if self.contagem_frames_seta >= len(self.seta_baixo):
                    self.contagem_frames_seta = 0

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

                self.screen.blit(mensagens_tutorial[3], (350, 35))
                self.screen.blit(self.seta_baixo[int(self.contagem_frames_seta)], (cracha_obj.x - 50, cracha_obj.y - 110))

                #COLISÃO COM O CRACHÁ:
                if (player.colisao.colliderect(cracha_obj)):
                    cracha_obj = None
                    self.som_pegou_coletavel.play()
                    cracha_coletado = True

            if (player.colisao.colliderect(transicao_1_2) and cracha_coletado):
                self.contagem_frames_botoes += 0.3
                if self.contagem_frames_botoes > len(self.animacoes_botao_C):
                    self.contagem_frames_botoes = 0
                self.screen.blit(self.animacoes_botao_C[int(self.contagem_frames_botoes)], (1120, 450))

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
            
            #COLISÃO COM O LIMITE ESQUERDO
            if (player.colisao.left <= self.limite_esquerdo.right):
                player.vel_x = 0
                player.pos[0] = 0
                player.colisao.x = player.pos[0]

            #COLISÃO COM O LIMITE DIREITO
            if (player.colisao.right >= self.limite_direito.left):
                player.vel_x = 0
                player.pos[0] = 1200
                player.colisao.x = player.pos[0]

            #DESENHA O JOGADOR
            if self.estado == 'jogando':
                player.desenhar()

            #VERIFICA SE O JOGADOR MORREU
            if player.vida <= 0:
                return self.Reiniciar(player)

            #ATUALIZA A TELA
            pygame.display.update()

            #TICK NO RELÓGIO
            self.clock.tick(60)

    #SALA ONDE OCORRERÁ O CAMINHO ATÉ O BOSS
    def CorredorInfinito(self, tela_x, vida=3, especial=0, desbloqueou_pulo_duplo=False, desbloqueou_dash=False):
        self.tela_x = tela_x

        #DEFINE O OBJETO DO PLAYER
        player = Player((50, 510), self.screen, vida, especial)
        player.desbloqueou_pulo_duplo = desbloqueou_pulo_duplo
        player.desbloqueou_dash = desbloqueou_dash

        # Prepara a lista de inimigos e um timer para spawn
        lista_inimigos = []
        timer_spawn = 60 # Começa em 60 frames (1 segundo) para o primeiro inimigo aparecer

        #OBJETO E VARIAVEL NECESSÁRIOS PARA REALIZAR O PARALAX
        obj_paralax = pygame.Rect(650, 0, 1, 900)
        self.paralax = False

        #MENSAGENS DAS PORTAS
        mensagem_porta1 = pygame.transform.scale(pygame.image.load('Assets/Mensagens/gradmensagem.png'), (700, 210))
        mensagem_porta2 = pygame.transform.scale(pygame.image.load('Assets/Mensagens/labhardwaremensagem.png'), (700, 210))
        mensagem_porta3 = pygame.transform.scale(pygame.image.load('Assets/Mensagens/anfiteatromensagem.png'), (700, 210))


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
                                self.Reiniciar(player)

                            #ENCERRA O JOGO
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                #JOGADOR VIVO
                elif self.estado == 'jogando':

                    player.processar_evento(event)

            #CRIANDO O OBJETO DAS PORTAS - ELES SE MOVEM CONFORME O PARALAX PARA CHEGAR AO PLAYER
            porta1 = pygame.Rect(1317 + self.tela_x, 122, 300, 678)
            porta2 = pygame.Rect(3684 + self.tela_x, 122, 300, 678)
            porta3 = pygame.Rect(5835 + self.tela_x, 122, 300, 678)

            #SOMADOR QUE FAZ A ANIMAÇÃO DE STEFAN
            self.contagem_frames_stefan += 0.1

            #FAZ UM LOOP NOS SPRITES DA CABEÇA DE STEFAN
            if self.contagem_frames_stefan >= len(self.cabeca_stefan):
                self.contagem_frames_stefan = 0

            self.screen.fill((0,0,0))

            #DESENHA NA TELA O CENÁRIO
            self.screen.blit(self.tela_corredor_infinito, (self.tela_x, 0))

            #DESENHA O CHÃO
            self.screen.blit(self.chao2, (self.tela_x, 710))

            #DESATIVA O PARALAX NO INÍCIO
            if (self.tela_x >= 0 and self.paralax == True):
                self.paralax = False
                self.tela_x = 0
                player.semparalax(-8)

            #ATIVA O PARALAX NO INÍCIO
            if (player.colisao.right == obj_paralax.left):
                self.paralax = True
                player.emparalax()

            #DESATIVA O PARALAX NO FIM DA TELA
            if (self.tela_x <= -5823 and self.paralax == True):
                self.paralax = False
                self.tela_x = -5823
                player.semparalax(+8)

            #ATIVA O PARALAX NO FIM DA TELA
            if (player.colisao.colliderect(obj_paralax)):
                self.paralax = True
                player.emparalax()

            #PARALAX PARA A DIREITA
            if (pygame.key.get_pressed()[K_d] and self.paralax == True and self.estado == 'jogando'):

                self.tela_x -= 8
                
                for ini in lista_inimigos:
                    ini.aplicar_paralax(-8)

            if player.state == 'dash' and player.andando_direita and self.paralax == True:
                self.tela_x -= 25

                for ini in lista_inimigos:
                    ini.aplicar_paralax(-25)

            #PARALAX PARA A ESQUERDA
            if (pygame.key.get_pressed()[K_a] and self.paralax == True and self.estado == 'jogando'):
                
                self.tela_x += 8

                for ini in lista_inimigos:
                    ini.aplicar_paralax(8)

            if player.state == 'dash' and not player.andando_direita and self.paralax == True:
                self.tela_x += 25

                for ini in lista_inimigos:
                    ini.aplicar_paralax(25)

            #ATUALIZA A ANIMAÇÃO CONFORME O EVENTO
            if self.estado == 'jogando':
                player.atualizar_animacao()
                player.movimento()
                
                #LÓGICA DE SPAWN ALEATÓRIO
                timer_spawn -= 1
                if timer_spawn <= 0:
                    # Cria o inimigo fora da tela na direita (posição X: 1400)
                    novo_inimigo = Inimigo_Corpo_a_Corpo([1400, 530], self.screen, self.sprites_vida_inimigo)
                    lista_inimigos.append(novo_inimigo)
                    
                    # Sorteia um tempo para o próximo inimigo
                    timer_spawn = random.randint(180, 240)
                
                # Atualizar os dados dos inimigos
                for ini in lista_inimigos[:]: 
                    ini.atualizar(player, self.plataformas)

                    # Verifica se o soco do player ou o especial acertou este inimigo
                    if player.hitbox_atq is not None and ini.vida > 0 and ini.invulnerabilidade == 0:
                        if player.hitbox_atq.colliderect(ini.colisao):
                            ini.vida -= 1
                            ini.invulnerabilidade = cst.INVULNERAVEL_INIMIGO
                            ini.tomoudano = True
                    
                    if player.hitbox_atq_especial is not None and ini.vida > 0 and ini.invulnerabilidade == 0:
                        if player.hitbox_atq_especial.colliderect(ini.colisao):
                            ini.vida -= 1
                            ini.invulnerabilidade = cst.INVULNERAVEL_INIMIGO
                            ini.tomoudano = True
                    
                    # Verifica se este inimigo encostou no player
                    if ini.vida > 0 and player.invulnerabilidade == 0:
                        if ini.colisao.colliderect(player.colisao):
                            player.vida -= 1
                            player.invulnerabilidade = cst.INVULNERAVEL
                            player.som_dano.play()

                            #MODIFICA O SPRITE DO INIMIGO
                            ini.atacando = True
                            ini.atacou = True
                    
                    # Remove o inimigo da lista se ele morrer (Limpa a memória do jogo!)
                    if ini.vida <= 0:
                        lista_inimigos.remove(ini)

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

            #PRIMEIRA PORTA
            if (player.colisao.colliderect(porta1)):

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

                #DESENHA A PRIMEIRA MENSAGEM
                self.screen.blit(mensagem_porta1, (350, 35))

                if (pygame.key.get_pressed()[K_c]):
                    player.semparalax(0)
                    self.paralax = False
                    self.valor_salvo_tela_x = self.tela_x
                    return self.Grad5(player.vida, player.especial, player.desbloqueou_pulo_duplo, player.desbloqueou_dash)

            #SEGUNDA PORTA
            if (player.colisao.colliderect(porta2)):

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

                #DESENHA A PRIMEIRA MENSAGEM
                self.screen.blit(mensagem_porta2, (350, 35))

                if (pygame.key.get_pressed()[K_c]):
                    player.semparalax(0)
                    self.paralax = False
                    self.valor_salvo_tela_x = self.tela_x
                    return self.LabHardware(player.vida, player.especial, player.desbloqueou_pulo_duplo, player.desbloqueou_dash)

            #TERCEIRA PORTA
            if (player.colisao.colliderect(porta3)):   

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

                #DESENHA A PRIMEIRA MENSAGEM
                self.screen.blit(mensagem_porta3, (350, 35))

                if (pygame.key.get_pressed()[K_c]):
                    player.semparalax(0)
                    self.paralax = False
                    self.valor_salvo_tela_x = self.tela_x
                    return self.Anfiteatro(player.vida, player.especial, player.desbloqueou_pulo_duplo, player.desbloqueou_dash)

            #COLISÃO COM O LIMITE ESQUERDO
            if (player.colisao.left <= self.limite_esquerdo.right):
                player.vel_x = 0
                player.pos[0] = 0
                player.colisao.x = player.pos[0]

            #COLISÃO COM O LIMITE DIREITO
            if (player.colisao.right >= self.limite_direito.left):
                player.vel_x = 0
                player.pos[0] = 1200
                player.colisao.x = player.pos[0]

            #DESENHA O JOGADOR
            if self.estado == 'jogando':
                player.desenhar()
                for ini in lista_inimigos:
                    ini.desenhar()

            #VERIFICA SE O JOGADOR MORREU
            if player.vida <= 0:
                return self.Reiniciar(player)

            #ATUALIZA A TELA
            pygame.display.update()

            #TICK NO RELÓGIO
            self.clock.tick(60)

    def Grad5(self, vida=3, especial=0, desbloqueou_pulo_duplo=False, desbloqueou_dash=False):
        msg_grad05 = pygame.transform.scale(pygame.image.load('Assets/Mensagens/tutorial_grad05.png'), (700, 210))

        #Mudei o sprite do pulo duplo, e deixei o que estava antes como o dash
        self.sprite_powerup_pulo_duplo = pygame.transform.scale(pygame.image.load('Assets/Coletáveis/powerup_pulo_duplo.png'), (74, 74))
        self.colisao_powerup = pygame.Rect(1000, 600, 74, 74)

        self.colisao_voltar_corredor = pygame.Rect(1290, 500, 100, 100)

        #DEFINE O OBJETO DO PLAYER
        player = Player((100, 510), self.screen, vida, especial)
        player.desbloqueou_pulo_duplo = desbloqueou_pulo_duplo
        player.desbloqueou_dash = desbloqueou_dash

        while True:

            #DEFINE A TELA ATUAL
            self.tela_atual == 'Grad5'

            #DESENHA NA TELA O CENÁRIO
            self.screen.blit(self.tela_grad5, (0, 0))

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
                                self.Reiniciar(player)

                            #ENCERRA O JOGO
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                #JOGADOR VIVO
                elif self.estado == 'jogando':

                    player.processar_evento(event)
            
            #DESENHA A MENSAGEM DE TUTORIAL
            self.screen.blit(msg_grad05, (350, 35))

            #SOMADOR QUE FAZ A ANIMAÇÃO DE STEFAN
            self.contagem_frames_stefan += 0.1

            #FAZ UM LOOP NOS SPRITES DA CABEÇA DE STEFAN
            if self.contagem_frames_stefan >= len(self.cabeca_stefan):
                self.contagem_frames_stefan = 0

            #DESENHA A CABEÇA DE STEFAN
            self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))
            
            #DESENHA OU NÃO O POWERUP
            if player.colisao.colliderect(self.colisao_powerup) and not player.desbloqueou_pulo_duplo :
                self.som_pegou_coletavel.play()
                player.desbloqueou_pulo_duplo = True
            
            if player.desbloqueou_pulo_duplo == False:
                self.screen.blit(self.sprite_powerup_pulo_duplo, (1000, 600))

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
            
            #VOLTA PARA O CORREDOR INFINITO
            if player.colisao.colliderect(self.colisao_voltar_corredor):
                return self.CorredorInfinito(self.valor_salvo_tela_x, player.vida, player.especial, player.desbloqueou_pulo_duplo, player.desbloqueou_dash)

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

            #COLISÃO COM O LIMITE ESQUERDO
            if (player.colisao.left <= self.limite_esquerdo.right):
                player.vel_x = 0
                player.pos[0] = 0
                player.colisao.x = player.pos[0]

            #COLISÃO COM O LIMITE DIREITO
            if (player.colisao.right >= self.limite_direito.left):
                player.vel_x = 0
                player.pos[0] = 1200
                player.colisao.x = player.pos[0]
            
            #DESENHA O JOGADOR
            if self.estado == 'jogando':
                player.desenhar()

            #VERIFICA SE O JOGADOR MORREU
            if player.vida <= 0:
                return self.Reiniciar(player)

            #ATUALIZA A TELA
            pygame.display.update()

            #TICK NO RELÓGIO
            self.clock.tick(60)

    def LabHardware(self, vida=3, especial=0, desbloqueou_pulo_duplo=False, desbloqueou_dash=False):
        msg_labhardware = pygame.transform.scale(pygame.image.load('Assets/Mensagens/tutorial_labhardware.png'), (700, 210))

        self.sprite_powerup_dash = pygame.transform.scale(pygame.image.load('Assets/Coletáveis/powerup_dash.png'), (74, 74))
        self.colisao_powerup = pygame.Rect(1000, 600, 74, 74)

        self.colisao_voltar_corredor = pygame.Rect(1290, 500, 100, 100)

        #DEFINE O OBJETO DO PLAYER
        player = Player((100, 510), self.screen, vida, especial)
        player.desbloqueou_pulo_duplo = desbloqueou_pulo_duplo
        player.desbloqueou_dash = desbloqueou_dash

        while True:

            #DEFINE A TELA ATUAL
            self.tela_atual == 'LabHardware'

            #DESENHA NA TELA O CENÁRIO
            self.screen.blit(self.tela_labhardware, (0, 0))

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
                                self.Reiniciar(player)

                            #ENCERRA O JOGO
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                #JOGADOR VIVO
                elif self.estado == 'jogando':

                    player.processar_evento(event)
                
            #DESENHA A MENSAGEM DE TUTORIAL
            self.screen.blit(msg_labhardware, (350, 35))

            #SOMADOR QUE FAZ A ANIMAÇÃO DE STEFAN
            self.contagem_frames_stefan += 0.1

            #FAZ UM LOOP NOS SPRITES DA CABEÇA DE STEFAN
            if self.contagem_frames_stefan >= len(self.cabeca_stefan):
                self.contagem_frames_stefan = 0

            #DESENHA A CABEÇA DE STEFAN
            self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

            #DESENHA OU NÃO O POWERUP
            if player.colisao.colliderect(self.colisao_powerup) and not player.desbloqueou_dash :
                self.som_pegou_coletavel.play()
                player.desbloqueou_dash = True

            if player.desbloqueou_dash == False:
                self.screen.blit(self.sprite_powerup_dash, (1000, 600))

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

            #VOLTA PARA O CORREDOR INFINITO
            if player.colisao.colliderect(self.colisao_voltar_corredor):
                return self.CorredorInfinito(self.valor_salvo_tela_x, player.vida, player.especial, player.desbloqueou_pulo_duplo, player.desbloqueou_dash)

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

            #COLISÃO COM O LIMITE ESQUERDO
            if (player.colisao.left <= self.limite_esquerdo.right):
                player.vel_x = 0
                player.pos[0] = 0
                player.colisao.x = player.pos[0]

            #COLISÃO COM O LIMITE DIREITO
            if (player.colisao.right >= self.limite_direito.left):
                player.vel_x = 0
                player.pos[0] = 1200
                player.colisao.x = player.pos[0]
            
            #DESENHA O JOGADOR
            if self.estado == 'jogando':
                player.desenhar()

            #VERIFICA SE O JOGADOR MORREU
            if player.vida <= 0:
                return self.Reiniciar(player)

            #ATUALIZA A TELA
            pygame.display.update()

            #TICK NO RELÓGIO
            self.clock.tick(60)

    def Anfiteatro(self, vida=3, especial=0, desbloqueou_pulo_duplo=False, desbloqueou_dash=False):
        msg_anfiteatro = pygame.transform.scale(pygame.image.load('Assets/Mensagens/tutorial_anfiteatro.png'), (700, 210))

        self.sprite_especial_carga1 = pygame.transform.scale(pygame.image.load('Assets/Coletáveis/coletavel_semaforo.png'), (74, 74))
        self.colisao_carga1 = self.sprite_especial_carga1.get_rect(topleft = (900, 600))
        self.coletou_carga1 = False

        self.sprite_especial_carga2 = pygame.transform.scale(pygame.image.load('Assets/Coletáveis/coletavel_semaforo.png'), (74, 74))
        self.colisao_carga2 = self.sprite_especial_carga2.get_rect(topleft = (1000, 600))
        self.coletou_carga2 = False

        self.sprite_especial_carga3 = pygame.transform.scale(pygame.image.load('Assets/Coletáveis/coletavel_semaforo.png'), (74, 74))
        self.colisao_carga3 = self.sprite_especial_carga3.get_rect(topleft = (1100, 600))
        self.coletou_carga3 = False

        #VARIÁVEIS QUE CRIAM AS MENSAGENS DO BOSS
        contagem_frames_humberto = 0
        contagem_boss = 0

        #SPRITE DA CABEÇA DE HUMBERTO
        cabeca_humberto = [
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('Assets/Mensagens/humberto.png'), (150, 150)), True, False),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('Assets/Mensagens/humberto2.png'), (150, 150)), True, False)

        ]

        #SPRITE DA CABEÇA DA VIRGINIANA
        cabeca_virginiana = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Assets/Mensagens/virginiana.png'), (130, 130)), True, False)


        #MENSAGENS
        mensagens_boss = [
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/boss1.png'), (700, 210)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/boss2.png'), (700, 210)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/boss3.png'), (700, 210)),
            pygame.transform.scale(pygame.image.load('Assets/Mensagens/boss4.png'), (700, 210))
        ]

        #DEFINE O OBJETO DO PLAYER
        player = Player((100, 510), self.screen, vida, especial)
        player.desbloqueou_pulo_duplo = desbloqueou_pulo_duplo
        player.desbloqueou_dash = desbloqueou_dash

        #VERIFICA SE O BOSS ESTÁ VIVO
        boss_morto = False
        boss_spawnou = False

        while True:

            #DEFINE A TELA ATUAL
            self.tela_atual == 'Anfiteatro'

            #DESENHA NA TELA O CENÁRIO
            self.screen.blit(self.tela_anfiteatro, (0, 0))

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
                                self.Reiniciar(player)

                            #ENCERRA O JOGO
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                #JOGADOR VIVO
                elif self.estado == 'jogando':

                    player.processar_evento(event)


            #DESENHA OU NÃO AS CARGAS
            if player.colisao.colliderect(self.colisao_carga1):
                player.especial += 1
                self.colisao_carga1.top = 700 #Deixa o retângulo da carga abaixo do chão, impedindo mais de uma colisão
                self.coletou_carga1 = True
                self.som_pegou_coletavel.play()

            if self.coletou_carga1 == False:
                self.screen.blit(self.sprite_especial_carga1, self.colisao_carga1)
            
            if player.colisao.colliderect(self.colisao_carga2):
                player.especial += 1
                self.colisao_carga2.top = 700 #Deixa o retângulo da carga abaixo do chão, impedindo mais de uma colisão
                self.coletou_carga2 = True
                self.som_pegou_coletavel.play()

            if self.coletou_carga2 == False:
                self.screen.blit(self.sprite_especial_carga2, self.colisao_carga2)
            
            if player.colisao.colliderect(self.colisao_carga3):
                player.especial += 1
                self.colisao_carga3.top = 700 #Deixa o retângulo da carga abaixo do chão, impedindo mais de uma colisão
                self.coletou_carga3 = True
                self.som_pegou_coletavel.play()

            if self.coletou_carga3 == False:
                self.screen.blit(self.sprite_especial_carga3, self.colisao_carga3)

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

            #DESENHA O TUTORIAL DESTA SALA
            if (self.coletou_carga3 == False):
                #DESENHA A MENSAGEM DE TUTORIAL
                self.screen.blit(msg_anfiteatro, (350, 35))

                #SOMADOR QUE FAZ A ANIMAÇÃO DE STEFAN
                self.contagem_frames_stefan += 0.1

                #FAZ UM LOOP NOS SPRITES DA CABEÇA DE STEFAN
                if self.contagem_frames_stefan >= len(self.cabeca_stefan):
                    self.contagem_frames_stefan = 0

                #DESENHA A CABEÇA DE STEFAN
                self.screen.blit(self.cabeca_stefan[int(self.contagem_frames_stefan)], (1040, 106))

            #VERIFICA SE TODAS AS CARGA FORAM COLETADAS
            if (self.coletou_carga3 == True):
                
                contagem_boss += 0.05

                #SOMADOR QUE FAZ A ANIMAÇÃO DE HUMBERTO
                contagem_frames_humberto += 0.1

                #FAZ UM LOOP NOS SPRITES DA CABEÇA DE HUMBERTO
                if contagem_frames_humberto >= len(cabeca_humberto):
                    contagem_frames_humberto = 0

                #INICIA AS MENSAGENS DO BOSS
                if contagem_boss > 2 and contagem_boss < 10:

                    #DESENHA A CABEÇA DE VIRGINIANA
                    self.screen.blit(cabeca_virginiana, (1060, 112))
                    
                    #DESENHA A PRIMEIRA MENSAGEM
                    self.screen.blit(mensagens_boss[0], (350, 35))


                #SEGUNDA MENSAGEM
                if contagem_boss > 10 and contagem_boss < 18:

                    #DESENHA A CABEÇA DE HUMBERTO
                    self.screen.blit(cabeca_humberto[int(contagem_frames_humberto)], (1040, 100))

                    self.screen.blit(mensagens_boss[1], (350, 35))

                #TERCEIRA MENSAGEM
                if contagem_boss > 18 and contagem_boss < 26:

                    #DESENHA A CABEÇA DE VIRGINIANA
                    self.screen.blit(cabeca_virginiana, (1060, 112))
                
                    self.screen.blit(mensagens_boss[2], (350, 35))

                #QUARTA MENSAGEM
                if contagem_boss > 26 and contagem_boss < 34:

                    #DESENHA A CABEÇA DE HUMBERTO
                    self.screen.blit(cabeca_humberto[int(contagem_frames_humberto)], (1040, 100))
                
                    self.screen.blit(mensagens_boss[3], (350, 35))

                #SPAWN DO BOSS
                if contagem_boss > 34:

                    if boss_morto == False:

                        #SPAWNA O BOSS APENAS UMA VEZ
                        if boss_spawnou == False:

                            #DEFINE A BOSS
                            boss = Boss([1000, 530], self.screen, self.sprites_vida_inimigo)
                            boss_spawnou = True

                        boss.atualizar(player, self.plataformas)

                        # Verifica se o soco do player acertou este inimigo
                        if player.hitbox_atq is not None and boss.vida > 0 and boss.invulnerabilidade == 0:
                            if player.hitbox_atq.colliderect(boss.colisao):
                                boss.vida -= 1
                                boss.invulnerabilidade = cst.INVULNERAVEL_INIMIGO
                                boss.tomoudano = True
                        
                        # Verifica se este inimigo encostou no player
                        if boss.vida > 0 and player.invulnerabilidade == 0:
                            if boss.colisao.colliderect(player.colisao):
                                player.vida -= 1
                                player.invulnerabilidade = cst.INVULNERAVEL
                                player.som_dano.play()

                                #MODIFICA O SPRITE DO INIMIGO
                                boss.atacando = True
                                boss.atacou = True
                        
                        # Remove o inimigo da lista se ele morrer (Limpa a memória do jogo!)
                        if boss.vida <= 0:
                            boss_morto = True
                            return self.Creditos()

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
            
            #COLISÃO COM O LIMITE ESQUERDO
            if (player.colisao.left <= self.limite_esquerdo.right):
                player.vel_x = 0
                player.pos[0] = 0
                player.colisao.x = player.pos[0]

            #COLISÃO COM O LIMITE DIREITO
            if (player.colisao.right >= self.limite_direito.left):
                player.vel_x = 0
                player.pos[0] = 1200
                player.colisao.x = player.pos[0]

            #DESENHA O JOGADOR
            if self.estado == 'jogando':
                player.desenhar()

                if (boss_spawnou):
                    boss.desenhar()

            #VERIFICA SE O JOGADOR MORREU
            if player.vida <= 0:
                return self.Reiniciar(player)

            #ATUALIZA A TELA
            pygame.display.update()

            #TICK NO RELÓGIO
            self.clock.tick(60)

    def Creditos(self):

            while True:

                #DEFINE A TELA ATUAL
                self.tela_atual == 'Créditos'

                #DESENHA NA TELA O CENÁRIO
                self.screen.blit(self.tela_creditos, (0, 0))

                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.quit()
                        exit()

                pygame.display.update()

    #Mensagem de game over
    def desenhar_game_over(self, player):
        if player.desbloqueou_pulo_duplo :
            pulo_duplo_txt = "PULO DUPLO - Encontrado"
        else :
            pulo_duplo_txt = "PULO DUPLO - Não encontrado"
        if player.desbloqueou_dash :
            dash_txt = "DASH - Encontrado"
        else :
            dash_txt = "DASH - Não encontrado"
        cargas_txt = f"CARGAS - {player.especial}"
        self.screen.blit(self.fonte.render(pulo_duplo_txt, True, (255, 255, 255)), (400, 360))
        self.screen.blit(self.fonte.render(dash_txt, True, (255, 255, 255)), (400, 420))
        self.screen.blit(self.fonte.render(cargas_txt, True, (255, 255, 255)), (400, 480))

    def Reiniciar(self, player):
            # Carrega a imagem da tela de derrota
            self.tela_perdeu = pygame.transform.scale(pygame.image.load('Assets/Cenários/Tela_de_Derrota.png'), (1300, 800))

            while True:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:

                            player.pos = [100, 500]
                            player.colisao.x = 100
                            player.colisao.y = 500
                            self.estado = 'jogando'
                            self.paralax = False

                            player.vida = 3
                            player.especial = 0
                            player.desbloqueou_pulo_duplo = False
                            player.desbloqueou_dash = False
                            player.vel_x = 0
                            player.vel_y = 0
                            player.invulnerabilidade = 0
                            player.semparalax(-8)

                            return self.CorredorInfinito(0, 3, 0, False, False)

                self.screen.blit(self.tela_perdeu, (0, 0))

                #Botar o relatório
                self.desenhar_game_over(player)

                pygame.display.update()

game = Game()
game.MenuInicial()