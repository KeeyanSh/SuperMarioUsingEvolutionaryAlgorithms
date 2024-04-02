import random


class Game:
    def __init__(self, levels, initial_population_size, calculate_win_prize, p_mutation, p_crossover,
                 use_roulette_wheel, cross_over_points):

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0
        self.population_size = initial_population_size
        self.population = None
        self.children = None
        self.fitness = None
        self.last_fitness_average = -1000
        self.fitness_average = None
        self.calculate_win_prize = calculate_win_prize
        self.p_mutation = p_mutation
        self.p_crossover = p_crossover
        self.use_roulette_wheel = use_roulette_wheel
        self.cross_over_points = cross_over_points
        self.max_fitnesses = []
        self.average_fitnesses = []
        self.min_fitnesses = []

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def get_score(self, actions):
        actions = list(actions)

        current_level = self.levels[self.current_level_index]
        steps, max_steps = 0, 0
        win = True
        for i in range(1, self.current_level_len):
            current_step = current_level[i]
            if i == self.current_level_len - 1 and win:
                if self.calculate_win_prize:
                    steps += 5

            if actions[i - 1] in {'1', '2'}:
                steps -= .5

            if current_step == '_':
                steps += 1
                if i == self.current_level_len - 2:
                    steps += 1
            elif current_step == 'M' and (actions[i - 1] == '0' or i > 1 and actions[i - 2] == '1'):
                steps += 3

            elif current_step == 'G' and actions[i - 1] == '1':
                steps += 1

            elif current_step == 'G' and i > 1 and actions[i - 2] == '1':
                steps += 3

            elif current_step == 'L' and actions[i - 1] == '2':
                steps += 1

            else:
                max_steps = max(max_steps, steps)
                steps = 0
                win = False

            max_steps = max(max_steps, steps)

        return win, max_steps

    def refine_population(self):
        for i in range(len(self.population)):
            pl = list(self.population[i])
            for j in range(len(pl)):
                if j > 0:
                    if pl[j - 1] == '1':
                        pl[j] = '0'
                    elif pl[j - 1] == '2':
                        if pl[j] == '1' or (j>1 and pl[j-2]=='2'):
                            pl[j] = '0'

            self.population[i] = ''.join(pl)

    def initialize_population(self):
        self.population = []
        for i in range(self.population_size):
            str = ''
            for j in range(self.current_level_len):
                str += f'{random.randint(0,2)}'
            self.population.append(str)
        self.refine_population()

    def calculate_fitness(self):
        self.fitness = []
        for p in self.population:
            self.fitness.append(self.get_score(p)[1])

        self.max_fitnesses.append(max(self.fitness))
        self.min_fitnesses.append(min(self.fitness))
        self.average_fitnesses.append(sum(self.fitness) / len(self.fitness))

    def select_highest_fitness(self):
        self.population = [p for _, p in sorted(zip(self.fitness, self.population))][
                          len(self.population) - int(self.population_size / 2):]

    def select_roulette_wheel(self):
        selected = []
        fitness_sum = 0
        for f in self.fitness:
            fitness_sum += f
        fitness = [f / fitness_sum for f in self.fitness]

        probs = []
        for i in range(len(self.population)):
            if i == 0:
                probs.append(fitness[i])
            else:
                probs.append(fitness[i] + probs[i - 1])

        for i in range(int(self.population_size / 2)):
            rand = random.randint(0, 1000) / 1000
            for j in range(len(probs)):
                if rand <= probs[j]:
                    selected.append(self.population[j])
                    break
        self.population = selected

    def crossover(self):
        children = []
        for i in range(int(self.population_size / 2)):
            parent_1 = self.population[random.randint(0, int(len(self.population) / 2))]
            parent_2 = self.population[random.randint(0, int(len(self.population) / 2))]
            crossover = random.randint(0, 1000) / 1000 <= self.p_crossover

            if crossover:
                cross_gene_1 = random.randint(0, self.current_level_len - 1)
                cross_gene_2 = random.randint(0, self.current_level_len - 1)
                if self.cross_over_points == 2:
                    child_1 = ''.join(
                        list(parent_1)[:cross_gene_1] +
                        list(parent_2)[cross_gene_1:cross_gene_2] + list(parent_1)[cross_gene_2:])
                    child_2 = ''.join(
                        list(parent_2)[:cross_gene_1]
                        + list(parent_1)[cross_gene_1:cross_gene_2] + list(parent_2)[cross_gene_2:])
                elif self.cross_over_points == 1:
                    child_1 = ''.join(list(parent_1)[:cross_gene_1] + list(parent_2)[cross_gene_1:])
                    child_2 = ''.join(list(parent_2)[:cross_gene_1] + list(parent_1)[cross_gene_1:])

            else:
                child_1 = parent_1
                child_2 = parent_2

            if random.randint(0, 1):
                children.append(child_1)
            else:
                children.append(child_2)
        self.children = children

    def mutation(self):

        for i in range(len(self.children)):
            child = list(self.children[i])
            self.children[i] = ''

            for j in range(len(child)):
                mutation = random.randint(0, 1000) / 1000 <= self.p_mutation
                if mutation:
                    child[j] = f'{random.randint(0, 2)}'
            self.children[i] = ''.join(child)

        self.population += self.children
        self.refine_population()

    def process(self):
        epsilon = 0.001
        iterations = 0
        self.initialize_population()

        def converged():
            self.fitness_average = sum(self.fitness) / len(self.fitness)
            if abs(self.fitness_average - self.last_fitness_average) <= epsilon:
                return True
            self.last_fitness_average = self.fitness_average
            return False

        while iterations < 1000:
            self.calculate_fitness()
            if converged():
                break
            if self.use_roulette_wheel:
                self.select_roulette_wheel()
            else:
                self.select_highest_fitness()
            self.crossover()
            self.mutation()

            iterations += 1

        return [p for _, p in sorted(zip(self.fitness, self.population))][-1]
