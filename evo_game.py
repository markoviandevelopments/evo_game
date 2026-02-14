from lib_evo import Agent, Environment


environment = Environment()

environment.initialize_pop(10)

environment.agents[0].bark()
