import pygame as pg
import random as random
import sys
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
    def gride(self):
        self.tile=[]
        self.start_X=101
        self.start_Y=390
        self.tile_width=81
        self.tile_height=81
        for row in range(6):
            for col in range(10):
                if row % 2 == 0:
                    x = self.start_X + col * self.tile_width
                else:
                    x = self.start_X + (9 - col) * self.tile_width
                y = self.start_Y - row * self.tile_height
                self.tile.append((x, y))
class Player:
    def __init__(self,image,position,up,down ,left, right ):
        self.image=pg.image.load(image)#upload the player image
        self.image=pg.transform.scale(self.image,(80,80))#resize the game image
        self.rect=self.image.get_rect(midbottom=position)
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.current_square = 0
    black=(0,0,0)
    white=(225,225,225)
    x,y=(100,100)
    def move(self,key):

        if key[self.right]:
            self.rect.x+=4
        if key[self.left]:
            self.rect.x-=4
        if key[self.up]:
            self.rect.y+=4
        if key[self.down]:
            self.rect.y-=4
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
        for dice in range(1, 9):
            self.dice_rolling_image = pg.image.load(
                "images/animation/roll" + str(dice) + ".png"
            )
            self.dice_rolling_images.append(self.dice_rolling_image)
    def trigger_roll(self):
        if self.rolling is False:
            self.rolling = True
            self.roll_start_time = pg.time.get_ticks()
    def draw(self, target_screen):
        current_time = pg.time.get_ticks()

        if self.rolling:
            if current_time - self.roll_start_time < self.roll_duration:

                self.dice_roling_counter = (
                    current_time // 100
                ) % len(self.dice_rolling_images)

                target_screen.blit(
                    self.dice_rolling_images[self.dice_roling_counter],
                    (900, 60)
                )

            else:
                self.rolling = False

                self.rand_num = random.randint(1, 6)

                global current_player, game

                if current_player == 1:
                    player1.current_square += self.rand_num
                    if player1.current_square >= len(board.tile):
                        player1.current_square = len(board.tile) - 1
                    current_player = 2

                else:
                    player2.current_square += self.rand_num
                    if player2.current_square >= len(board.tile):
                        player2.current_square = len(board.tile) - 1
                    current_player = 1

                self.dice_num_image = self.dice_images[self.rand_num - 1]

        target_screen.blit(self.dice_num_image, (900, 60))
screen = Screen(1000, 500)
show_menu = True
show_instructions = False
python_game=False
game=False

player2=Player(("images/player2.png"),(100,110),   
                pg.K_DOWN,pg.K_UP, pg.K_LEFT, pg.K_RIGHT
)
player1=Player(("images/player.png"),(150,110),  
                pg.K_s,pg.K_w, pg.K_a, pg.K_d
)
board = Background()
board.gride()
black=(0,0,0)
dice=Dice()
current_player = 1

game_state = "MENU" 

instructions = [
    "GAME INSTRUCTIONS",
    "",
    "1. Press SPACE to roll the dice.",
    "2. Players take turns automatically.",
    "3. Move forward according to the number rolled.",
    "4. Some squares contain questions.",
    "5. Answer the question correctly.",
    "6. Some squares are traps!",
    "7. Traps may send you backward.",
    "8. Reach the final square to win.",
    "9. First player to reach the finish wins.",
    "10. Press ESC to return to Menu."
]

def winner():
    if player1.current_square==len(board.tile) - 1:
        screen.screen.fill((100,23,129))
        player1_win = pg.transform.scale(player1.image,(200,200))
        rect = player1_win.get_rect(midbottom=(500,250))
        screen.screen.blit(player1_win, rect)
        winning=font.render("Congratulations! Player 1 is the winner!",True,(255,255,255))
        screen.screen.blit(winning,(150,300))

    elif player2.current_square==len(board.tile) - 1 :
        screen.screen.fill((100,23,129))
        player2_win = pg.transform.scale(player2.image,(200,200)) 
        rect = player2_win.get_rect(midbottom=(500,250))
        screen.screen.blit(player2_win, rect)
        winning=font.render("Congratulations! Player 2 is the winner!",True,(255,255,255))
        screen.screen.blit(winning,(150,300))
    
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()#tell python to shut down all the pygame moudel 
            sys.exit()#telling python to stop running the entire file
            
        if event.type==pg.KEYDOWN:
            if game_state == "MENU":
                if event.key==pg.K_RSHIFT or event.key==pg.K_LSHIFT:
                    game=True
                    game_state = "PLAYING"
                elif event.key==pg.K_i:
                    game_state = "INSTRUCTIONS"
                    
            elif game_state == "INSTRUCTIONS":
                if event.key==pg.K_ESCAPE:
                    game_state = "MENU"   
            elif game_state == "PLAYING":
                if event.key==pg.K_SPACE:
                    dice.trigger_roll()  
                if event.key==pg.K_ESCAPE:
                    game_state = "MENU"
                    game = False
    if game_state == "MENU":
        screen.screen.fill((200, 200, 200)) 
        start=font.render("Hellow to Python game !",True,(34,54,21))
        options=font.render("Press'I' for instruction or Shift to Start",True,(34,54,21))
        screen.screen.blit(start, (300, 180))
        screen.screen.blit(options, (250, 260))
        Player1=pg.transform.scale(player1.image,(200,200))
        screen.screen.blit(Player1,player1.rect)
        Player2=pg.transform.scale(player2.image,(200,200))
        player2.rect=player2.image.get_rect(midbottom=(100,280))
        screen.screen.blit(Player2,player2.rect)


    elif game_state == "INSTRUCTIONS":
        screen.screen.fill((200, 200, 200))
        for i, line in enumerate(instructions):
            text = font.render(line, True, (0, 0, 0))
            screen.screen.blit(text, (50, 30 + i * 35))    
    elif game_state == "PLAYING" or game == True:
        #display the board, player1, and player2 
        screen.screen.blit(board.board,board.rect)
        screen.screen.blit(player1.image,player1.rect)
        screen.screen.blit(player2.image,player2.rect)
        screen.screen.blit(player1.image, player1.rect)
        screen.screen.blit(player2.image, player2.rect)
        pg.draw.rect(screen.screen,black, (900,50,70,70))
        x1, y1 = board.tile[player1.current_square]
        player1.rect.topleft = (x1 - 3, y1 - 20)
        x2, y2 = board.tile[player2.current_square]
        player2.rect.topleft = (x2 + 17, y2 - 16)
        dice.draw(screen.screen) #show the dicewhich contains a numers
        winner()
        
    pg.display.update()
    clock.tick(60)#Consistent Game Speed
    #draw 60 frame per second