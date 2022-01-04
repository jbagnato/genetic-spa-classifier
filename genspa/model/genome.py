import random

from genspa.model.chromosome import Chromosome
from genspa.model.component import Component


class Genome:

    def __init__(self, max_components=10, height_px=4096):
        self.components = list()
        self.fitness = 0.0
        prev_chromo = None
        prevTop=0
        for i in range(max_components):
            randomIncrement = random.randint(0, int(height_px/max_components))
            top = prevTop #(int(height_px/max_components)*i)
            height = int((height_px/max_components)/2) + randomIncrement
            prevTop = top + height
            chromo = Chromosome(random.choice(list(Component)),
                                top=top,
                                height_px=height,
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
