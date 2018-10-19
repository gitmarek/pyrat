import sys
import numpy as np
from scipy.fftpack import fft, ifft

from pyrat import logger


def start(args):

    if args.infile:
        infile= args.infile
    else:
        infile = sys.stdin

    logger.info(f'Reading file: {infile.name}')
    a = np.fromfile(infile, dtype=np.float32)
    l = len(a)

    if l == 0:
        logger.error(f'The file {infile.name} does not contain any data')
        logger.error(f'Abort')
        sys.exit(1)

    logger.info(f'No. of samples: {l}')

    # For the sake of convenience, drop one sample if the length is even
    if l % 2 == 0:
        logger.info('The no. of samples is even. Drop the last sample...')
        l -= 1
        a = a[:-1]

    logger.info('Computing fft')
    at = fft(a)

    # Actually, due to rounding error, some of the elements
    # may have absulute value slightly diffrerent than 1.
    # The input signal is real, so we need only (l-1)//2 phases
    logger.info(f'Randomize phases with b={args.b}')
    phase_exp = 2j*np.pi
    pt = np.exp(phase_exp*np.random.uniform(0, args.b, (l-1)//2))
    pt = np.concatenate( ([1], pt, np.conj(pt)[::-1]) )

    bt = at*pt

    logger.info('Computing ifft')
    b = ifft(bt)

    # b should be real, but there's always some small imaginary part.
    logger.info('Max. imaginary residue: ' + str(np.amax(np.abs(np.imag(b)))))
    b = np.real(b)

    if args.outfile:
        outfile= args.outfile
    else:
        outfile = sys.stdout
    logger.info(f'Writing data: {outfile.name}')
    b.astype(np.float32).tofile(outfile)

    logger.info('Done.')
    sys.exit(0)
