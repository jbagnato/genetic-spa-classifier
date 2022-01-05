from genspa.model.component import Component
from genspa.model.tools.pattern_recognition import detect_big_image, detect_image_gallery, detect_banner, \
    detectBigTitle, detectAbout, detectBlank, detect_product_features
from genspa.util.logger_utils import getLogger


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
        self.logger = getLogger()

    """depending on the component, this function will calculate the value of fitness
    on the part of the image it is situated"""
    def fitness(self, site_image, scale=1) -> float:

        #crop image from top to height
        ih = site_image.shape[0]
        iw = site_image.shape[1]

        top_anchor = self.top  #int(ih - self.top)
        if top_anchor < 0:
            return 0.0

        bottom_anchor = int(top_anchor + self.height)
        if bottom_anchor > ih:
            bottom_anchor = ih

        cropped = site_image[top_anchor:bottom_anchor, 0:int(iw)]

        if self.score > 0.0:
            return self.score

        #self.logger.debug(f"scoreComponent {self.component.name}")
        try:
            self.score = self.scoreComponent(cropped,scale=scale)
        except:
            self.score = 0.0
        #self.logger.debug(f"END scoreComponent: {self.score}")

        return self.score

    def get_enum_component(self, num):
        switch = Component.__members__
        return switch.get(num, "Invalid input")

    def scoreComponent(self, image,scale=1) -> float:
        if self.component == Component.BIG_IMAGE:
            return detect_big_image(image, scale=scale)
        elif self.component == Component.IMAGE_GALLERY:
            return detect_image_gallery(image, scale=scale)
        elif self.component == Component.BANNER:
            score = detect_banner(image, scale=scale)
            if score > 0 and self.position == 0 or (not self.next_chromo):
                score += 1.0
            return score
        elif self.component == Component.BIG_TITLE:
            return detectBigTitle(image, scale=scale)
        elif self.component == Component.ABOUT:
            return detectAbout(image, scale=scale)
        elif self.component == Component.TEXT_PARAGRAPH:
            return detectAbout(image, scale=scale, min_len=60, min_boxes=1, min_intros=3, min_box_height=350)
        elif self.component == Component.PRODUCT_FEATURES:
            return detect_product_features(image,scale=scale)
        elif self.component == Component.BLANK:
            return detectBlank(image, scale=scale)
        elif self.component == Component.HEADER:
            if self.position == 0:
                return 10.0
        elif self.component == Component.FOOTER:
            if not self.next_chromo:
                return 8.0

        return 0.0

    def __str__(self):
        if self.component:
            return self.component.name + ", " + str(self.score)
        else:
            return "Chromosome, not initialized"

    def __repr__(self):
        if self.component:
            return self.component.name + ", " + str(self.score)
        else:
            return "Chromosome, not initialized"
