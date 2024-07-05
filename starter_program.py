import sys


if sys.platform.startswith("linux"):
    OPEN_COMMAND = "xdg-open"
elif sys.platform.startswith("windows"):
    OPEN_COMMAND = "start"
elif sys.platform == "darwin":
    OPEN_COMMAND = "open"
else:
    raise NotImplementedError(f"We do not know how to open URLs in {sys.platform} platform")
