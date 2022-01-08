import random
import json

from genspa.constants import SCREEN_RES, PATTERN_DIR
from genspa.model.component import Component
from genspa.model.tools.icon_detect import findIconInImage
from genspa.model.tools.pattern_recognition import detect_big_image, detect_image_gallery, detect_banner, \
    detectBigTitle, detectAbout, detectBlank, detect_product_features, detect_big_button, detect_form
from genspa.util.logger_utils import getLogger


class Chromosome(dict):

    def __init__(self, component: Component, top, height_px=205*SCREEN_RES, position=0, prev_chromo=None, next_chromo=None):
        self.component = component
        self.top = top
        self.height = height_px
        self.score = -1
        self.position = position
        self.prev_chromo = prev_chromo
        self.next_chromo = next_chromo
        self.text = None
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.logger = getLogger()
        dict.__init__(self, name=component.name, top=top, height=height_px, score=0.0, position=position)


    """depending on the component, this function will calculate the value of fitness
    on the part of the image it is situated"""
    def fitness(self, site_image, scale=1) -> float:

        #crop image from top to height
        ih = site_image.shape[0]
        iw = site_image.shape[1]

        top_anchor = int(self.top)  #int(ih - self.top)
        if top_anchor < 0:
            return 0.0

        bottom_anchor = int(top_anchor + self.height)
        if bottom_anchor > ih:
            bottom_anchor = ih

        try:
            cropped = site_image[top_anchor:bottom_anchor, 0:int(iw)]
        except:
            print("ERROR:",top_anchor,bottom_anchor, int(iw))
            return 0.0

        if self.score > 0.0:
            return self.score

        #self.logger.debug(f"scoreComponent {self.component.name}")
        try:
            self.score = self.scoreComponent(cropped,scale=scale)
            super().__setitem__("score", self.score)
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
            base = detect_image_gallery(image, scale=scale)
            p_list = ["gal01_next.jpg", "gal02_next.jpg", "gal03_next.jpg", "gal04_next.jpg", "gal05_next.jpg"]
            add = findIconInImage(p_list, image)
            return base + add
        elif self.component == Component.BANNER:
            score = detect_banner(image, scale=scale)
            if score > 0 and self.position == 0 or (not self.next_chromo):
                score += 1.0
            return score
        elif self.component == Component.BIG_TITLE:
            return detectBigTitle(image, scale=scale)
        elif self.component == Component.BIG_BUTTONS:
            return detect_big_button(image, scale=scale)
        elif self.component == Component.ABOUT:
            return detectAbout(image, scale=scale)
        elif self.component == Component.TEXT_PARAGRAPH:
            return detectAbout(image, scale=scale, min_len=55, min_boxes=1, min_intros=2, min_box_height=175*SCREEN_RES)
        elif self.component == Component.PRODUCT_FEATURES:
            base = detect_product_features(image, scale=scale)
            p_list = ["like01_icon.jpg", "like02_icon.jpg"]
            add = findIconInImage(p_list, image)
            return base + add
        elif self.component == Component.BLANK:
            return detectBlank(image, scale=scale)
        elif self.component == Component.FORM:
            return detect_form(image, scale=scale)
        elif self.component == Component.VIDEO:
            p_list = ["play01.jpg", "play02.jpg"]
            return findIconInImage(p_list, image)
        elif self.component == Component.REVIEW:
            p_list = ["rating01_icon.jpg", "rating02_icon.jpg","rating03_icon.jpg", "rating04_icon.jpg", "rating05_icon.jpg"]
            return findIconInImage(p_list, image,anchorThreshold=7600000)
        elif self.component == Component.HEADER:
            p_list = ["menu_icon.jpg","cart_icon.jpg", "bag_icon.jpg"]
            res = findIconInImage(p_list, image)
            if self.position == 0:
                base = 6.0
                return base + res
            return res
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

    def to_json(self):
        return {
            "name": self.component.name,
            "score": self.score,
            "top": self.top,
            "height": self.height,
            "position": self.position,
        }

    #def toJSON(self):
    #    return json.dumps(self, default=lambda o: o.__dict__,
    #                      sort_keys=True, indent=4)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
