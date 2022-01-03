import random

from genspa.model.chromosome import Chromosome
from genspa.model.component import Component


class Genome:

    def __init__(self, max_components=10, height_px=4096):
        self.components = list()
        self.fitness = 0.0
        prev_chromo = None
        for i in range(max_components):
            chromo = Chromosome(random.choice(list(Component)),
                                top=(int(height_px/max_components)*i),
                                height_px=int(height_px/max_components),
                                position=i,
                                prev_chromo=prev_chromo,
                                next_chromo=None
            )
            self.components.append(chromo)
            if prev_chromo:
                prev_chromo.next_chromo = chromo
            prev_chromo=chromo

    def set_fitness(self, value:float):
        self.fitness=value

    def reset(self):
        self.components = list()
        self.fitness = 0.0
        return self
