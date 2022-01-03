from genspa.model.genome import Genome


class Webpage:

    def __init__(self, site_image, width_px=1024, height_px=4096):
        self.site_image = site_image
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
    def render(self, path_list):
        pass
