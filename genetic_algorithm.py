git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin master

import random

class Driver:
    def __init__(self, name, cost, quality, capacity, fuel_consumption, reliability):
        self.name = name
        self.id = random.randint(1000, 9999)
        self.cost = cost
        self.quality = quality
        self.capacity = capacity
        self.fuel_consumption = fuel_consumption
        self.reliability = reliability

def generate_initial_population(drivers, population_size):
    population = []
    for _ in range(population_size):
        shuffled_drivers = random.sample(drivers, len(drivers))
        population.append(shuffled_drivers)
    return population

def evaluate_solution(solution):
    total_cost = sum(driver.cost for driver in solution)
    total_quality = sum(driver.quality for driver in solution)
    total_capacity = sum(driver.capacity for driver in solution)
    total_fuel = sum(driver.fuel_consumption for driver in solution)
    total_reliability = sum(driver.reliability for driver in solution)
    

    weight_quality = 0.4
    weight_capacity = 0.3
    weight_reliability = 0.2
    weight_cost = -0.3  
    weight_fuel = -0.2  
    
    
    score = (
        weight_quality * total_quality +
        weight_capacity * total_capacity +
        weight_reliability * total_reliability +
        weight_cost * total_cost +
        weight_fuel * total_fuel
    )
    return score

def select_parents(population):
    
    scores = [evaluate_solution(solution) for solution in population]
    
    total_score = sum(scores)
    probabilities = [score / total_score for score in scores]
    
    parent1 = random.choices(population, probabilities, k=1)[0]
    parent2 = random.choices(population, probabilities, k=1)[0]
    return parent1, parent2

def crossover(parent1, parent2):
    crossover_point = len(parent1) // 2
    child1 = parent1[:crossover_point] + [d for d in parent2 if d not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [d for d in parent1 if d not in parent2[:crossover_point]]
    return child1, child2

def mutate(solution, mutation_rate):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(solution)), 2)
        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]

def genetic_algorithm(drivers, population_size=10, generations=100, mutation_rate=0.1):
    population = generate_initial_population(drivers, population_size)
    
    for generation in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])
        population = new_population

    best_solution = max(population, key=evaluate_solution)
    return best_solution
