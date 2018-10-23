import sys
import numpy as np
from scipy.fftpack import fft, ifft

from pyrat import logger


def start(args):

    infile= args.infile
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

    w = 5000
    logger.info('Modulate the amplitute envelope')
    if w < 1:
        logger.error('ERROR: Envelope window length must be at least 1')
        logger.error('Abort')
        sys.exit(1)
    if l < w:
        logger.error('Envelope window length larger than the signal length')
        logger.error('Abort')
        sys.exit(1)

    cs = np.cumsum(np.abs(a))
    env = np.concatenate( ( [cs[w - 1] / w], 
                ( cs[w:] - cs[:-w] ) / w,
                [ np.mean(np.abs(a[i:])) for i in range(l-w+1,l) ] ) )

    b = env * b

    outfile= args.outfile
    logger.info(f'Writing data: {outfile.name}')
    b.astype(np.float32).tofile(outfile)

    logger.info('Done.')
    sys.exit(0)
