import random
import joblib as jl

import cv2
import imutils
from alive_progress import alive_bar

from genspa.constants import SCREEN_RES
from genspa.model.genome import Genome


class Webpage:

    def __init__(self, site_image, width_px=None, height_px=None, scale=1):
        self.scale = scale
        resized = imutils.resize(site_image, width=int(site_image.shape[1] * scale))
        self.site_image = resized
        if not width_px:
            height_px = resized.shape[0]
            width_px = resized.shape[1]
        self.width = width_px
        self.height = height_px

    """Returns a fitness score proportional to the distance reached from the exit."""
    def testRoute(self, path:Genome, bar=None) -> float:
        score = 0.0
        travel_px = 0

        for chromo in path.components:
            if travel_px > self.height:
                break

            c_score = chromo.fitness(self.site_image.copy(), scale=self.scale)
            score += c_score
            travel_px += chromo.height
            if bar and c_score > 0.0:
                bar.text(f"{chromo.component.name} : {c_score}")

        path.set_fitness(score)
        #bar()
        return score

    """Draw the components over the original image"""
    def render(self, path_list, wait_seconds=2, skip_no_score=False):
        image = self.site_image.copy()

        skip_similar = False
        # iterate chromosomas and draw each rectangle and color
        for chromo in path_list.components:
            if skip_no_score and chromo.score <= 0:
                continue

            top_anchor = chromo.top  #int(self.height - chromo.top)
            if top_anchor <= 0:
                top_anchor = 0

            if chromo.next_chromo and chromo.next_chromo.component == chromo.component:
                bottom_anchor = int(top_anchor + chromo.next_chromo.height)
            else:
                bottom_anchor = int(top_anchor + chromo.height)

            if bottom_anchor > self.height:
                bottom_anchor = self.height

            if not skip_similar:
                color = chromo.color #(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                thickness = int(7*SCREEN_RES*self.scale)
                cv2.rectangle(image, (0+thickness, top_anchor+thickness), (self.width-thickness, bottom_anchor-thickness), color, thickness)
                font = cv2.FONT_HERSHEY_SIMPLEX
                # fontScale
                fontScale = max(int(1.5*SCREEN_RES*self.scale), 1)
                org = (int(15*SCREEN_RES), int(bottom_anchor - (15*SCREEN_RES)))
                image = cv2.putText(image, str(chromo.component.name) + " " + str(chromo.score), org, font, fontScale, color, thickness, cv2.LINE_AA)

            if chromo.next_chromo and chromo.next_chromo.component == chromo.component:
                skip_similar = True
            else:
                skip_similar = False

        cv2.namedWindow('Image', cv2.WINDOW_AUTOSIZE)  # WINDOW_AUTOSIZE WINDOW_NORMAL WINDOW_GUI_NORMAL
        cv2.imshow("Image", image)
        cv2.waitKey(int(wait_seconds))
        return image
