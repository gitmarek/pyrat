import numpy as np
from scipy.fftpack import fft, ifft

from pyrat import logger


def start(args):

    logger.info(f'Reading file: {args.infile}')
    a = np.fromfile(args.infile, dtype=np.float32)
    l = len(a)
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

    logger.info(f'Writing the output file: {args.outfile}')
    b.astype(np.float32).tofile(args.outfile)

    logger.info('Done.')
    exit(0)
