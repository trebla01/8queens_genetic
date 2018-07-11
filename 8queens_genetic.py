import random
import operator
random.seed

# a board looks like the following: [1, 7, 0, 2, 6, 5, 3, 4]
# the number is the queen's position at each column
def generate_rand_board():
    result = [i for i in range(8)]
    random.shuffle(result)
    return result

def draw_board(board):
    drawing = [[0 for x in range(8)] for y in range(8)]
    for i in range(8):
        drawing[board[i]][i] = 1
    for elem in drawing:
        print(elem)

def list_to_str(board):
    return "".join(str(x) for x in board)

def str_to_list(board):
    l = list(board)
    l= [int(x) for x in l]
    return l

# checks for colliding pairs. Can have more than 8 colliding pairs if all diagonal.
# only check for the queens in front of you, assume behind already checked
# checks for colliding pairs
def number_collisions(board):
    collision_pairs = 0
    for i in range(8):
        interested_queen = board[i]
        for j in range(i+1, 8):
            other_queen = board[j]
            if interested_queen + (j-i) == other_queen or \
                                    interested_queen - (j-i) == other_queen or \
                                    interested_queen == other_queen:
                #print("colliding at {} and {}".format(i,j))
                collision_pairs += 1
    return collision_pairs

# max collisions = 28, minimum fitness
# min collision = 0, maximum fitness
def fitness(board):
    collision_pairs = number_collisions(board)
    return (100 - collision_pairs / 28 * 100)

def generate_first_population(size_population):
    population = []
    for i in range(size_population):
        population.append(generate_rand_board())
    return population

# sort population by fitness, returns a dictionary of board with its scores
def sort_population(population):
    sorted_population = {}
    for individual in population:
        sorted_population[list_to_str(individual)] = fitness(individual)
    return sorted(sorted_population.items(), key=operator.itemgetter(1), reverse=True)

def select_from_population(sorted_population, best_sample, lucky_few):
    next_generation = []
    for i in range(best_sample):
        next_generation.append(str_to_list(sorted_population[i][0]))
    for j in range(lucky_few):
        next_generation.append(str_to_list(random.choice(sorted_population)[0]))
    random.shuffle(next_generation)
    return next_generation

#uses crossover algorithm
def create_child(individual1, individual2):
    child = []
    crossover_point = random.randint(0,8)
    for i in range(0, crossover_point):
        child.append(individual1[i])
    for j in range(crossover_point, 8):
        child.append(individual2[j])
    return child

def create_children(breeders, number_of_child):
    next_population = []
    for i in range(len(breeders)//2):
        for j in range(number_of_child):
            next_population.append(create_child(breeders[i], breeders[len(breeders) -1 - i]))
    return next_population

#only mutate 1 queen at most
def mutate_board(board):
    index = random.randint(0,7)
    board[index] = random.randint(0,7)
    return board


def mutate_population(population, chance_of_mutation):
    for i in range(len(population)):
        if random.random() * 100 < chance_of_mutation:
            population[i] = mutate_board(population[i])
    return population

def next_generation(first_generation, best_sample, lucky_few, number_of_child, chance_of_mutation):
    sorted_population = sort_population(first_generation)
    next_breeders = select_from_population(sorted_population, best_sample, lucky_few)
    next_population = create_children(next_breeders, number_of_child)
    next_generation = mutate_population(next_population, chance_of_mutation)
    return next_generation

def multiple_generation(number_of_generation, size_population, best_sample, lucky_few, number_of_child, chance_of_mutation):
    historic = []
    historic.append(generate_first_population(size_population))
    for i in range(number_of_generation):
        historic.append(next_generation(historic[i], best_sample, lucky_few, number_of_child, chance_of_mutation))
    return historic

def get_best_individual(population):
    return sort_population(population)[0]

def get_list_best_individual_from_historic(historic):
    best_individuals = []
    for population in historic:
        best_individuals.append(get_best_individual(population))
    return best_individuals

#print every solution found
def get_solutions(best_individuals):
    solutions = []
    for elem in best_individuals:
        if elem[1] == 100:
            solutions.append(str_to_list(elem[0]))
    return solutions

#constants
size_population = 100
best_sample = 20
lucky_few = 20
number_of_child = 5
number_of_generation = 50
chance_of_mutation = 5

#repeat the evolution process until a solution is found
while True:
    historic = multiple_generation(number_of_generation, size_population, best_sample, lucky_few, number_of_child, chance_of_mutation)
    best_individuals = get_list_best_individual_from_historic(historic)
    solutions = get_solutions(best_individuals)
    if not solutions:
        print("no solutions found, repeat evolution")
        continue
    else:
       for elem in solutions:
           print("Following solution found: ", list_to_str(elem))
           draw_board(elem)
       break
