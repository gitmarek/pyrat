name='pyrat'
version='0.2'

import logging
LOGGING_FORMAT = '%(asctime)-15s ' + name + ' (%(process)d): %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
logger = logging.getLogger(__name__)
