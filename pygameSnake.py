import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np


BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)



pygame.init()

font = pygame.font.SysFont('arial', 20)

Point = namedtuple('Point', 'x, y')
blockSize = 20;
clockSpeed = 10;

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame():
    
    def __init__(self, w=640, h=480):
        self.w = w 
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        

    def reset(self):
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-blockSize, self.head.y), Point(self.head.x-(2*blockSize), self.head.y)]
        
        self.score = 0
        self.food = None
        self._placeFood()
        self.frameCount = 0
        
    
    def _placeFood(self):
        x = random.randint(0, (self.w-blockSize) // blockSize ) * blockSize
        y = random.randint(0, (self.h-blockSize) // blockSize ) * blockSize

        self.food =  Point(x,y)
        if self.food in self.snake:
            self._placeFood()
        
    def playStep(self, action):
        self.frameCount += 1
        for event in pygame.event.get() or self.frameCount > 100*len(self.snake):
            if event == pygame.QUIT:
                pygame.quit()
                quit()
        
        self._move(action)
        self.snake.insert(0, self.head)
        
        game_over = False
        if self.collision(action):
            game_over = True
            return game_over, self.score
        
        if self.head == self.food:
            self.score += 1
            self._placeFood()
        else:
            self.snake.pop()
        
        self. _updateUI()
        self.clock.tick(clockSpeed)
        
        game_over = False
        return game_over, self.score

    def _updateUI(self):
        self.display.fill(BLACK)
        
        for p in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(p.x, p.y, blockSize, blockSize))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, blockSize, blockSize))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()
    
    def _move(self, action):
        clockWise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockWise.index(self.direction)
        
        if np.array_equal(clockWise, [1,0,0]):
            newDirection = clockWise[idx]
        elif np.array_equal(clockWise, [0,1,0]):
            new_idx = (idx+1) % 4
            newDirection = clockWise[new_idx]
        else:
            new_idx = (idx-1) % 4
            newDirection = clockWise[new_idx]
        
        self.direction = newDirection
        
        x=self.head.x
        y=self.head.y
        
        if self.direction == Direction.RIGHT:
            x += blockSize
        elif self.direction == Direction.LEFT:
            x -= blockSize
        elif self.direction == Direction.DOWN:
            y += blockSize
        elif self.direction == Direction.UP:
            y -= blockSize
        
        self.head = Point(x, y)
    
    def collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - blockSize or pt.x < 0 or pt.y > self.h - blockSize or pt.x < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False