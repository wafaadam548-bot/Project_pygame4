import pygame as pg
pg.init()
clock=pg.time.Clock()
class Screen:
    def __init__(self , width, height):
        self.width=width
        self.height=height
        self.screen=pg.display.set_mode((width,height))
class Background:
    def __init__(self):
        self.board=pg.image.load("image")
class Player2:
    def __init__(self):
        self.image=pg.image.load("images/player2.png")
        self.image=pg.transform.scale(self.image,(100,100))
        self.rect=self.image.get_rect(midbottom=(100,500 ))
class Player:
    def __init__(self):
        self.image=(pg.image.load("images/player1.png"))
        self.image=pg.transform.scale(self.image,(100,100))
        self.rect=self.image.get_rect(midbottom=(70,500 ))
screen = Screen(1000, 500)
player=Player()
player2=Player2()
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()#tell python to shut down all the pygame moudel 
            exit()#telling python to stop running the entire file
        screen.screen.blit(player.image,player.rect)
        screen.screen.blit(player2.image,player2.rect)
        pg.display.update()
        clock.tick(60)#Consistent Game Speed
