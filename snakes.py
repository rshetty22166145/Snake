import pygame,sys,math,random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.new_block=False
        self.direction = Vector2(1,0)
        

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        


    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index,block in enumerate(self.body):
            x_pos=int(block.x*cell_size)
            y_pos=int(block.y*cell_size)
            block_rect=pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index==0:
                screen.blit(self.head,block_rect)
                
            if index==len(self.body)-1:
                screen.blit(self.tail,block_rect)
                
            elif(index!=0 and index!=len(self.body)-1):
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)
    def update_head_graphics(self):
        head_direction=self.body[1]-self.body[0]
        if head_direction == Vector2(1,0):
            self.head = self.head_left
        if head_direction == Vector2(-1,0):
            self.head=self.head_right
        if head_direction == Vector2(0,1):
            self.head=self.head_up
        if head_direction== Vector2(0,-1):
            self.head=self.head_down
            
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        if tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        if tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        if tail_relation == Vector2(0,-1):
            self.tail = self.tail_down
            
        

            
    def move_snake(self):
        if self.new_block==True:
            
            body_copy=self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]
            self.new_block=False
        else:
            body_copy=self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]
            
    def add_block(self):
        self.new_block=True
        
    def play_crunch_sound(self):
        self.crunch_sound.play()
    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        
            
class FRUIT(SNAKE):
    def __init__(self):
        self.snake=SNAKE()
        self.randomize()

    def draw_fruit(self):
        # draw the rectangle on to the screen
        
        fruit_rect=pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        '''pygame.draw.rect(screen,(126,166,114),fruit_rect)'''
    def randomize(self):
        # create an x,y position and covert it into a vector
        
        self.x=random.randint(0,cell_number-1)
        self.y=random.randint(0,cell_number-1)

        for blocks in self.snake.body[:]:
            if blocks.x== self.x and blocks.y == self.y:
                self.randomize()
            else:
                self.pos=Vector2(self.x,self.y)
                
            
            
        
    
    
        

class MAIN:
    def __init__(self):
        self.snake=SNAKE()
        self.fruit=FRUIT()
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_high_score()
    def update(self):
        self.snake.move_snake()
        self.eating_fruit()
        self.check_fail()
        
    def eating_fruit(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
    def check_fail(self):
        if self.snake.body[0].x not in range(0,cell_number) or self.snake.body[0].y not in range(0,cell_number):
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
            
            
    
    def game_over(self):
        
        self.snake.reset()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render("Current Score:"+str(score_text),True,(56,74,12))
        score_x = int(cell_size * cell_number - 100)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 8,apple_rect.height)
        
        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)
    
    def draw_high_score(self):
        global a
        score_text = str(len(self.snake.body) - 3)
        if a<=int(score_text):
            a=int(score_text)
        high_score_surface = game_font.render("High Score:"+str(a),True,(56,74,12))
        high_score_x = int(cell_size * cell_number - 100)
        high_score_y = int(cell_size * cell_number - 80)
        high_score_rect = high_score_surface.get_rect(center = (high_score_x,high_score_y))
        apple_rect = apple.get_rect(midright = (high_score_rect.left,high_score_rect.centery))
        high_bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + high_score_rect.width + 8,apple_rect.height)
            
        pygame.draw.rect(screen,(167,209,61),high_bg_rect)
        screen.blit(high_score_surface,high_score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),high_bg_rect,2)
    
        
        
pygame.init()
cell_size=40
cell_number=20
screen=pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number))
clock=pygame.time.Clock()
apple=pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
SCREEN_UPDATE=pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)
a=0

main_game=MAIN()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            print("Your High Score Was:",a)
            print("Thanks For Playing")
            pygame.quit()
            sys.exit()
        if event.type==SCREEN_UPDATE:
            main_game.update()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                if main_game.snake.direction.y !=1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key==pygame.K_DOWN:
                if main_game.snake.direction.y !=-1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key==pygame.K_LEFT:
                if main_game.snake.direction.x !=1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key==pygame.K_RIGHT:
                if main_game.snake.direction.x !=-1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_ESCAPE:
                print("Your High Score Was:",a)
                print("Thanks For Playing,Made By Rohit Shetty")
                pygame.quit()
                sys.exit()
                
            
            

                
                
            
    screen.fill(pygame.Color("light green"))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)



