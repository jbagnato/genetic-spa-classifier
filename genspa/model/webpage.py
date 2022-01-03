import cv2

from genspa.model.genome import Genome


class Webpage:

    def __init__(self, site_image, width_px=None, height_px=None):
        self.site_image = site_image
        if not width_px:
            height_px = site_image.shape[0]
            width_px = site_image.shape[1]
        self.width = width_px
        self.height = height_px

    """Returns a fitness score proportional to the distance reached from the exit."""
    def testRoute(self, path:Genome) -> float:
        score = 0.0
        travel_px = 0
        for chromo in path.components:
            if travel_px > self.height:
                break

            #TODO: validate not to have more than 1 header, and other rules that wont add score

            score += chromo.fitness(self.site_image)
            travel_px += chromo.height

        return score

    """Draw the components over the original image"""
    def render(self, path_list, wait_seconds=2):
        image = self.site_image.copy()

        # iterate chromosomas and draw each rectangle and color
        for chromo in path_list.components:
            top_anchor = int(self.height - chromo.top)
            if top_anchor <= 0:
                top_anchor = 0

            bottom_anchor = int(top_anchor - chromo.height)
            if bottom_anchor <= 0:
                bottom_anchor = 0

            color = (0, 0, 255)
            thickness = 4
            cv2.rectangle(image, (0, self.width), (bottom_anchor, top_anchor), color, thickness)
            font = cv2.FONT_HERSHEY_SIMPLEX
            # fontScale
            fontScale = 1
            org = (10, bottom_anchor + 10)
            image = cv2.putText(image, str(chromo.component) , org, font,
                                fontScale, color, thickness, cv2.LINE_AA)

        cv2.namedWindow('Image', cv2.WINDOW_GUI_NORMAL)  # WINDOW_AUTOSIZE WINDOW_NORMAL
        cv2.imshow("Image", image)
        cv2.waitKey(int(wait_seconds))

