import os
from time import sleep

import cv2

from alive_progress import alive_bar

from genspa.constants import IMG_DIR
from genspa.model.chromosome import Chromosome
from genspa.model.component import Component
from genspa.model.genetic_spa import GeneticAlgorithmSPA
from genspa.model.webpage import Webpage
from genspa.use_cases.SPAScrap import SPAScrap
from genspa._argument_parser import parse_args
from genspa.util.json_utils import openConfig
from genspa.util.logger_utils import getLogger


def main():
    """Main entry point.

    This function is called when you execute the module
    (for example using `ingesta` or `python -m ingesta`).
    """
    args = parse_args()
    
    logger = getLogger(log_level=args.log_level, log_file=args.log_file)
    task = args.task

    ENVIRONMENT = os.getenv('ENVIRONMENT')
    if ENVIRONMENT is not None:
        args.environment = ENVIRONMENT

    if task == "scrap":
        scrap = SPAScrap()
        if args.jsonFile == 'basic':
            urls = scrap.scrap_urls()
        elif args.jsonFile.startswith("http"):
            urls = args.jsonFile.split(",")
        else:
            try:
                settings = openConfig(args.jsonFile)
                urls = settings.get('sites')
            except ValueError:
                logger.error("Can not open Json file")

        scrap.captureWebsiteSceen(urls, delay=0.5)
    elif task == "train":
        logger.info(f"STARTING SPA GENETIC ALGORITHM")
        #TODO: read config from json
        CROSSOVER_RATE = 0.7
        MUTATION_RATE = 0.001
        POP_SIZE = 110
        CHROMO_LENGTH = 10
        EPOCHS = 105
        infor_every = EPOCHS / 25

        scale = 0.35

        webimage = cv2.imread(IMG_DIR + args.image)
        if webimage is None:
            logger.error(f"Can not find image file {args.image}")
            return
        web = Webpage(webimage, scale=scale)

        logger.info(f"IMAGE readed: {web.width}px x {web.height}px")

        algo = GeneticAlgorithmSPA(web, POP_SIZE, CROSSOVER_RATE, MUTATION_RATE, CHROMO_LENGTH)
        with alive_bar(EPOCHS, title='Processing') as bar:
            for i in range(EPOCHS):
                algo.epoch()
                if i % infor_every == 0:
                    algo.render(wait_seconds=2)
                    bar.text(f"GENERATION SCORE: {algo.total_fitness_score}")
                bar()

        logger.info(f"GENOMA FINAL BEST SCORE: {algo.best_fitness_score}")
        algo.render(save=True)
        cv2.destroyAllWindows()
    elif task == "test":
        height = 820
        chromo = Chromosome(Component.BIG_IMAGE,0,height)
        scale = 1
        webimage = cv2.imread(IMG_DIR + args.image)
        ih = webimage.shape[0]
        iw = webimage.shape[1]
        logger.info(f"IMAGE readed: {iw}px x {ih}px")
        cropped = webimage[0:height, 0:int(iw)]
        score = chromo.scoreComponent(cropped, scale)
        logger.info(f"SCORE: {score}")
        cv2.imshow('test', cropped)
        WAIT_SECONDS = 6
        cv2.waitKey(WAIT_SECONDS)
        sleep(WAIT_SECONDS)
        cv2.destroyAllWindows()

    elif task == "interactive":
        from genspa.use_cases.InteractiveCommandLine import InteractiveCommandLine
        ic = InteractiveCommandLine()
        ic.run(args.name)
    else:
        logger.error(f"No valid task: '{task}")


if __name__ == "__main__":
    main()
