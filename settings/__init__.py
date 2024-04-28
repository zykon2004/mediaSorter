import os

match os.environ["ENV"]:
    case "DEV":
        from .dev import *  # noqa: F403
    case "PROD", _:
        from .prod import *  # noqa: F403
