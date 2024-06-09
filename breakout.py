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
paddle_color = ball_color = (103, 82, 81)
red = (232, 94, 94)
green = (59, 220, 139)
blue = (90, 220, 237)

cols = 6
rows = 6

screen.fill(bg_color)

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



wall = Wall()
wall.build_wall()

run = True
while run:
    clock.tick(60)

    wall.draw_wall()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
