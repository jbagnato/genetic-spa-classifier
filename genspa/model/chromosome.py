from genspa.model.component import Component


class Chromosome:

    def __init__(self, component: Component, top, height_px=410):
        self.component = component
        self.top = top
        self.height = height_px

    """depending on the component, this function will calculate the value of fitness
    on the part of the image it is situated"""
    def fitness(self, site_image) -> float:
        return 0.0
