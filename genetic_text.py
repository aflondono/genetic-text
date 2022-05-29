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

class Specimen:
    """Represents a specimen."""

    def generate_code(self, length, seed=''):
        """Generate a new code of the given length, using the given seed.

        Based on the seed, generate a code with the specified length.
        Example if the seed is 'a' and length is 5, then the code will
        be 'aaaaa'. With a multicharacter seed, repeat the seed. For example
        with seed 'abc', and length 10, the code should be 'abcabcabca'.
        With an empty seed, just generate a code of the given length with
        random characters.
        """
        code = ''

        if seed == '':
            source = string.ascii_lowercase + ' '
            return ''.join(random.choice(source) for i in range(length))
        else:
            while len(code) < length:
                code += seed
            return code[:length]

    def code_fitness(self, goal):
        result = 0
        for i in range(len(self.code)):
            if self.code[i] == goal[i]:
                result += 1
        return result

    def __init__(self, goal, generation, code=''):
        if code == '':
            self.code = self.generate_code(len(goal))
        else:
            self.code = code
        self.fitness = self.code_fitness(goal)
        self.generation = generation


def mutation(code):
    source = string.ascii_lowercase + ' '
    newValue = random.choice(source)
    position = random.randint(0, len(code) - 1)
    mutable = list(code)
    mutable[position] = newValue
    return ''.join(mutable)


def breed(parent_a, parent_b):
    childSize = max(len(parent_a), len(parent_b))
    child_code = ''
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
            child_code += geneA
        else:
            child_code += geneB

    has_mutation = random.randint(0, 1) == 1
    if has_mutation:
        return mutation(child_code)
    else:
        return child_code


def remove_older_generation(population, generation):
    """Remove all specimens equal or older to the given generation number."""
    population = [s for s in population if s.generation > generation]


def find_fittest(population):
    maxFit = 0
    fittest = None
    for s in population:
        if s.fitness > maxFit:
            fittest = s
            maxFit = s.fitness
    return fittest


def minimum_breed_fitness(population):
    """Return the minimum fitness required for breeding."""
    non_zero_fitnesses = [s.fitness for s in population if s.fitness > 0]
    return statistics.median_low(non_zero_fitnesses)


def colour_match(code, goal):
    """Return a string where characters matching the goal appear green."""
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    result = ''
    for i in range(len(code)):
        if code[i] == goal[i]:
            result += OKGREEN + code[i] + ENDC
        else:
            result += code[i]
    return result


def print_match(code, goal):
    result = colour_match(code, goal)
    print(result)


def print_population_info(population, goal):
    # i = 1
    # for s in population:
    #     print(i, s.generation, colour_match(s.code, goal), s.fitness)
    #     i += 1

    fittest = find_fittest(population)
    print('fittest:', colour_match(fittest.code, goal), fittest.fitness)
    print('population:', len(population))

    return fittest.fitness

# ---

# Generate original population of 32 specimens
population = []
goalLength = len(goal)
gen = 0
for i in range(32):
    specimen = Specimen(goal, gen)
    population.append(specimen)

# Print population info
print('-- generation ' + str(gen) +':')
highest_fitness = print_population_info(population, goal)

cont = ''
while (cont.lower() != 'n') and (highest_fitness < len(goal)):
    # Breed pairs of specimens with a fitness greater than the current generation number (gen)
    parents = []
    new_generation = []
    min_breed_fitness = minimum_breed_fitness(population)
    print('minimum breed fitness:', min_breed_fitness)

    for s in population:
        # Only breed parents with a fitness greater or equal to min_breed_fitness
        if (s.fitness >= min_breed_fitness) and (len(parents) < 2):
            parents.append(s)
        if len(parents) == 2:
            child_code = breed(parents[0].code, parents[1].code)
            child = Specimen(goal, gen+1, child_code)
            new_generation.append(child)
            parents = []

    population += new_generation
    gen += 1
    population = [s for s in population if s.generation > gen - 3]

    # Print population info
    print('-- generation ' + str(gen) +':')
    highest_fitness = print_population_info(population, goal)
    
    cont = input("Continue? [Y/n]")