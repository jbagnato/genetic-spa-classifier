import os
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
    
    getLogger(log_level=args.log_level, log_file=args.log_file)
    task = args.task

    ENVIRONMENT = os.getenv('ENVIRONMENT')
    if ENVIRONMENT is not None:
        args.environment = ENVIRONMENT
    DATAACCESS = os.getenv('DATAACCESS')
    if DATAACCESS is not None:
        args.data_access = DATAACCESS

    if task == "scrap":
        scrap = SPAScrap()
        if args.jsonFile:
            settings = openConfig(args.jsonFile)
            urls = settings.get('sites')
        else:
            #urls = scrap.scrap_urls()
            pass
        scrap.captureWebsiteSceen(urls, delay=0.5)
    elif task == "train":
        facade = SPAScrap()
    elif task == "interactive":
        from genspa.use_cases.InteractiveCommandLine import InteractiveCommandLine
        ic = InteractiveCommandLine()
        ic.run(args.name)
    else:
        print("No valid task '{task}'")

if __name__ == "__main__":
    main()
