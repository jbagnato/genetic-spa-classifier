import os
import json

def openConfig(filepath: str) -> dict:
    """ opens the json configuration file  """
    if isinstance(filepath, str) and os.path.exists(filepath):
        with open(filepath, 'r') as myfile:
            data = myfile.read()

        # parse file
        obj = json.loads(data)

        return obj

    raise Exception(f"Can not find required config file in path: {filepath}")
