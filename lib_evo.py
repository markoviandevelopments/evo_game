


class Agent:
    global i

    def __init__(self, i):
        self.id = i
    
    def bark(self):
        print("Woof! - dog when grokking it.")
    


class Environment:

    def __init__(self):
        self.agents = []


    def initialize_pop(self, n):
        for i in range(n):
            self.agents.append(Agent(i))
