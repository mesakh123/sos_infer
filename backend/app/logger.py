import logging
from os import path
logging.root.handlers = []
logging.root.setLevel(logging.INFO)
for name in logging.root.manager.loggerDict.keys():
    logging.getLogger(name).handlers = []
    logging.getLogger(name).propagate = True


curr_logger = logging.getLogger(__name__)
uvicorn_access_logger = logging.getLogger("uvicorn.access")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )
)
logging.root.addHandler(handler)
