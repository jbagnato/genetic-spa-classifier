from genspa.model.component import Component
from genspa.model.tools.pattern_recognition import detect_big_image


class Chromosome:

    def __init__(self, component: Component, top, height_px=410):
        self.component = component
        self.top = top
        self.height = height_px

    """depending on the component, this function will calculate the value of fitness
    on the part of the image it is situated"""
    def fitness(self, site_image) -> float:

        #crop image from top to height
        ih = site_image.shape[0]
        iw = site_image.shape[1]

        top_anchor = int(ih - self.top)
        if top_anchor <= 0:
            return 0.0

        bottom_anchor = int(top_anchor - self.height)
        if bottom_anchor <= 0:
            bottom_anchor = 0

        cropped = site_image[bottom_anchor:top_anchor, 0:int(iw)]

        score = self.scoreComponent(cropped)

        return score

    def get_enum_component(self, num):
        switch = Component.__members__
        return switch.get(num, "Invalid input")

    def scoreComponent(self, image) -> float:
        if self.component == Component.BIG_IMAGE:
            return detect_big_image(image)
        return 0.0
