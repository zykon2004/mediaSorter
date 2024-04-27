import os

match os.environ["ENV"]:
    case "DEV":
        from .dev import *
    case "PROD", _:
        from .prod import *
