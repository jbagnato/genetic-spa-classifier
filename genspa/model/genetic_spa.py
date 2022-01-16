import cv2
import copy
import concurrent.futures

from alive_progress import alive_bar

from genspa.constants import N_JOBS, MAX_SCORE_STOP, INVALID_GENOMA_RETRIES, SCREEN_RES
from genspa.model.chromosome import Chromosome
from genspa.model.component import Component
from genspa.model.genome import Genome
from genspa.model.webpage import Webpage

import random

from genspa.util.logger_utils import getLogger


class GeneticAlgorithmSPA:

    def __init__(self, webpage:Webpage, pop_size:int, cross_rate:float, muta_rate:float, components_length:int=10,TOP_BEST_TO_ADD=3, NUM_BEST_TO_ADD=2):
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
        self.logger = getLogger()
        self.TOP_BEST_TO_ADD=TOP_BEST_TO_ADD
        self.NUM_BEST_TO_ADD=NUM_BEST_TO_ADD


    def mutate(self, genoma:Genome, changeKind=True):
        valid = False
        retries = 0
        while (not valid) and retries < INVALID_GENOMA_RETRIES:
            new_components = genoma.clone()
            for i, chromo in enumerate(new_components):
                if (random.randint(0, 1000)/1000) < self.mutation_rate:
                    #self.logger.info("Mutation")
                    #flip the bit!
                    randomIncrement = random.randint(0, max(int(200*SCREEN_RES*self.webpage.scale), int(self.webpage.height / self.components_length)))

                    randomOperation = random.randint(0, 100)
                    if (randomOperation>50):
                        randomIncrement = -1*randomIncrement
                        if chromo.height + randomIncrement <= 0:
                            randomIncrement = 0
                    if changeKind:
                        kind = random.choice(list(Component))
                    else:
                        kind = chromo.component
                    newchromo = Chromosome(kind,
                                           top=chromo.top,
                                           height_px=int(chromo.height + randomIncrement),
                                           position=chromo.position,
                                           prev_chromo=chromo.prev_chromo,
                                           next_chromo=chromo.next_chromo)

                    # adjust the next chromos top and height position
                    nchrom = chromo.next_chromo
                    if nchrom:
                        prevtop = nchrom.top
                        nchrom.top = chromo.top + int(chromo.height + randomIncrement)
                        if nchrom.top >= prevtop:
                            nchrom.height = nchrom.height - (nchrom.top - prevtop)
                        else:
                            nchrom.height = nchrom.height + (prevtop - nchrom.top)
                        nchrom.score = -1

                    new_components[i] = newchromo

            valid = genoma.testGenome(new_components, self.webpage.scale)
            retries += 1

        if not valid:
            self.logger.warning("Mutation: not valid Genome")

        genoma.components = genoma.fusion(new_components)

    def crossover(self, mum:Genome, dad:Genome) -> (Genome, Genome):

        c1 = random.randint(0, min(len(mum.components), len(dad.components)))
        c2 = random.randint(0, min(len(mum.components), len(dad.components)))

        if ((random.randint(0, 100)/100) > self.crossover_rate) or (mum == dad) or (c1 == c2):
            return mum, dad

        baby1 = Genome(self.components_length, self.webpage.height, self.webpage.scale, skip_generation=True)
        baby2 = Genome(self.components_length, self.webpage.height, self.webpage.scale, skip_generation=True)

        comps1 = list()
        comps2 = list()
        lastTop1 = 0
        lastTop2 = 0
        prevChromo1=None
        prevChromo2=None
        for i in range(min(len(mum.components), len(dad.components))):
            if i != c1 and i != c2:
                chromo1 = copy.deepcopy(mum.components[i])
                chromo1.prev_chromo = prevChromo1
                if prevChromo1:
                    prevChromo1.next_chromo = chromo1
                comps1.append(chromo1)
                lastTop1 += chromo1.height
                prevChromo1 = chromo1
                chromo2 = copy.deepcopy(dad.components[i])
                chromo2.prev_chromo = prevChromo2
                if prevChromo2:
                    prevChromo2.next_chromo = chromo2
                comps2.append(chromo2)
                prevChromo2 = chromo2
                lastTop2 += chromo2.height
            else:
                # need to update the prev and next chromosomas
                # also have to adjust top and recalculate score
                chromo1 = copy.deepcopy(dad.components[i])
                chromo1.top = lastTop1
                lastTop1 += chromo1.height
                chromo1.score=-1  # reset score because the offset
                if prevChromo1:
                    prevChromo1.next_chromo=chromo1
                chromo1.prev_chromo = prevChromo1
                comps1.append(chromo1)
                prevChromo1 = chromo1
                chromo2 = copy.deepcopy(mum.components[i])
                chromo2.top = lastTop2
                lastTop2 += chromo2.height
                chromo2.score=-1  # reset score because the offset
                if prevChromo2:
                    prevChromo2.next_chromo=chromo2
                chromo2.prev_chromo = prevChromo2
                comps2.append(chromo2)
                prevChromo2 = chromo2

        baby1.components = comps1
        baby2.components = comps2

        return baby1, baby2

    def crossover0(self, mum:Genome, dad:Genome) -> (Genome, Genome):

        comps = min(len(mum.components), len(dad.components)) - 1

        if ((random.randint(0, 100)/100) > self.crossover_rate) or (mum == dad) or comps <= 6:
            return mum, dad

        #self.logger.info("Crossover")
        cut = random.randint(1, min(len(mum.components), len(dad.components))-1)#self.components_length-1)

        baby1 = Genome(self.components_length, self.webpage.height, self.webpage.scale, skip_generation=True)
        baby2 = Genome(self.components_length, self.webpage.height, self.webpage.scale, skip_generation=True)

        valid = False
        retries = 0
        while (not valid) and retries < INVALID_GENOMA_RETRIES:#(self.components_length):
            comps1 = list()
            used = []
            comps2 = list()
            used2 = []
            lastTop1 = 0
            lastTop2 = 0
            prevChromo1=None
            prevChromo2=None
            for i in range(min(len(mum.components), len(dad.components))):#self.components_length):
                if i < cut:
                    chromo1 = copy.deepcopy(mum.components[i])
                    #if chromo1.score == 0:
                    #    chromo1.component = mum.transitions[chromo1.component]
                    used.append(chromo1.component)
                    chromo1.prev_chromo = prevChromo1
                    if prevChromo1:
                        prevChromo1.next_chromo = chromo1
                    comps1.append(chromo1)

                    lastTop1 += chromo1.height
                    prevChromo1 = chromo1

                    chromo2 = copy.deepcopy(dad.components[i])
                    #if chromo2.score == 0:
                    #    chromo2.component = dad.transitions[chromo2.component]
                    used2.append(chromo2.component)
                    chromo2.prev_chromo = prevChromo2
                    if prevChromo2:
                        prevChromo2.next_chromo = chromo2

                    comps2.append(chromo2)

                    prevChromo2 = chromo2
                    lastTop2 += chromo2.height
                else:
                    # need to update the prev and next chromosomas
                    # also have to adjust top and recalculate score
                    chromo1 = copy.deepcopy(dad.components[i])
                    #if chromo1.score == 0:
                    #    chromo1.component = mum.transitions[chromo1.component]

                    chromo1.top = lastTop1
                    lastTop1 += chromo1.height

                    chromo1.score=-1  # reset score because the offset
                    if prevChromo1:
                        prevChromo1.next_chromo=chromo1
                    chromo1.prev_chromo = prevChromo1

                    #if mum.more_than(used, chromo1.component, 2):
                    #    chromo1.component = Component.BLANK
                    #else:
                    #    used.append(chromo1.component)

                    comps1.append(chromo1)
                    prevChromo1 = chromo1

                    chromo2 = copy.deepcopy(mum.components[i])
                    #if chromo2.score == 0:
                    #    chromo2.component = dad.transitions[chromo2.component]

                    chromo2.top = lastTop2
                    lastTop2 += chromo2.height
                    chromo2.score=-1  # reset score because the offset
                    if prevChromo2:
                        prevChromo2.next_chromo=chromo2
                    chromo2.prev_chromo = prevChromo2

                    #if dad.more_than(used2, chromo2.component, 2):
                    #    chromo2.component = Component.BLANK
                    #else:
                    #    used2.append(chromo2.component)

                    comps2.append(chromo2)
                    prevChromo2 = chromo2

            valid = baby1.testGenome(comps1, self.webpage.scale) and baby2.testGenome(comps2, self.webpage.scale)
            retries += 1

        if not valid:
            self.logger.warning("Crossover: not valid Genome")

        baby1.components = comps1 #baby1.fusion(comps1)
        baby2.components = comps2 #baby2.fusion(comps2)

        return baby1, baby2

    def roulette_wheel_selection(self) -> Genome:
        slice = random.randint(0, 100)/100 * self.total_fitness_score
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

        with concurrent.futures.ThreadPoolExecutor(max_workers=N_JOBS) as executor:
            for score in executor.map(self.webpage.testRoute, self.genomas):
                if score > self.best_fitness_score:
                    self.best_fitness_score = score
                self.total_fitness_score += score

        for i, gen in enumerate(self.genomas):
            if gen.fitness == self.best_fitness_score:
                self.fittest_genome = i
                break

    def create_start_popualtion(self):
        for new in range(self.population_size):
            self.genomas.append(Genome(self.components_length, self.webpage.height, self.webpage.scale))

    def epoch(self, render=False, last=False):
        self.update_fitness_score()
        img = None
        if render:
            img = self.render(2)
            bestgen = self.get_best_genoma()
            for chome in bestgen.components:
                self.logger.info(f"-- {chome.component.name}: {chome.score} - ({chome.top},{chome.height}) - {chome.top + chome.height}")

        if self.best_fitness_score >= (MAX_SCORE_STOP * self.components_length) or last:
            # we found best posible solution
            return True, img

        self.logger.info("GENERATING NEW POPULATION")
        baby_genomes = list()

        # To return a new list, use the sorted() built-in function...
        orderedlist = sorted(self.genomas, key=lambda x: x.fitness, reverse=True)
        for i in range(self.TOP_BEST_TO_ADD):
            for j in range(self.NUM_BEST_TO_ADD):
                genome = copy.deepcopy(orderedlist[i])
                genome.components = genome.clone() #copy.deepcopy(orderedlist[i]).copy()
                genome.changeZeroKind()
                baby_genomes.append(genome)

        while len(baby_genomes) < self.population_size:
            mum = self.roulette_wheel_selection()
            dad = self.roulette_wheel_selection()
            baby1, baby2 = self.crossover(mum, dad)
            self.mutate(baby1, changeKind=False)
            self.mutate(baby2, changeKind=False)
            baby1.changeZeroKind()
            baby2.changeZeroKind()
            baby_genomes.append(baby1)
            baby_genomes.append(baby2)

        self.genomas = baby_genomes
        self.generation += 1

        return False, img

    def render(self, wait_seconds=1, save=False, skip_no_score=False, filename='output.png'):
        img = self.webpage.render(self.genomas[self.fittest_genome], wait_seconds, skip_no_score=skip_no_score)
        if save:
            cv2.imwrite(filename, img)
        return img

    def get_best_genoma(self):
        return self.genomas[self.fittest_genome]

    def saveJson(self, bestgen:Genome, filename:str):
        import json
        with open(filename, 'w') as f:
            f.write(json.dumps(bestgen.components, indent=4))

