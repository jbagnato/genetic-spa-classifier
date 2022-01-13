import os
from time import sleep
# for saving gif
import imageio

import cv2
import imutils

from alive_progress import alive_bar

from genspa.constants import IMG_DIR, OUT_DIR, SCREEN_RES, EARLY_STOP
from genspa.model.chromosome import Chromosome
from genspa.model.component import Component
from genspa.model.genetic_spa import GeneticAlgorithmSPA
from genspa.model.tools.pattern_recognition import detectAbout
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
        if args.settingsFile == 'basic':
            urls = scrap.scrap_urls()
        elif args.settingsFile.startswith("http"):
            urls = args.settingsFile.split(",")
        else:
            try:
                settings = openConfig(args.settingsFile)
                urls = settings.get('sites')
            except ValueError:
                logger.error("Can not open Json file")

        scrap.captureWebsiteSceen(urls, delay=0.5)

    elif task == "train":

        logger.info(f"STARTING SPA GENETIC ALGORITHM")
        try:
            settings = openConfig(args.settingsFile)
            ga = settings.get('ga')
        except ValueError:
            logger.error("Can not open Json file")

        infor_every = ga.get("EPOCHS") / 25
        TOP_BEST_TO_ADD = ga.get("TOP_BEST_TO_ADD")
        NUM_BEST_TO_ADD = ga.get("NUM_BEST_TO_ADD")

        webimage = cv2.imread(IMG_DIR + args.image)
        if webimage is None:
            logger.error(f"Can not find image file {args.image}")
            return
        web = Webpage(webimage, scale=ga.get("scale"))

        logger.info(f"IMAGE readed: {web.width}px x {web.height}px")

        algo = GeneticAlgorithmSPA(web, ga.get("POP_SIZE"), ga.get("CROSSOVER_RATE"), ga.get("MUTATION_RATE"), ga.get("CHROMO_LENGTH"),TOP_BEST_TO_ADD,NUM_BEST_TO_ADD)
        totalEpochs = ga.get("EPOCHS")
        images = []
        best_score=0.0
        same=0
        with alive_bar(totalEpochs, title='PROCESSING') as bar:
            for i in range(totalEpochs):
                logger.info(f"EPOCH {i}/{ga.get('EPOCHS')}")
                done, img= algo.epoch(render=True, last=i == (totalEpochs-1) )

                color = (0, 0, 0)
                thickness = int(7*SCREEN_RES*web.scale)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = max(int(2.0*SCREEN_RES*web.scale), 1)
                org = (int(25*SCREEN_RES), int(25*SCREEN_RES))
                img = cv2.putText(img, str(i), org, font, fontScale, color, thickness, cv2.LINE_AA)

                images.append(img)
                #if i % infor_every == 0:
                #algo.render(wait_seconds=2)
                logger.debug(f"GENERATION SCORE: {algo.total_fitness_score}")
                logger.debug(f"FITTEST GENOMA: {algo.best_fitness_score}")

                if algo.best_fitness_score> best_score:
                    same=0
                else:
                    same +=1

                if same >= EARLY_STOP:
                    logger.info("EARLY STOP")
                    done = True

                bar()
                if done:
                    break

        logger.info(f"BEST GENOMA SCORE: {algo.best_fitness_score}")
        bestgen = algo.get_best_genoma()
        for chome in bestgen.components:
            logger.info(f"-- {chome.component.name}: {chome.score} - ({chome.top},{chome.height})")

        algo.render(save=True)
        algo.render(save=True, skip_no_score=True, filename=f"{OUT_DIR}output-{args.image}")
        imageio.mimsave(f"{OUT_DIR}output-{args.image[:-4]}.gif", images, fps=4)  # ,duration=0.8
        algo.saveJson(bestgen, filename=f"{OUT_DIR}output-{args.image[:-4]}.json")

        cv2.destroyAllWindows()
    elif task == "test":
        WAIT_SECONDS = 2

        scale = 1
        #height = int(820*scale)
        height = int(820*scale)
        chromo = Chromosome(Component.HEADER,0,height)
        webimage = cv2.imread(IMG_DIR + args.image)
        webimage = imutils.resize(webimage, width=int(webimage.shape[1] * scale))

        ih = webimage.shape[0]
        iw = webimage.shape[1]
        logger.info(f"IMAGE readed: {iw}px x {ih}px")
        for i in range(int(30)):
            offset = 0 + int(i*(height/3))
            print("OFFset", offset)
            cropped = webimage[offset:offset+height, 0:int(iw)]
            logger.info(f"CROPPED: {iw}px x {height}px offset: {offset}")
            score = chromo.scoreComponent(cropped, scale)
            #score = detectAbout(cropped, scale)
            logger.info(f"SCORE: {score}")
            #if score > 0:
            cv2.imshow('test', cropped)
            cv2.waitKey(WAIT_SECONDS)
            sleep(WAIT_SECONDS)
            break

        cv2.destroyAllWindows()

    elif task == "interactive":
        from genspa.use_cases.InteractiveCommandLine import InteractiveCommandLine
        ic = InteractiveCommandLine()
        ic.run(args.name)
    else:
        logger.error(f"No valid task: '{task}")


if __name__ == "__main__":
    main()
