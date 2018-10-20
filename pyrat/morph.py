import sys

import numpy as np
from scipy.fftpack import fft, ifft
from math import floor

from pyrat import logger


def start(args):

    infile= args.infile
    logger.info(f'Reading file: {infile.name}')
    a = np.fromfile(infile, dtype=np.float32)
    al = len(a)
    if al == 0:
        logger.error(f'The file {infile.name} does not contain any data')
        logger.error(f'Abort')
        sys.exit(1)
    logger.info(f'No. of samples: {al}')
    at_x = np.arange(al)
    at = fft(a)


    modfile = args.modfile
    logger.info(f'Reading file: {modfile.name}')
    m = np.fromfile(modfile, dtype=np.float32)
    ml = len(m)
    if ml == 0:
        logger.error(f'The file {modfile.name} does not contain any data')
        logger.error(f'Abort')
        sys.exit(1)
    logger.info(f'No. of samples: {ml}')
    mt_x = np.arange(ml)
    mt = fft(m)

    b = args.b
    if b == 0:
        rt = at
    elif b == 1:
        rt = mt
    else:
        rl = floor((1-b)*al + b*ml)
        rt = np.empty(rl)
        rt_x = np.arange(rl)

        # Interpolated arrays
        at_i = np.interp(rt_x, at_x, at)
        del at_x, at

        mt_i = np.interp(rt_x, mt_x, mt)
        del mt_x, mt

        rt = (1-b)*at_i + b*mt_i
        alpha, beta = (1-b)*(1-b), b*b
        rt = rt / np.abs(rt) * np.sqrt(
            alpha * np.power(np.abs(at_i),2) + 
            beta  * np.power(np.abs(mt_i),2)) 

    r = ifft(rt)

    # Normalize and remove offset
    r = (r - r.mean())/np.abs(r).max()

    outfile= args.outfile
    logger.info(f'Writing data: {outfile.name}')
    r.astype(np.float32).tofile(outfile)

    logger.info('Done.')
    sys.exit(0)
