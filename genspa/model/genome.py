import random

from genspa.model.chromosome import Chromosome
from genspa.model.component import Component


class Genome:

    def __init__(self, max_components=10, height_px=4096, scale=1, skip_generation=False):
        self.components = list()
        self.fitness = 0.0
        self.scale = scale
        valid = False
        if not skip_generation:
            while not valid:
                generated = self.generateRandomGenoma(height_px, max_components)
                if self.testGenome(generated, scale):
                    self.components = generated
                    valid = True

    def generateRandomGenoma(self, height_px, max_components) -> list:
        prev_chromo = None
        prevTop=0
        components = list()
        for i in range(max_components):
            randomIncrement = random.randint(0, int(height_px / max_components))
            top = prevTop  # (int(height_px/max_components)*i)
            height = int((height_px / max_components) / 2) + randomIncrement
            prevTop = top + height
            chromo = Chromosome(random.choice(list(Component)),
                                top=top,
                                height_px=height,
                                position=i,
                                prev_chromo=prev_chromo,
                                next_chromo=None
                                )
            components.append(chromo)
            if prev_chromo:
                prev_chromo.next_chromo = chromo
            prev_chromo = chromo

        return components

    def set_fitness(self, value:float):
        self.fitness=value

    def reset(self):
        self.components = list()
        self.fitness = 0.0
        return self

    def testGenome(self, chromos, scale):
        headers = [x for x in chromos if x.component == Component.HEADER]
        if len(headers)>1:
            return False

        footer = [x for x in chromos if x.component == Component.FOOTER]
        if len(footer)>1:
            return False

        banner = [x for x in chromos if x.component == Component.BANNER]
        if len(banner)>2:
            return False

        badBanner = [x for x in chromos if x.component == Component.BANNER and x.height > (450*scale)]
        if len(badBanner)>0:
            return False

        about = [x for x in chromos if x.component == Component.ABOUT]
        if len(about)>2:
            return False

        return True
