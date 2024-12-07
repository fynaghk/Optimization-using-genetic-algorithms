import random
from deap import base, creator, tools, algorithms

# Define the problem and GA parameters
NUM_CLASSES = 10  # Example: Number of classes
NUM_SLOTS = 5  # Number of time slots available
POP_SIZE = 50  # Population size
GENS = 100  # Number of generations

# Define fitness function (maximize fitness)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Define individual and population
toolbox = base.Toolbox()
toolbox.register("attr_time_slot", random.randint, 0, NUM_SLOTS - 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_time_slot, n=NUM_CLASSES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define fitness evaluation
def evaluate(individual):
    conflicts = sum(individual.count(slot) > 1 for slot in range(NUM_SLOTS))
    return 1 / (1 + conflicts),  # Minimize conflicts

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# GA Execution
population = toolbox.population(n=POP_SIZE)
result, _ = algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.2, ngen=GENS, verbose=False)

# Best solution
best_individual = tools.selBest(population, k=1)[0]
print("Optimized Curriculum:", best_individual)
