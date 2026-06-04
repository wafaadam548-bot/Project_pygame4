import pygame as pg
import random as random
pg.init()
clock=pg.time.Clock()
dice_value = 1
rolling = False
roll_start_time = 0
class Questions:
    def __init__(self):
        pass
class Screen:
    def __init__(self , width, height):
        self.width=width
        self.height=height
        self.screen=pg.display.set_mode((width,height))
class Background:
    def __init__(self):
        self.board=pg.image.load("images/board.png")
        self.board =pg.transform.scale(self.board, (1000, 500))
        self.rect=self.board.get_rect(midbottom=(500,500))
class Player2:
    def __init__(self):
        self.image=pg.image.load("images/player2.png")
        self.image=pg.transform.scale(self.image,(100,100))
        self.rect=self.image.get_rect(midbottom=(150,110 ))
class Player:
    def __init__(self):
        self.image=(pg.image.load("images/player.png"))
        self.image=pg.transform.scale(self.image,(100,100))
        self.rect=self.image.get_rect(midbottom=(110,110 ))
    black=(0,0,0)
    white=(225,225,225)
    x,y=(100,100)
screen = Screen(1000, 500)
player=Player()
player2=Player2()
board=Background()
black=(0,0,0)
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()#tell python to shut down all the pygame moudel 
            exit()#telling python to stop running the entire file
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_SPACE:
                rolling=True
                roll_start_time=pg.time.get_ticks()
    screen.screen.blit(board.board,board.rect)
    screen.screen.blit(player.image,player.rect)
    screen.screen.blit(player2.image,player2.rect)
    pg.draw.rect(screen.screen,black, (900,50,70,70))
    key =pg.key.get_pressed()
    if key[pg.K_RIGHT]:
        player.rect.x+=10
    if key[pg.K_LEFT]:
        player.rect.x-=10
    if key[pg.K_DOWN]:
        player.rect.y+=4
    if key[pg.K_UP]:
        player.rect.y-=4
    #the same for player2
    if key[pg.K_d]:
        player2.rect.x+=4
    if key[pg.K_a]:
        player2.rect.x-=4
    if key[pg.K_s]:
        player2.rect.y+=4
    if key[pg.K_w]:
        player2.rect.y-=4      
    pg.display.update()
    clock.tick(60)#Consistent Game Speed
