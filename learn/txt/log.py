import logging
import sys
import traceback

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='c.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def error(e, limit=None, file=None, chain=True):
    # http://docs.python.org/2/library/sys.html#sys.exc_info
    etype, value, tb = sys.exc_info()  # most recent (if any) by default
    rtn = ''
    for line in traceback.TracebackException(
            type(value), value, tb, limit=limit).format(chain=chain):
        rtn += line

    logging.error(rtn)
