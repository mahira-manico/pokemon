import pygame

#screen size
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720

#color repertory
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(200,0,0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
YELLOW=(255, 255, 0)
MAGENTA=(255, 0, 255)
CYAN=(0, 255, 255)
SKY_BLUE=(135, 206, 235)
ORANGE=(255, 165, 0)
FOREST_GREEN=(34, 139, 34)
CRIMSON=(220, 20, 60)
GOLD=(255, 215, 0)

#font sizes
SMALL=20
MEDIUM=40
LARGE=70

pygame.font.init()
FONT1=pygame.font.Font("assets/fonts/bold_pokemon.ttf",45)
FONT2=pygame.font.Font("assets/fonts/solid_pokemon.ttf",SMALL)