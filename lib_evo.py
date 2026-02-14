import random

TILE_COUNT_WIDTH = 10
TILE_COUNT_HEIGHT = 10

class Agent:
    global i

    def __init__(self, i, x, y):
        self.id = i
        self.number = -1
        self.x = x
        self.y = y
        self.x_v = 0
        self.y_v = 0
        self.food = 1
    
    def bark(self):
        print(f'Woof ({self.number})! - dog when grokking it. Agent at {self.x}, {self.y}')
    


class Environment:

    def __init__(self):
        self.agents = []
        self.time = 0
        self.tiles = []
        for i in range(TILE_COUNT_WIDTH):
            temp = []
            for j in range(TILE_COUNT_HEIGHT):
                temp.append(1)
            self.tiles.append(temp)

    def initialize_pop(self, n):
        for i in range(n):
            x = random.uniform(0,1)
            y = random.uniform(0,1)
            self.agents.append(Agent(i, x, y))

    def add_agent(self):
        x = random.uniform(0,1)
        y = random.uniform(0,1)
        self.agents.append(Agent(-1, x, y))
    
    def iterate_physics(self):
        for agent in self.agents:

            # Agent EAT
            tile_index_x = int(agent.x * TILE_COUNT_WIDTH)
            tile_index_y = int(agent.y * TILE_COUNT_HEIGHT)
            if (0 <= tile_index_x < TILE_COUNT_WIDTH and
                0 <= tile_index_y < TILE_COUNT_HEIGHT):
                food_transfer = self.tiles[tile_index_x][tile_index_y] * 0.1
                agent.food += food_transfer
                self.tiles[tile_index_x][tile_index_y] -= food_transfer
            agent.x += agent.x_v
            agent.y += agent.y_v
            
            # Agent Hungee
            agent.food -= 0.03

            # Agent Collisions
            if agent.x > 1:
                agent.x = 1
                agent.x_v *= -1
            if agent.x < 0:
                agent.x = 0
                agent.x_v *= -1
            if agent.y > 1:
                agent.y = 1
                agent.y_v *= -1
            if agent.y < 0:
                agent.y = 0
                agent.y_v *= -1
            
        # Food Regen
        for i in range(5):
            x = random.randint(0, TILE_COUNT_WIDTH - 1)
            y = random.randint(0, TILE_COUNT_HEIGHT - 1)
            self.tiles[x][y] += random.uniform(0, 1)
        
        for i in range(len(self.agents) -1, -1, -1):
            agent = self.agents[i]
            if agent.food <= 0:
                self.agents.pop(i)

        if random.uniform(0,1) < 0.01:
            self.add_agent()

        self.time += 1