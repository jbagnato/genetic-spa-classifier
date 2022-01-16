import copy
import random

from genspa.constants import SCREEN_RES
from genspa.model.chromosome import Chromosome
from genspa.model.component import Component


class Genome:

    def __init__(self, max_components=10, height_px=2048*SCREEN_RES, scale=1, skip_generation=False):
        self.components = list()
        self.transitions = {
            #Component.BLANK : Component.BANNER,
            Component.BANNER : Component.BIG_IMAGE,
            Component.BIG_IMAGE: Component.BIG_BUTTONS,
            Component.BIG_BUTTONS: Component.BIG_TITLE,
            Component.BIG_TITLE: Component.ABOUT,
            Component.ABOUT: Component.FORM,
            Component.FORM: Component.IMAGE_GALLERY,
            Component.IMAGE_GALLERY: Component.PRODUCT_FEATURES,
            Component.PRODUCT_FEATURES: Component.REVIEW,
            Component.REVIEW: Component.TEXT_PARAGRAPH,
            Component.TEXT_PARAGRAPH: Component.VIDEO,
            Component.VIDEO: Component.BANNER
        }

        self.fitness = 0.0
        self.scale = scale
        self.screen_height = height_px
        self.max_components = max_components
        valid = False
        if not skip_generation:
            retries=0
            while not valid and retries < 4000:
                generated = self.generateRandomGenoma(height_px, max_components)
                if self.testGenome(generated, scale):
                    self.components = generated  #self.fusion(generated)
                    valid = True
                retries+=1
            if not valid:
                print("Invalid Genoma")
                self.components = generated

    def generateRandomGenoma(self, height_px, max_components) -> list:
        prev_chromo = None
        prevTop=0
        components = list()
        base_size = max(int(height_px / max_components), int(200*SCREEN_RES*self.scale))
        used=[]
        for i in range(max_components):
            randomIncrement = random.randint(0, max(int(300*SCREEN_RES*self.scale),base_size))
            top = prevTop  # (int(height_px/max_components)*i)
            height = int(base_size / 2) + randomIncrement
            if i == 0:
                kind = Component.HEADER
                height = min(height, int(300*SCREEN_RES*self.scale))
            elif i == (max_components - 1):
                kind = Component.FOOTER
                height = min(height, int(300*SCREEN_RES*self.scale))
            else:
                kind = random.choice(list(Component))
                while kind == Component.HEADER or kind == Component.FOOTER:
                    kind = random.choice(list(Component))

            #if self.more_than(used, kind, 2):
            #    kind = Component.BLANK

            if kind == Component.BANNER:
                height = min(height, int(225*SCREEN_RES*self.scale))

            if kind == Component.BIG_IMAGE:
                height = max(height, int(200*SCREEN_RES*self.scale))

            prevTop += height

            chromo = Chromosome(kind,
                                top=top,
                                height_px=height,
                                position=i,
                                prev_chromo=prev_chromo,
                                next_chromo=None
                                )
            used.append(kind)
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
        if len(headers) > 1:
            return False

        if len(headers) == 1 and headers[0].height>(350*SCREEN_RES*scale):
            return False

        footer = [x for x in chromos if x.component == Component.FOOTER]
        if len(footer) > 1:
            return False

        gal = [x for x in chromos if x.component == Component.IMAGE_GALLERY]
        if len(gal) > 2:
            return False

        vid = [x for x in chromos if x.component == Component.VIDEO]
        if len(vid) > 1:
            return False

        form = [x for x in chromos if x.component == Component.FORM]
        if len(form) > 1:
            return False

        review = [x for x in chromos if x.component == Component.REVIEW]
        if len(review) > 1:
            return False

        banner = [x for x in chromos if x.component == Component.BANNER]
        if len(banner) > 2:
            return False

        badBanner = [x for x in chromos if x.component == Component.BANNER and x.height > (250*SCREEN_RES*scale)]
        if len(badBanner) > 0:
            return False

        bad_big_pic = [x for x in chromos if (x.component == Component.BIG_IMAGE) and (x.height < (200*SCREEN_RES*scale))]
        if len(bad_big_pic) > 0:
            return False

        about = [x for x in chromos if x.component == Component.ABOUT]
        if len(about) > 2:
            return False

        blank = [x for x in chromos if x.component == Component.BIG_BUTTONS]
        if len(blank) > 4:
            return False

        return True

    def copy(self):
        ncopied = list()
        prev = None
        for c in self.components:
            newC = copy.deepcopy(c)
            newC.prev_chromo = prev
            if prev:
                prev.next_chromo = newC
            ncopied.append(newC)
            prev = newC
        self.components = ncopied

        return self

    def clone(self):
        ncopied = list()
        prev = None
        for c in self.components:
            newC = copy.deepcopy(c)
            newC.prev_chromo = prev
            if prev:
                prev.next_chromo = newC
            ncopied.append(newC)
            prev = newC

        return ncopied

    def fusion(self, chromos, reposition=False):
        to_delete = []
        if len(chromos)<=6:
            return chromos

        for i, chromo in enumerate(chromos):
            if chromo.next_chromo and chromo.next_chromo.component == chromo.component:
                to_delete.append(i)
                chromo.height = chromo.height + chromo.next_chromo.height
                # if there are more than 2
                chromo.next_chromo.top = chromo.top
                chromo.next_chromo.height = chromo.height
                chromo.score = -1  # reset score

        chromos = [x for i, x in enumerate(chromos) if i not in to_delete]

        if reposition:
            # complete with blank blocks at the end
            for i in range(len(to_delete)):
                chromo = Chromosome(Component.BANNER, # BLANK
                                top=self.screen_height,
                                height_px=100,
                                position= self.max_components - i,
                                prev_chromo=None,
                                next_chromo=None
                                )
                chromos.append(chromo)

        return chromos

    def more_than(self, used, kind, qty):
        review = [x for x in used if x == kind] #and kind != Component.BLANK]
        if len(review) > (qty-1):
            return True

        return False

    def changeZeroKind(self, change=7):
        """change in a predefined order the zero values to try to get value"""

        detected=0
        for chromo in self.components:
            if chromo.score == 0:
                chromo.component = self.transitions[chromo.component]
                chromo.score = -1
                detected +=1

            if detected>=change:
                break
