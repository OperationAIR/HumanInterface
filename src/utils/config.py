import os
from pathlib import Path

import yaml


class ConfigValues():

    class __ConfigValues:
        def __init__(self):
            print("Reading file")
            self.values = self.read_config()

        def __str__(self):
            return repr(self)

        def read_config(self):
            ROOT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)
            with open(ROOT_DIR + "/config/config.yml", 'r') as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

    instance = None

    def __init__(self):
        if not ConfigValues.instance:
            ConfigValues.instance = ConfigValues.__ConfigValues()

    def __getattr__(self, name):
        return getattr(self.instance, name)

