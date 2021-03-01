import pygame
import math
import numpy as np
import random
from block import Block
from brain import brain
from pprint import pprint

TOLEFT=0
TORIGHT=1
TOTOP=2
TODOWN=3
YELLOW=(255,255,0)

class Snake :
    def __init__(self, screen, w, h):
        self.blocks=[Block(int(w/2),int(h/2),YELLOW), Block(int(w/2)+10,int(h/2),YELLOW)]
        self.size=2
        self.direction=random.randrange(0,4)
        self.dx=10
        self.dy=10
        self.w=w
        self.h=h
        self.screen=screen
        self.is_alive=True
        self.score=0
        self.energy= 1000.0
        self.dist= 2000.0
        self.brain=brain()
    
    def set_dist(self, dist) :
        if dist < self.dist :
            self.brain.good()
        else :
            self.brain.bad()
        self.dist=dist

    def set_direction(self, d) :
        if not ((self.direction, d) in [(0,1),(1,0),(2,3),(3,2)]):
             self.direction=d

    def update_gradient(self):
        self.brain.update_gradient()

    def reset_reward(self):
        self.brain.reward=0

    def take_decesion(self,prey_pos) :
        inputs=[prey_pos[0], prey_pos[1],self.direction]
        if self.size < 5 :
            inputs.append(2000.0)
        else:    
            mi=math.dist(self.blocks[0].rect.center,self.blocks[1].rect.center)
            for i in range(2, self.size):
                d=math.dist(self.blocks[0].rect.center,self.blocks[i].rect.center)
                if d < mi :
                    mi=d
            inputs.append(d)

        inputs.append(math.dist(self.blocks[0].rect.center,prey_pos))
        inputs.append(self.blocks[0].rect.top)
        inputs.append(self.h - self.blocks[0].rect.bottom)
        inputs.append(self.blocks[0].rect.left)
        inputs.append(self.w - self.blocks[0].rect.right)
        inputs=np.array(inputs).reshape((1,9))
        dis=self.brain.decision(inputs)
        self.set_direction(np.argmax(dis))


    def turn_right(self):
        if self.direction == TOLEFT :
            self.direction = TOTOP
        elif self.direction == TORIGHT :
            self.direction = TODOWN
        elif self.direction == TOTOP :
            self.direction = TORIGHT
        else :
            self.direction = TOLEFT

    def turn_left(self):
        if self.direction == TOLEFT :
            self.direction = TODOWN
        elif self.direction == TORIGHT :
            self.direction = TOTOP
        elif self.direction == TOTOP :
            self.direction = TOLEFT
        else :
            self.direction = TORIGHT


    def reset_blocks(self):
        self.blocks=[Block(int(self.w/2),int(self.h/2),YELLOW), Block(int(self.w/2)+10,int(self.h/2),YELLOW)]
        self.size=2
        self.direction=random.randrange(0,4)

    def move(self):
        l=len(self.blocks)-1
        while l>0 :
            self.blocks[l].rect.center = self.blocks[l-1].rect.center 
            l-=1
        if self.direction== TOLEFT :
            self.blocks[0].rect.centerx-=self.dx
        elif self.direction== TORIGHT :
            self.blocks[0].rect.centerx+=self.dx
        elif self.direction== TOTOP :
            self.blocks[0].rect.centery-=self.dy
        else :
            self.blocks[0].rect.centery+=self.dy


        self.dec_energy()
        self.test_wall_collision()

    def test_wall_collision(self):
        if self.blocks[0].rect.top <= 0 :
            self.energy -= 10
            self.brain.bad()
            return True
        elif self.blocks[0].rect.bottom >= self.h :
            self.energy -= 10
            self.brain.bad()
            return True
        elif self.blocks[0].rect.left <= 0 :
            self.energy -= 10
            self.brain.bad()
            return True
        elif self.blocks[0].rect.right >= self.w :
            self.energy -= 10
            self.brain.bad()
            return True

        return False

    def dec_energy(self):
        self.energy-=1
        '''if self.energy == 0 :
            self.is_alive = False'''

    def test_self_collision(self):
        for i in range(3,self.size):
            if self.blocks[0].rect.colliderect(self.blocks[i].rect) !=0 :
                self.energy-=10
                self.brain.bad()
                return True
        return False

    def test_prey_collision(self, prey):
        if self.blocks[0].rect.colliderect(prey.rect) != 0 :
            self.eat()
            return True
        return False

    def eat(self) :
        self.blocks.append(Block((self.blocks[-1].rect.centerx+self.dx)%800,self.blocks[-1].rect.centery,YELLOW))
        self.size+=1
        self.energy += 10
        self.brain.good()
        self.score+=1

    def blit(self):
        for block in self.blocks :
            self.screen.blit(block.surface, block.rect)