import pygame as pg
import random as random
import sys

pg.init()
clock = pg.time.Clock()
font = pg.font.Font("Font/Archivo_Black/ArchivoBlack-Regular.ttf", 30)

with open("Questions.txt", "r") as file:#read file
    raw = file.read().strip().split("---")#The code is divided into blocks, each block containing ---
    questions = []

    for block in raw:
        lines = block.split("\n")#split the block into lines
        if len(lines) >= 6:
            questions.append({
                "q": lines[0],#the question
                "a": lines[1],#option a
                "b": lines[2],#option b
                "c": lines[3],#option c 
                "d": lines[4],#obtion d 
                "correct": lines[5].lower() # last line represent the correct answer
            })
    print("Total questions:", len(questions))
req_questions = [2, 3, 7, 9, 11, 15, 23, 29, 35, 37, 42, 44, 46, 50, 51, 53, 56, 59]#the squares that have the questions
req_inc_money = [4, 5, 10, 16, 17, 20, 22, 24, 25, 28, 31, 35, 36, 38, 40, 47, 49, 54, 58, 60]
req_dec_score = [6, 18, 21, 26, 30, 34, 41, 45, 52, 57]

#Remove the square number so the computer can understand it.
questions_square = []
for sq in req_questions:
    questions_square.append(sq - 1)
inc_money = []
for sq in req_inc_money:
    inc_money.append(sq - 1)
dec_score = []
for sq in req_dec_score:
    dec_score.append(sq - 1)
#Vars
game_state = "MENU"
score1 = 0
score2 = 0
active_question = None
selected_answer = None
show_question = False
current_player = 1        
question_player = 1        

class Screen:
    def __init__(self, width, height):#method 1
        self.width = width#Atribute 1
        self.height = height
        self.screen = pg.display.set_mode((width, height))

class Background:
    def __init__(self):
        self.board = pg.image.load("images/board.png")
        self.board = pg.transform.scale(self.board, (1000, 500))
        self.rect = self.board.get_rect(midbottom=(500, 500))
        
    def gride(self):
        self.tile = []
        #first square bottom left
        self.start_X = 84   
        self.start_Y = 385
        self.tile_width = 83#the width for the square
        self.tile_height = 61#the height for the square
        for row in range(6):#6 rows
            row_tiles = []
            for col in range(10):#10 cols
                x = self.start_X + col * self.tile_width# for example self start width =84 col =1 self_tile_width=83 
                y = self.start_Y - row * self.tile_height
                row_tiles.append((x, y))
            if row % 2 != 0:#if the row is odd switsh the number so it start from right to left
                row_tiles.reverse()
            self.tile.extend(row_tiles)#discharge row_tiles in self.tile

class Player:
    def __init__(self, image, position, offset_x, offset_y):
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (60, 60))#resize the player
        self.rect = self.image.get_rect(topleft=position)
        self.current_square = 0#the square the player on it
        self.target_square = 0  #the square the player want to go to it 
        #if the 2 player in the same square one will be in the in the right and one in the left
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.move_delay = 200   #wiat 200 betwen the squaare and the square
        self.last_move_time = 0

    def update_movement(self, tiles):
        current_time = pg.time.get_ticks()
        if self.current_square < self.target_square:
            if current_time - self.last_move_time > self.move_delay:
                self.current_square += 1
                self.last_move_time = current_time
        elif self.current_square > self.target_square:
            if current_time - self.last_move_time > self.move_delay:
                self.current_square -= 1
                self.last_move_time = current_time
        
        x, y = tiles[self.current_square]
        self.rect.topleft = (x + self.offset_x, y - 5 + self.offset_y)

    def is_moving(self):
        return self.current_square != self.target_square

