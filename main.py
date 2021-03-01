import pygame
from snake import Snake
import time
from block import Block
from pprey import place_prey
import numpy as np
from pprint import pprint
import math

BLACK=(0,0,0)
BLUE=(50,50,255)
YELLOW=(255,255,0)
TOLEFT=0
TORIGHT=1
TOTOP=2
TODOWN=3

pygame.init()
screen = pygame.display.set_mode((800, 600))

snake = Snake(screen, 800, 600)

x,y=place_prey(snake,800,600)
prey = Block(x,y,BLUE)

frame=1
oscore=0

while True :
    screen.fill(BLACK)

    if frame==0 or snake.test_self_collision() or snake.test_wall_collision() :
        #pprint(snake.brain.grad_map)
        snake.blocks[0].rect.center=(400,300)
        snake.reset_blocks()
        #x,y=place_prey(snake,800, 600)
        #prey=Block(x,y,BLUE)
    
    

    if snake.test_prey_collision(prey):
        x,y=place_prey(snake,800, 600)
        prey=Block(x,y,BLUE)

    snake.take_decesion(prey.rect.center)
    snake.move()

    snake.set_dist(math.dist(snake.blocks[0].rect.center, prey.rect.center))
    #pprint(snake.brain.grad_map)
    snake.brain.update_weights()
    snake.update_gradient()

    snake.reset_reward()

    snake.blit()
    screen.blit(prey.surface, prey.rect)

    pygame.display.flip()
    time.sleep(1/30)
    
    frame = (frame+1)%200000
    