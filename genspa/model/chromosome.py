from genspa.model.component import Component
from genspa.model.tools.pattern_recognition import detect_big_image, detect_image_gallery, detect_banner, \
    detectBigTitle, detectAbout


class Chromosome:

    def __init__(self, component: Component, top, height_px=410, position=0, prev_chromo=None, next_chromo=None):
        self.component = component
        self.top = top
        self.height = height_px
        self.score = -1
        self.position = position
        self.prev_chromo = prev_chromo
        self.next_chromo = next_chromo
        self.text = None

    """depending on the component, this function will calculate the value of fitness
    on the part of the image it is situated"""
    def fitness(self, site_image, scale=1) -> float:

        #crop image from top to height
        ih = site_image.shape[0]
        iw = site_image.shape[1]

        top_anchor = self.top  #int(ih - self.top)
        if top_anchor <= 0:
            return 0.0

        bottom_anchor = int(top_anchor + self.height)
        if bottom_anchor > ih:
            bottom_anchor = ih

        cropped = site_image[top_anchor:bottom_anchor, 0:int(iw)]

        if self.score > 0:
            return self.score

        self.score = self.scoreComponent(cropped,scale=scale)

        return self.score

    def get_enum_component(self, num):
        switch = Component.__members__
        return switch.get(num, "Invalid input")

    def scoreComponent(self, image,scale=1) -> float:
        if self.component == Component.BIG_IMAGE:
            return detect_big_image(image,scale=scale)
        elif self.component == Component.IMAGE_GALLERY:
            return detect_image_gallery(image,scale=scale)
        elif self.component == Component.BANNER:
            return detect_banner(image,scale=scale)
        elif self.component == Component.BIG_TITLE:
            return detectBigTitle(image,scale=scale)
        elif self.component == Component.ABOUT:
            return detectAbout(image,scale=scale)

        return 0.0
