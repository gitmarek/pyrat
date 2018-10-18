import logging

import numpy as np
from scipy import signal

from pyrat import logger

# TODO: check for empty files

def start(args):
    #logger.setLevel('INFO')

    logger.info(f'Reading file: {args.infile}')
    sig = np.fromfile(args.infile, dtype=np.float32)

    logger.info(f'Reading file: {args.kerfile}')
    ker = np.fromfile(args.kerfile, dtype=np.float32)

    logger.info('Performing fft convolution')
    result = signal.fftconvolve(sig, ker, mode='full')

    logger.info('Normalizing the result')
    result = (result - result.mean())/result.max()

    logger.info(f'Writing data: {args.outfile}')
    result.astype(np.float32).tofile(args.outfile)

    exit(0)
