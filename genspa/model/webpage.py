import random

import cv2
import imutils
from alive_progress import alive_bar

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

            #TODO: validate not to have more than 1 header, and other rules that wont add score

            score += chromo.fitness(self.site_image.copy(),scale=self.scale)
            travel_px += chromo.height
            if bar:
                bar.text(f"{chromo.component.name} LAST SCORE: {score}")

        return score

    """Draw the components over the original image"""
    def render(self, path_list, wait_seconds=2):
        image = self.site_image.copy()

        # iterate chromosomas and draw each rectangle and color
        for chromo in path_list.components:
            top_anchor = chromo.top  #int(self.height - chromo.top)
            if top_anchor <= 0:
                top_anchor = 0

            bottom_anchor = int(top_anchor + chromo.height)
            if bottom_anchor > self.height:
                bottom_anchor = self.height

            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            thickness = int(14*self.scale)
            cv2.rectangle(image, (0+thickness, top_anchor+thickness), (self.width-thickness, bottom_anchor-thickness), color, thickness)
            font = cv2.FONT_HERSHEY_SIMPLEX
            # fontScale
            fontScale = max(int(3*self.scale),1)
            org = (30, bottom_anchor - 30)
            image = cv2.putText(image, str(chromo.component.name) , org, font, fontScale, color, thickness, cv2.LINE_AA)

        cv2.namedWindow('Image', cv2.WINDOW_GUI_NORMAL)  # WINDOW_AUTOSIZE WINDOW_NORMAL
        cv2.imshow("Image", image)
        cv2.waitKey(int(wait_seconds))
        return image
