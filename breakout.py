import pygame
from pygame.locals import *

pygame.init()

#Game Data
screen_height = 600
screen_width = 600
clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("Breakout")

#Define Colors
bg_color = (247, 235, 232)
text_color = (64, 60, 59)
main_font = pygame.font.SysFont("Bauhaus", 80)
sub_font = pygame.font.SysFont("Bauhaus", 40)
paddle_color = ball_color = (103, 82, 81)
red = (232, 94, 94)
green = (59, 220, 139)
blue = (90, 220, 237)

cols = 6
rows = 6

game_over = False

def draw_text(string, font, color, x, y):
    text = font.render(string, True, color)
    screen.blit(text, (x, y))

class Wall():
    def __init__(self) -> None:
        self.width = screen_width // cols
        self.height = 50
    
    def build_wall(self):
        self.blocks = []
        block_individual = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                #genereate x and y position for each block and generate rect
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                else:
                    strength = 1
                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.blocks.append(block_row)
    
    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    block_color = red
                elif block[1] == 2:
                    block_color = green
                elif block[1] == 1:
                    block_color = blue
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, bg_color, block[0], 2)


class Paddle():
    def __init__(self) -> None:
        self.width = screen_width // cols
        self.height = 20
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = paddle_color

    def draw_paddle(self):
        pygame.draw.rect(screen, paddle_color, self.rect)

    def move(self):
        if not game_over:
            key = pygame.key.get_pressed()
            if key[K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if key[K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += self.speed

class Ball():
    def __init__(self) -> None:
        self.width = 10
        self.height = 10
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2) - 30
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 5
        self.direction = [1, 1]
        self.ball_moving = False
        self.game_over = False

    def move(self):
        global game_over
        if self.ball_moving:
            self.rect.x += self.speed * self.direction[0]
            self.rect.y += self.speed * -self.direction[1]
        if self.rect.right == screen_width:
            self.direction[0] = -self.direction[0]
        if self.rect.top == 0:
            self.direction[1] = -self.direction[1]
        if self.rect.left == 0:
            self.direction[0] = -self.direction[0]
        if self.rect.bottom == screen_height:
            game_over = True

        if self.rect.colliderect(paddle):
            self.direction[1] = -self.direction[1]
        
        for row in wall.blocks:
            for item in row:
                if self.rect.colliderect(item[0]):
                    #check if from below:
                    if abs(self.rect.top - item[0].bottom) == 5 or abs(self.rect.bottom - item[0].top) == 5:
                        self.direction[1] = -self.direction[1]
                    elif abs(self.rect.left - item[0].right) == 5 or abs(self.rect.right - item[0].left) == 5:
                        self.direction[0] = -self.direction[0]
                    if item[1] > 1:
                        item[1] -= 1
                    else:
                        item[0] = [0,0,0,0]

    def draw(self):
        pygame.draw.circle(screen, ball_color, (self.rect.x, self.rect.y), self.width)


wall = Wall()
paddle = Paddle()
ball = Ball()
wall.build_wall()

run = True
while run:
    clock.tick(60)

    screen.fill(bg_color)
    wall.draw_wall()
    ball.draw()
    ball.move()
    paddle.draw_paddle()
    paddle.move()

    # Start the game
    key = pygame.key.get_pressed()
    if key[K_SPACE]:
        ball.ball_moving = True
        game_over = False

    if game_over:
        ball.rect.x = (screen_width // 2) - (ball.width // 2)
        ball.rect.y = screen_height - (ball.height * 2) - 30
        ball.direction = [1, 1]
        ball.ball_moving = False
        paddle.rect.x = (screen_width // 2) - (paddle.rect.width // 2)
        paddle.rect.y = screen_height - (paddle.rect.height * 2)
        wall.build_wall()
        draw_text("Game over", main_font, text_color, 100, 200)
        draw_text("Press Spacebar to restart", sub_font, text_color, 100, 300)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()