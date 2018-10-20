PROGNAME='pyrat'
VERSION='0.1.1'

import logging
LOGGING_FORMAT = '%(asctime)-15s ' + PROGNAME + ' (%(process)d): %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
logger = logging.getLogger(__name__)
