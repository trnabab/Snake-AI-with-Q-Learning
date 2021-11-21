import pygame
import random
from enum import Enum
from collections import namedtuple

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
        
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-blockSize, self.head.y), Point(self.head.x-(2*blockSize), self.head.y)]
        
        self.score = 0
        self.food = None;
        self._place_food();
    
    def _place_food(self):
        x = random.randint(0, (self.w-blockSize) // blockSize ) * blockSize
        y = random.randint(0, (self.h-blockSize) // blockSize ) * blockSize

        self.food =  Point(x,y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        game_over = False
        if self._collision():
            game_over = True
            return game_over, self.score
        
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        self. _update_ui()
        self.clock.tick(clockSpeed)
        
        game_over = False
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        
        for p in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(p.x, p.y, blockSize, blockSize))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, blockSize, blockSize))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()
    
    def _move(self, direction):
        x=self.head.x
        y=self.head.y
        
        if direction == Direction.RIGHT:
            x += blockSize
        elif direction == Direction.LEFT:
            x -= blockSize
        elif direction == Direction.DOWN:
            y += blockSize
        elif direction == Direction.UP:
            y -= blockSize
        
        self.head = Point(x, y)
    
    def _collision(self):
        if self.head.x > self.w - blockSize or self.head.x < 0 or self.head.y > self.h - blockSize or self.head.x < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False
    
if __name__ == '__main__':
    game = SnakeGame()
    
    while True:
        game_over, score= game.play_step()
        
        if game_over == True:
            break
    
    print("Final Score:", score)
    pygame.quit()