class Dice:
    def __init__(self):
        self.dice_value = 1
        self.rolling = False
        self.roll_start_time = 0
        self.dice_rolling_images = []
        self.dice_images = []
        self.dice_roling_counter = 0
        self.roll_duration = 1000 
        for num in range(1, 7):
            self.dice_images.append(pg.image.load("Images/dice/" + str(num) + ".png"))
        self.dice_num_image = self.dice_images[0]
        for dice in range(1, 9):
            self.dice_rolling_images.append(pg.image.load("Images/animation/roll" + str(dice) + ".png"))

    def trigger_roll(self):
        if not self.rolling and not show_question and not player1.is_moving() and not player2.is_moving(): 
            self.rolling = True
            self.roll_start_time = pg.time.get_ticks()

    def draw(self, target_screen):
        global score1, score2, current_player, show_question, active_question, question_player
        current_time = pg.time.get_ticks()
        
        if self.rolling:
            if current_time - self.roll_start_time < self.roll_duration:
                self.dice_roling_counter = (current_time // 100) % len(self.dice_rolling_images)
                target_screen.blit(self.dice_rolling_images[self.dice_roling_counter], (900, 30))
            else:
                self.rolling = False
                self.rand_num = random.randint(1, 6)
                
                question_player = current_player

                if current_player == 1:
                    player1.target_square += self.rand_num
                    if player1.target_square >= len(board.tile):
                        player1.target_square = len(board.tile) - 1
                    
                    if player1.target_square in inc_money: score1 += random.randint(1, 15)
                    if player1.target_square in dec_score: score1 -= random.randint(1, 10)
                    if player1.target_square in questions_square:
                        active_question = random.randint(0, len(questions) - 1)
                        show_question = True
                    
                    current_player = 2 
                else:
                    player2.target_square += self.rand_num
                    if player2.target_square >= len(board.tile):
                        player2.target_square = len(board.tile) - 1
                    
                    if player2.target_square in inc_money: score2 += random.randint(1, 15)
                    if player2.target_square in dec_score: score2 -= random.randint(1, 10)
                    if player2.target_square in questions_square:
                        active_question = random.randint(0, len(questions) - 1)
                        show_question = True
                            
                    current_player = 1 
                
                self.dice_num_image = self.dice_images[self.rand_num - 1]
                
        target_screen.blit(self.dice_num_image, (900, 30))

screen = Screen(1000, 500)

def display_score():
    score_image1 = font.render(f"P1: {score1}", False, "Black")
    screen.screen.blit(score_image1, score_image1.get_rect(center=(250, 35)))
    score_image2 = font.render(f"P2: {score2}", False, "Black")
    screen.screen.blit(score_image2, score_image2.get_rect(center=(700, 35)))

player1 = Player("Images/player.png", (84, 385), 0, 0)
player2 = Player("Images/player2.png", (84, 385), 26, 0)
board = Background()
board.gride()
dice = Dice()

instructions = [
    "GAME INSTRUCTIONS", "",
    "1. Press SPACE to roll the dice.",
    "2. Players take turns automatically.",
    "3. Move forward according to the number rolled.",
    "4. Some squares contain questions.",
    "5. Correct answer grants points.",
    "6. Wrong answer costs points AND moves you 2 squares BACK!",
    "7. Some squares are traps!",
    "8. Reach the final square to win.",
    "9. First player to reach the finish wins.",
    "10. Press ESC to return to Menu."
]

def check_winner():
    if player1.current_square == len(board.tile) - 1:
        return 1
    elif player2.current_square == len(board.tile) - 1:
        return 2
    return 0

def reset_game():
    global score1, score2, current_player, show_question
    score1 = 0
    score2 = 0
    player1.current_square = 0
    player1.target_square = 0
    player2.current_square = 0
    player2.target_square = 0
    current_player = 1
    show_question = False

def render_wrapped_text(surface, text, font_obj, color, start_x, start_y, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font_obj.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    
    for i, line in enumerate(lines):
        rendered_surface = font_obj.render(line, True, color)
        surface.blit(rendered_surface, (start_x, start_y + i * (font_obj.get_linesize() - 5)))
    return len(lines) * font_obj.get_linesize()

while True:
    winner_status = check_winner()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
        if event.type == pg.KEYDOWN:
            if winner_status != 0:
                if event.key == pg.K_SPACE:
                    reset_game()
                    game_state = "MENU"
                continue

            if show_question:
                if event.key == pg.K_a: selected_answer = "a"
                elif event.key == pg.K_b: selected_answer = "b"
                elif event.key == pg.K_c: selected_answer = "c"
                elif event.key == pg.K_d: selected_answer = "d"
                
                if selected_answer is not None:
                    q = questions[active_question]
                    if selected_answer == q["correct"]:
                        if question_player == 1: score1 += 15
                        else: score2 += 15
                    else:
                        if question_player == 1: 
                            score1 -= 15
                            player1.target_square = max(0, player1.target_square - 2)
                        else: 
                            score2 -= 15
                            player2.target_square = max(0, player2.target_square - 2)
                        
                    show_question = False
                    selected_answer = None
                continue  
                
            if game_state == "MENU":
                if event.key in [pg.K_RSHIFT, pg.K_LSHIFT]:
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pg.K_i:
                    game_state = "INSTRUCTIONS"
                    
            elif game_state == "INSTRUCTIONS":
                if event.key == pg.K_ESCAPE:
                    game_state = "MENU"
                    
            elif game_state == "PLAYING":
                if event.key == pg.K_SPACE:
                    dice.trigger_roll()
                elif event.key == pg.K_ESCAPE:
                    game_state = "MENU"
                
    if game_state == "MENU":
        screen.screen.fill((200, 200, 200)) 
        start = font.render("Welcome to Python game !", True, (34, 54, 21))
        options = font.render("Press 'I' for instruction or Shift to Start", True, (34, 54, 21))
        screen.screen.blit(start, (300, 180))
        screen.screen.blit(options, (180, 260))
        
        p1_menu = pg.transform.scale(player1.image, (150, 150))
        p2_menu = pg.transform.scale(player2.image, (150, 150))
        screen.screen.blit(p1_menu, (300, 330))
        screen.screen.blit(p2_menu, (550, 330))
        
    elif game_state == "INSTRUCTIONS":
        screen.screen.fill((200, 200, 200))
        for i, line in enumerate(instructions):
            text = font.render(line, True, (0, 0, 0))
            screen.screen.blit(text, (50, 20 + i * 38))    
 
    elif game_state == "PLAYING":
        if winner_status == 0:
            screen.screen.blit(board.board, board.rect)
            
            player1.update_movement(board.tile)
            player2.update_movement(board.tile)
            
            screen.screen.blit(player1.image, player1.rect)
            screen.screen.blit(player2.image, player2.rect)
            
            dice.draw(screen.screen)
            display_score()
            
            if show_question and not player1.is_moving() and not player2.is_moving():
                pg.draw.rect(screen.screen, (240, 240, 240), (100, 40, 800, 420)) # تم تكبير الارتفاع لـ 420 وتعديل بداية Y لـ 40 ليعطي مساحة أكبر
                pg.draw.rect(screen.screen, (0, 0, 0), (100, 40, 800, 420), 4)
                
                q = questions[active_question]
                q_font = pg.font.Font("Font/Archivo_Black/ArchivoBlack-Regular.ttf", 16) # تصغير حجم خط السؤال قليلاً ليناسب الالتفاف
                options_font = pg.font.Font("Font/Archivo_Black/ArchivoBlack-Regular.ttf", 20) # تصغير خط الخيارات بدقة
                
                # 2. طباعة السؤال في الأعلى
                text_height = render_wrapped_text(screen.screen, f"Question: {q['q']}", q_font, (200, 0, 0), 130, 60, 740)
                
                # 3. الحل الجذري: نحدد مسافة مرنة للأسفل بناءً على طول السؤال ولكن مع سقف أمان وثابت بين السطور
                options_start_y = 65 + text_height
                if options_start_y < 160: # تأمين ألا تصعد الخيارات للأعلى وتداخل مع السؤال
                    options_start_y = 160
                    
                # 4. طباعة الاختيارات الأربعة بمسافات رأسية متناسقة (36 بكسل بدلاً من 42)
                screen.screen.blit(options_font.render(q["a"], True, (0, 0, 0)), (140, options_start_y))
                screen.screen.blit(options_font.render(q["b"], True, (0, 0, 0)), (140, options_start_y + 36))
                screen.screen.blit(options_font.render(q["c"], True, (0, 0, 0)), (140, options_start_y + 72))
                screen.screen.blit(options_font.render(q["d"], True, (0, 0, 0)), (140, options_start_y + 108))
        else:
            screen.screen.fill((100, 23, 129))
            active_winner_img = player1.image if winner_status == 1 else player2.image
            p_win = pg.transform.scale(active_winner_img, (200, 200))
            screen.screen.blit(p_win, p_win.get_rect(midbottom=(500, 250)))
            
            winning_text = f"Congratulations! Player {winner_status} is the winner!"
            winning = font.render(winning_text, True, (255, 255, 255))
            restart = font.render("Press SPACE to restart and play again", True, (200, 200, 200))
            
            screen.screen.blit(winning, (150, 300))
            screen.screen.blit(restart, (230, 370))
                    
    pg.display.update()
    clock.tick(60)