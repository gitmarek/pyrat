import logging, sys

import numpy as np
from scipy import signal

from pyrat import logger


def start(args):

    if args.infile:
        infile= args.infile
    else:
        infile = sys.stdin

    logger.info(f'Reading file: {infile.name}')
    sig = np.fromfile(infile, dtype=np.float32)

    if len(sig) == 0:
        logger.error(f'The file {infile.name} does not contain any data')
        logger.error(f'Abort')
        sys.exit(1)

    kerfile = args.kerfile
    logger.info(f'Reading kernel file: {args.kerfile.name}')
    ker = np.fromfile(args.kerfile, dtype=np.float32)

    if len(ker) == 0:
        logger.error(f'The file {kerfile.name} does not contain any data')
        logger.error(f'Abort')
        sys.exit(1)

    logger.info('Performing fft convolution')
    result = signal.fftconvolve(sig, ker, mode='full')

    logger.info('Normalizing the result')
    result = (result - result.mean())/result.max()

    if args.outfile:
        outfile= args.outfile
    else:
        outfile = sys.stdout
    logger.info(f'Writing data: {outfile.name}')
    result.astype(np.float32).tofile(outfile)

    sys.exit(0)
