import pygame as pg
import random as random
pg.init()
clock=pg.time.Clock()
font=pg.font.Font("Font/Archivo_Black/ArchivoBlack-Regular.ttf",30)
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
        self.board =pg.transform.scale(self.board, (1000, 500))#resize the game board
        self.rect=self.board.get_rect(midbottom=(500,500))
class Player2:
    def __init__(self):
        self.image=pg.image.load("images/player2.png")#upload the player image
        self.image=pg.transform.scale(self.image,(100,100))#resize the game image
        self.rect=self.image.get_rect(midbottom=(150,110 ))
class Player:
    def __init__(self):
        self.image=(pg.image.load("images/player.png"))#upload the player image 
        self.image=pg.transform.scale(self.image,(100,100))#resize the image
        self.rect=self.image.get_rect(midbottom=(110,110 ))
    black=(0,0,0)
    white=(225,225,225)
    x,y=(100,100)
class Dice:
    def __init__(self):
        self.dice_value = 1
        self.rolling = False
        self.roll_start_time = 0
        self.dice_rolling_images=[]
        self.dice_images=[]
        self.dice_roling_counter=0
        self.roll_duration=1000 
        for num in range(1,7):
            self.dice_image=pg.image.load("images/dice/"+str(num)+".png")
            self.dice_images.append(self.dice_image)
        self.dice_num_image=self.dice_images[0]
        for dice in range(1,9):
            self.dice_rolling_image=pg.image.load("images/animation/roll"+str(dice)+".png")
            self.dice_rolling_images.append(self.dice_rolling_image)
    def trigger_roll(self):
        if self.rolling is False:
            self.rolling = True
            self.roll_start_time = pg.time.get_ticks()
    def  draw(self,target_screen):
        if self.rolling:
            self.current_time = pg.time.get_ticks()
            if self.current_time - self.roll_start_time < self.roll_duration:
                self.dice_roling_counter = (pg.time.get_ticks() // 100) % len(self.dice_rolling_images)
                target_screen.blit(self.dice_rolling_images[self.dice_roling_counter], (900, 60))
            else:
                self.rolling = False
                self.rand_num = random.randint(0, 5)
                self.dice_num_image = self.dice_images[self.rand_num]
                target_screen.blit(self.dice_num_image, (900, 60))
        else:
            target_screen.blit(self.dice_num_image, (900, 60))
screen = Screen(1000, 500)
player=Player()
player2=Player2()
board=Background()
black=(0,0,0)
dice=Dice()
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()#tell python to shut down all the pygame moudel 
            exit()#telling python to stop running the entire file
        if event.type==pg.KEYDOWN:
            
            dice.trigger_roll()                   
             #show the dicewhich contains a numers
    #display the board, player1, and player2 
    screen.screen.blit(board.board,board.rect)
    screen.screen.blit(player.image,player.rect)
    screen.screen.blit(player2.image,player2.rect)
    
    
    pg.draw.rect(screen.screen,black, (900,50,70,70))
    key =pg.key.get_pressed()
    #set the movement for the first player
    if key[pg.K_RIGHT]:
        player.rect.x+=4
    if key[pg.K_LEFT]:
        player.rect.x-=4
    if key[pg.K_DOWN]:
        player.rect.y+=4
    if key[pg.K_UP]:
        player.rect.y-=4
    #set movment for player2
    if key[pg.K_d]:
        player2.rect.x+=4
    if key[pg.K_a]:
        player2.rect.x-=4
    if key[pg.K_s]:
        player2.rect.y+=4
    if key[pg.K_w]:
        player2.rect.y-=4  
    dice.draw(screen.screen)
    pg.display.update()
    clock.tick(60)#Consistent Game Speed
    #draw 60 frame per second
