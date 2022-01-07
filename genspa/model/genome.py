import copy
import random

from genspa.constants import SCREEN_RES
from genspa.model.chromosome import Chromosome
from genspa.model.component import Component


class Genome:

    def __init__(self, max_components=10, height_px=2048*SCREEN_RES, scale=1, skip_generation=False):
        self.components = list()
        self.fitness = 0.0
        self.scale = scale
        valid = False
        if not skip_generation:
            while not valid:
                generated = self.generateRandomGenoma(height_px, max_components)
                if self.testGenome(generated, scale):
                    self.components = self.fusion(generated)
                    valid = True

    def generateRandomGenoma(self, height_px, max_components) -> list:
        prev_chromo = None
        prevTop=0
        components = list()
        base_size = max(int(height_px / max_components), int(175*SCREEN_RES*self.scale))
        for i in range(max_components):
            randomIncrement = random.randint(0, base_size)
            top = prevTop  # (int(height_px/max_components)*i)
            height = int(base_size / 2) + randomIncrement
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

        badHeaders = [x for x in chromos if x.component == Component.HEADER and x.height>(350*SCREEN_RES)]
        if len(badHeaders)>1:
            return False

        footer = [x for x in chromos if x.component == Component.FOOTER]
        if len(footer)>1:
            return False

        banner = [x for x in chromos if x.component == Component.BANNER]
        if len(banner)>2:
            return False

        badBanner = [x for x in chromos if x.component == Component.BANNER and x.height > (225*SCREEN_RES*scale)]
        if len(badBanner)>0:
            return False

        bad_big_pic = [x for x in chromos if (x.component == Component.BIG_IMAGE) and (x.height < (200*SCREEN_RES*scale))]
        if len(bad_big_pic) > 0:
            return False

        about = [x for x in chromos if x.component == Component.ABOUT]
        if len(about)>2:
            return False

        blank = [x for x in chromos if x.component == Component.BLANK]
        if len(blank)>4:
            return False

        return True

    def copy(self):
        ncopied = list()
        for c in self.components:
            newC = copy.deepcopy(c)
            ncopied.append(newC)
        self.components = ncopied

        return self

    def fusion(self, chromos):
        to_delete=[]
        for i, chromo in enumerate(chromos):
            if chromo.next_chromo and chromo.next_chromo.component == chromo.component:
                to_delete.append(i)
                chromo.height = chromo.height + chromo.next_chromo.height
                # if there are more than 2
                chromo.next_chromo.top = chromo.top
                chromo.score = -1  # reset score

        chromos = [x for i, x in enumerate(chromos) if i not in to_delete]
        return chromos
