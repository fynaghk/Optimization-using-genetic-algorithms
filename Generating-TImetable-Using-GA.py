import random

# define the fitness function
def fitness(schedule):
    # calculate the number of hard constraint violations
    hard_violations = 0
    for day in schedule:
        teacher_count = {}
        student_count = {}
        for timeslot in day:
            for class_ in timeslot:
                teacher = class_['teacher']
                students = class_['students']
                if teacher in teacher_count:
                    teacher_count[teacher] += 1
                else:
                    teacher_count[teacher] = 1
                for student in students:
                    if student in student_count:
                        student_count[student] += 1
                    else:
                        student_count[student] = 1
        for count in teacher_count.values():
            if count > 1:
                hard_violations += count - 1
        for count in student_count.values():
            if count > 1:
                hard_violations += count - 1

    # calculate the number of soft constraint violations
    soft_violations = 0
    for day in schedule:
        teacher_count = {}
        student_count = {}
        for timeslot in day:
            for class_ in timeslot:
                teacher = class_['teacher']
                students = class_['students']
                if teacher in teacher_count:
                    teacher_count[teacher] += 1
                else:
                    teacher_count[teacher] = 1
                for student in students:
                    if student in student_count:
                        student_count[student] += 1
                    else:
                        student_count[student] = 1
        for count in teacher_count.values():
            if count > 3:
                soft_violations += count - 3
        for count in student_count.values():
            if count > 4:
                soft_violations += count - 4

    return hard_violations * 10 + soft_violations
# define the crossover function
def crossover(schedule1, schedule2):
    # select a random crossover point
    crossover_point = random.randint(0, len(schedule1)-1)
    # create the offspring schedules by swapping days at the crossover point
    offspring1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    offspring2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return offspring1, offspring2
# define the mutation function
def mutation(schedule):
    # select a random mutation point (day and timeslot)
    mutation_day = random.randint(0, len(schedule)-1)
    mutation_timeslot = random.randint(0, len(schedule[mutation_day])-1)
    # mutate the schedule by randomly shuffling classes within the selected timeslot
    random.shuffle(schedule[mutation_day][mutation_timeslot])
    return schedule
# define the selection function
def selection(population):
    # calculate the fitness of each individual in the population
    fitnesses = [fitness(individual) for individual in population]
    # select the best individuals to be parents for the next generation based on tournament selection with a tournament size of 2
    parents = []
    for i in range(2):
        tournament_indices = random.sample(range(len(population)), k=2)
        tournament_fitnesses = [fitnesses[index] for index in tournament_indices]
        min_fitness_index = tournament_indices[tournament_fitnesses.index(min(tournament_fitnesses))]
        parents.append(population[min_fitness_index])
    return parents
# define the genetic algorithm function
def genetic_algorithm(classes, days, timeslots_per_day, population_size, max_generations):
    # create an initial population of random schedules
    population = []
    for i in range(population_size):
        individual = []
        for j in range(days):
            day_schedule=[]
            for k in range(timeslots_per_day):
                day_schedule.append(random.sample(classes,k+1))
            individual.append(day_schedule)
            
        population.append(individual) 



# Define sample dataset
classes = [
    {'name': 'Math', 'teacher': 'Mr. Smith', 'students': ['Alice', 'Bob', 'Charlie']},
    {'name': 'English', 'teacher': 'Ms. Johnson', 'students': ['Alice', 'David', 'Eve']},
    {'name': 'Science', 'teacher': 'Dr. Brown', 'students': ['Bob', 'Charlie', 'Eve']},
    {'name': 'History', 'teacher': 'Mr. White', 'students': ['Alice', 'David']},
    {'name': 'Art', 'teacher': 'Ms. Green', 'students': ['Charlie', 'Eve']}
]

# Parameters for the genetic algorithm
days = 5  # Number of days in the schedule
timeslots_per_day = 3  # Number of timeslots per day
population_size = 10  # Population size
max_generations = 50  # Maximum number of generations

# Run the genetic algorithm
result = genetic_algorithm(classes, days, timeslots_per_day, population_size, max_generations)

def genetic_algorithm(classes, days, timeslots_per_day, population_size, max_generations):
    # create an initial population of random schedules
    population = []
    for i in range(population_size):
        individual = []
        for j in range(days):
            day_schedule = []
            for k in range(timeslots_per_day):
                day_schedule.append(random.sample(classes, k + 1))
            individual.append(day_schedule)

        population.append(individual)

    # Run the algorithm for the specified number of generations
    for generation in range(max_generations):
        # Calculate fitness for each individual in the population
        fitnesses = [fitness(individual) for individual in population]
        
        # Select the best individuals to form the next generation
        parents = selection(population)
        
        # Create offspring through crossover
        offspring1, offspring2 = crossover(parents[0], parents[1])
        
        # Mutate the offspring
        offspring1 = mutation(offspring1)
        offspring2 = mutation(offspring2)
        
        # Add offspring to the population (you may need to implement selection to limit population size)
        population.append(offspring1)
        population.append(offspring2)

        # Limit the population size to avoid it growing too large
        if len(population) > population_size:
            population = sorted(population, key=fitness)[:population_size]
    
    # Return the best schedule (individual with the lowest fitness score)
    best_individual = min(population, key=fitness)
    return best_individual

# Run the genetic algorithm
result = genetic_algorithm(classes, days, timeslots_per_day, population_size, max_generations)

# Print the optimized timetable
if result:
    for day_idx, day in enumerate(result):
        print(f"Day {day_idx + 1}:")
        for timeslot_idx, timeslot in enumerate(day):
            print(f"  Timeslot {timeslot_idx + 1}: {timeslot}")
else:
    print("No valid timetable generated.")
