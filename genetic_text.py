# Generate a specific text using some kind of genetic algorithm.
#
# I want to try to generate some specific text, which I'll call the 'goal'.
# For example the pangram "the quick brown fox jumps over the lazy dog". 
# This particular goal has 43 characters including the spaces.
#
# My idea is to start with a population of at least 10 'specimens'. A 'specimen'
# 'specimen' will be, in this first version, a string of text with 43 characters 
# (the length of the goal), random or hardcoded. Then 'breed' pairs of this 
# initial population to produce a new generation. Some of the specimens in this
# new generation might have a mutation. A mutation will be simply a random 
# character, randomly changed.
#
# For a "survival of the fittest" scenario, those specimens closer to the goal 
# text will have a better chance of breeding. A specimen will be considered 
# closer to the goal based on the correct number of characters in the correct 
# position. The number of correct characters in correct location are the 
# 'fitness' of the specimen.

import random
import string
import statistics

goal = 'the quick brown fox jumps over the lazy dog'


def generate_specimen(length, seed=''):
    """Generate a new specimen of the given length, using the given seed.

    Based on the seed, generate a specimen with the specified length.
    Example if the seed is 'a' and length is 5, then the specimen will
    be 'aaaaa'. With a multicharacter seed, repeat the seed. For example
    with seed 'abc', and length 10, the specimen should be 'abcabcabca'.
    With an empty seed, just generate a specimen of the given length with
    random characters.
    """
    specimen = ''

    if seed == '':
        source = string.ascii_lowercase + ' '
        return ''.join(random.choice(source) for i in range(length))
    else:
        while len(specimen) < length:
            specimen += seed
        return specimen[:length]


def specimen_fitness(specimen, goal):
    result = 0
    for i in range(len(specimen)):
        if specimen[i] == goal[i]:
            result += 1
    return result


def mutation(specimen):
    source = string.ascii_lowercase + ' '
    newValue = random.choice(source)
    position = random.randint(0, len(specimen) - 1)
    mutable = list(specimen)
    mutable[position] = newValue
    return ''.join(mutable)


def breed(parent_a, parent_b):
    childSize = max(len(parent_a), len(parent_b))
    child = ''
    for i in range(childSize):
        genePool = ''
        geneA = ''
        geneB = ''
        if i < len(parent_a):
            genePool += 'a'
            geneA = parent_a[i]
        if i < len(parent_b):
            genePool += 'b'
            geneB = parent_b[i]

        if len(genePool) > 1:
            geneSource = random.choice(genePool)
        else:
            geneSource = genePool

        if geneSource == 'a':
            child += geneA
        else:
            child += geneB

    has_mutation = random.randint(0, 1) == 1
    if has_mutation:
        return mutation(child)
    else:
        return child


def remove_older_generation(population, generation):
    """Remove all especimens equal or older to the given generation number."""
    population = [s for s in population if s[2] > generation]


def find_fittest(population):
    maxFit = 0
    fittest = ()
    for s in population:
        if s[1] > maxFit:
            fittest = s
            maxFit = s[1]
    return fittest


def minimum_breed_fitness(population):
    """Return the minimum fitness required for breeding."""
    non_zero_fitnesses = [s[1] for s in population if s[1] > 0]
    return statistics.median_low(non_zero_fitnesses)


def colour_match(specimen, goal):
    """Return a string where characters matching the goal appear green."""
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    result = ''
    for i in range(len(specimen)):
        if specimen[i] == goal[i]:
            result += OKGREEN + specimen[i] + ENDC
        else:
            result += specimen[i]
    return result


def print_match(specimen, goal):
    result = colour_match(specimen, goal)
    print(result)


def print_population_info(population, generation, goal):
    print('-- generation ' + str(generation) +':')

    # i = 1
    # for s in population:
    #     print(i, s[2], colour_match(s[0], goal), s[1])
    #     i += 1

    fittest = find_fittest(population)
    print('fittest:', colour_match(fittest[0], goal), fittest[1])
    print('population:', len(population))

    return fittest[1]

# ---

# Generate original population of 32 specimens
population = []
goalLength = len(goal)
gen = 0
for i in range(32):
    specimen = generate_specimen(goalLength)
    specimenInfo = (specimen, specimen_fitness(specimen, goal), gen)
    population.append(specimenInfo)

# Print population info
highest_fitness = print_population_info(population, gen, goal)

cont = ''
while (cont.lower() != 'n') and (highest_fitness < len(goal)):
    # Breed pairs of specimens with a fitness greater than the current generation number (gen)
    parents = []
    new_generation = []
    min_breed_fitness = minimum_breed_fitness(population)
    print('minimum breed fitness:', min_breed_fitness)

    for s in population:
        # Only breed parents with a fitness greater or equal to min_breed_fitness
        if (s[1] >= min_breed_fitness) and (len(parents) < 2):
            parents.append(s)
        if len(parents) == 2:
            child = breed(parents[0][0], parents[1][0])
            childInfo = (child, specimen_fitness(child, goal), gen+1)
            new_generation.append(childInfo)
            parents = []

    population += new_generation
    gen += 1
    population = [s for s in population if s[2] > gen - 3]

    # Print population info
    highest_fitness = print_population_info(population, gen, goal)
    
    cont = input("Continue? [Y/n]")