import random


class Agent:
    global i

    def __init__(self, i, x, y):
        self.id = i
        self.number = -1
        self.x = x
        self.y = y
    
    def bark(self):
        print(f'Woof ({self.number})! - dog when grokking it. Agent at {self.x}, {self.y}')
    


class Environment:

    def __init__(self):
        self.agents = []


    def initialize_pop(self, n):
        for i in range(n):
            x = random.uniform(0,1)
            y = random.uniform(0,1)
            self.agents.append(Agent(i, x, y))
            
