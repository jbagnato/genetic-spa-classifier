import cv2

from genspa.model.chromosome import Chromosome
from genspa.model.component import Component
from genspa.model.genome import Genome
from genspa.model.webpage import Webpage

import random


class GeneticAlgorithmSPA:

    def __init__(self, webpage:Webpage, pop_size:int, cross_rate:float, muta_rate:float, components_length:int=10):
        self.genomas = list()
        self.population_size = pop_size
        self.crossover_rate = cross_rate
        self.mutation_rate = muta_rate
        self.components_length = components_length
        self.fittest_genome = 0
        self.best_fitness_score = 0.0
        self.total_fitness_score = 0.0
        self.generation = 0
        self.webpage = webpage
        self.memory = list()  # to see how is the evolution over generations
        self.create_start_popualtion()


    def mutate(self, genoma:Genome):
        for i, chromo in enumerate(genoma.components):
            if random.randint(0,100)/100 < self.mutation_rate:
                #flip the bit!
                newchromo = Chromosome(random.choice(list(Component)), top=chromo.top, height_px=chromo.height)
                genoma.components[i] = newchromo

    def crossover(self, mum:Genome, dad:Genome) -> (Genome, Genome):
        if random.randint(0,100)/100 > self.crossover_rate or mum == dad:
            return mum, dad

        cut = random.randint(0, self.components_length)

        baby1 = Genome().reset()
        baby2 = Genome().reset()

        for i in range(self.components_length):
            if i < cut:
                chromo1 = mum.components[i]
                baby1.components.append(chromo1)
                chromo2 = dad.components[i]
                baby2.components.append(chromo2)
            else:
                chromo1 = dad.components[i]
                baby1.components.append(chromo1)
                chromo2 = mum.components[i]
                baby2.components.append(chromo2)

        return baby1, baby2

    def roulette_wheel_selection(self) -> Genome:
        slice = random.randint(0,100)/100 * self.total_fitness_score
        total = 0.0
        selected_genome = 0
        for i in range(self.population_size):
            total += self.genomas[i].fitness
            if total >= slice:
                selected_genome = i
                break

        return self.genomas[selected_genome]

    def update_fitness_score(self):
        self.total_fitness_score = 0.0
        for i, genoma in enumerate(self.genomas):
            score = self.webpage.testRoute(genoma)
            genoma.set_fitness(score)
            if score > self.best_fitness_score:
                self.best_fitness_score = score
                self.fittest_genome = i
            self.total_fitness_score += score

    def create_start_popualtion(self):
        for new in range(self.population_size):
            self.genomas.append(Genome(self.components_length, self.webpage.height))

    def epoch(self):
        self.update_fitness_score()

        new_babies = 0
        baby_genomes = list()

        while new_babies < self.population_size:
            mum = self.roulette_wheel_selection()
            dad = self.roulette_wheel_selection()
            baby1, baby2 = self.crossover(mum, dad)
            self.mutate(baby1)
            self.mutate(baby2)
            baby_genomes.append(baby1)
            baby_genomes.append(baby2)
            new_babies += 2

        self.genomas = baby_genomes
        self.generation += 1

    def render(self, wait_seconds=1, save=False):
        img = self.webpage.render(self.genomas[self.fittest_genome], wait_seconds)
        if save:
            cv2.imwrite('output.png', img)
