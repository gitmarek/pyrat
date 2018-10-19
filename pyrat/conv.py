import logging, sys

import numpy as np
from scipy import signal

from pyrat import logger

# TODO: check for empty files

def start(args):
    #logger.setLevel('INFO')

    if args.infile:
        infile= args.infile
    else:
        infile = sys.stdin

    logger.info(f'Reading file: {infile.name}')
    sig = np.fromfile(infile, dtype=np.float32)


    kerfile = args.kerfile
    logger.info(f'Reading kernel file: {args.kerfile.name}')
    ker = np.fromfile(args.kerfile, dtype=np.float32)

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
