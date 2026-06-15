import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Imagens do cenário
BACKGROUND_INICIAL = pygame.image.load("cin-pixel.png")
BACKGROUND = pygame.transform.scale(BACKGROUND_INICIAL, (SCREEN_WIDTH, SCREEN_HEIGHT-100))
GROUND_INICIAL = pygame.image.load("ground.png")
GROUND = pygame.transform.scale(GROUND_INICIAL, (SCREEN_WIDTH, SCREEN_HEIGHT-500))

#Imagens do personagem
FIGURA_PARADA = pygame.transform.scale(pygame.image.load("parado.png"), (96, 112)).convert_alpha()
FIGURA_PULANDO = pygame.transform.scale(pygame.image.load("pulo.png"), (96, 112)).convert_alpha()
FIGURA_CORRENDO = pygame.transform.scale(pygame.image.load("correndo.png"), (96, 112)).convert_alpha()
FIGURA_ATACANDO = pygame.transform.scale(pygame.image.load("atacando.png"), (96, 112)).convert_alpha()
sprite_invertido = pygame.transform.flip(FIGURA_CORRENDO, True, False)

fonte = pygame.font.SysFont("Arial", 28)

def tela_menu():
   pygame.display.set_caption("Menu Inicial")
   while True:

       for evento in pygame.event.get():
           if evento.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
      
       key = pygame.key.get_pressed()
       if key[pygame.K_RETURN]:
           return "jogo"       
          
       screen.fill((30, 30, 30))
       texto = fonte.render("HUMBERTO ADVENTURE - APERTE ENTER PARA JOGAR", True, (255, 255, 255))
       screen.blit(texto, (30, 250))
      
       pygame.display.update()
       clock.tick(60)

def tela_jogo1():
   pygame.display.set_caption("Tutorial")
   posicao_x = 20
   posicao_y = 480
  
   player = FIGURA_PARADA.get_rect(center=(posicao_x, posicao_y))

   direita = False
   esquerda = False
   ataque = False
   pulando = False
   Y_GRAVIDADE = 1
   ALTURA_PULO = 18
   Y_VELOCIDADE = ALTURA_PULO
  
   while True:

       for evento in pygame.event.get():
           if evento.type == pygame.QUIT:
               pygame.quit()
               sys.exit()

       screen.blit(BACKGROUND, (0, 0))
       screen.blit(GROUND, (0, 500))

       key = pygame.key.get_pressed()
       if key[pygame.K_SPACE]:
           pulando = True
       elif key[pygame.K_a]:
           player.move_ip(-5, 0)
           movimento = True
           esquerda = True
       elif key[pygame.K_d]:
           player.move_ip(5, 0)
           movimento = True
           direita = True
       elif key[pygame.K_x]:
           ataque = True
       elif key[pygame.K_ESCAPE]:
           return "menu"
      
       if pulando:
           player.y -= Y_VELOCIDADE
           Y_VELOCIDADE -= Y_GRAVIDADE
           if Y_VELOCIDADE < -ALTURA_PULO:
               pulando = False
               Y_VELOCIDADE = ALTURA_PULO
           screen.blit(FIGURA_PULANDO, player)
       else:
           if direita:
               screen.blit(FIGURA_CORRENDO, player)
           elif esquerda:
               screen.blit(sprite_invertido, player)
           elif ataque:
               screen.blit(FIGURA_ATACANDO, player)
           else:
               screen.blit(FIGURA_PARADA, player)

       direita = False
       esquerda = False
       ataque = False

       pygame.display.update()
       clock.tick(60)

estado_atual = "menu"

while True:
   if estado_atual == "menu":
       estado_atual = tela_menu()
   elif estado_atual == "jogo":
       estado_atual = tela_jogo1()