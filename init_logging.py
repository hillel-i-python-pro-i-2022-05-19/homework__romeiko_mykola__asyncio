import logging
import sys


def init_logging(is_verbose: bool = False):
    logging.basicConfig(
        stream=sys.stdout,
        format="[%(asctime)s.%(msecs)03d] "
               "[PROCESS %(process)d %(processName)s] "
               "%(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if is_verbose else logging.INFO,
    )