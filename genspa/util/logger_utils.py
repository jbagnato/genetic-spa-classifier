import logging


def getLogger(log_level="DEBUG", log_name='genspa', log_file=None) -> logging.Logger:
    logger = logging.getLogger(log_name)
    
    if not logger.handlers:
        logger.setLevel(log_level)
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        #logFormatter = logging.Formatter('%(asctime)s %(process)s %(thread)s - %(name)-12s - %(levelname)-8s - %(message)s in %(pathname)s:%(lineno)d - %(filename)s:%(funcName)s -')
        logFormatter = logging.Formatter('%(asctime)s - %(name)-8s %(levelname)-7s %(funcName)-16s %(message)s')
        ch.setFormatter(logFormatter)
        logger.addHandler(ch)
        logger.propagate = 0

        if log_file is not None:
            fileHandler = logging.FileHandler(log_file)
            fileHandler.setFormatter(logFormatter)
            logger.addHandler(fileHandler)

    return logger
