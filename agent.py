import torch
import numpy as np
import random
from collections import deque
from pygameSnake import SnakeGame, Direction, Point

maxMemory = 100_000
batchSize = 1000

class Agent:
    
    def __init__(self):
        self.generation = 0
        self.epsilon = 0
        self.memory = deque(maxlen=maxMemory)
        self.model = None
        self.trainer = None
    
    def getState(self, game):
        head = game.snake[0]
        pointLeft = Point(head.x - 20, head.y)
        pointRight = Point(head.x + 20, head.y)
        pointUp = Point(head.x, head.y - 20)
        pointDown = Point(head.x, head.y + 20)
        
        diirectionLeft = game.direction == Direction.LEFT
        directionRight = game.direction == Direction.RIGHT
        directionUp = game.direction == Direction.UP
        directionDown = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (directionRight and game.collision(pointRight)) or 
            (diirectionLeft and game.collision(pointLeft)) or 
            (directionUp and game.collision(pointUp)) or 
            (directionDown and game.collision(pointDown)),

            # Danger right
            (directionUp and game.collision(pointRight)) or 
            (directionDown and game.collision(pointLeft)) or 
            (diirectionLeft and game.collision(pointUp)) or 
            (directionRight and game.collision(pointDown)),

            # Danger left
            (directionDown and game.collision(pointRight)) or 
            (directionUp and game.collision(pointLeft)) or 
            (directionRight and game.collision(pointUp)) or 
            (diirectionLeft and game.collision(pointDown)),
            
            # Move direction
            diirectionLeft,
            directionRight,
            directionUp,
            directionDown,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, nextState, gameOver):
        self.memory.append((self, state, action, reward, nextState, gameOver))
    
    def trainShortMemory(self, state, action, reward, nextState, gameOver):
        self.trainer.trainStep(state, action, reward, nextState, gameOver)
    
    def trainLongMemory(self):
        if len(self.memory) > batchSize:
            shortSample = random.sample(self.memory, batchSize)
        else:
            shortSample = self.memory
        
        states, actions, rewards, nextStates, gameOvers = zip(*shortSample)
        self.trainer.trainStep(states, actions, rewards, nextStates, gameOvers)
    
    def getAction(self, state):
        self.epsilon = 80 - self.generation
        lastMove = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            lastMove[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            lastMove[move] = 1

        return lastMove
    
def train():
    plotScores = []
    plotMeanScore = []
    totalScore = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    
    oldState = agent.getState(game)
    
    lastMove = agent.getAction(oldState)
    
    reward, gameOver, score = game.playStep(lastMove)
    newState = agent.getState(game)
    
    agent.trainShortMemory(oldState, lastMove, reward, newState, gameOver)
    
    agent.remember(oldState, lastMove, reward, newState, gameOver)
    
    if gameOver:
        game.reset()
        agent.generation+=1
        agent.trainLongMemory()
        
        if score > record:
            record = score
        agent.model.save()

        print('Generation', agent.generation, 'Score', score, 'Record:', record)
        
        plotScores.append(score)
        totalScore += score
        mean_score = totalScore / agent.n_games
        plotMeanScore.append(mean_score)
        plot(plotScores, plotMeanScore)
        
if __name__ == '__main__':
    train()