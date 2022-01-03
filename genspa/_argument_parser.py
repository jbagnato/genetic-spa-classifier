import argparse

parser = argparse.ArgumentParser(description=r"""
Genetic Single Page App's Classifier
""", formatter_class=argparse.RawTextHelpFormatter)

#####################
# Common arguments. #
#####################
parser.add_argument("-l", "--logging-level", dest="log_level", default="DEBUG",
                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                    help="Logging level.")
parser.add_argument("-lf", "--logging-file", dest="log_file", default=None,
                    help="Logging file. By default std out is use.")

parser.add_argument("-env", "--environment", dest="environment", default="develop", 
                    choices=["develop", "testing", "production"],
                    help="Environment: develop,testing,production")


###############
# Subparsers. #
###############
subparsers = parser.add_subparsers(dest="task")
subparsers.required = True
# Preprocessing subparser
preprocess_parser = subparsers.add_parser("scrap", help="visit list of websites and take snapshot.")
preprocess_parser.add_argument("jsonFile", nargs='?', default="basic", help="Optional. Specify a json settings file.")

# Preprocessing subparser
preprocess_parser = subparsers.add_parser("train", help="run GA")
preprocess_parser.add_argument("settingsFile", help="JSON settings file.")
preprocess_parser.add_argument("image", help="path to site PNG image.")

preprocess_parser = subparsers.add_parser("interactive", help="Interactive command line utility")

def parse_args(*args, **kwargs):
  return parser.parse_args(*args, **kwargs)
