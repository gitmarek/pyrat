import argparse, sys

import pyrat
from pyrat import PROGNAME, VERSION, logger


# sub-command functions

def conv(args):
    pyrat.conv.start(args)


def randph(args):
    pyrat.randph.start(args)



if __name__ == '__main__':

    # create the top-level parser
    parser = argparse.ArgumentParser(prog=PROGNAME,
        description='Raw tools for raw audio (32-bit float mono).',
        epilog=PROGNAME+' <command> -h for more details.')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('-v', '--version', action='store_true',
        help='print version number and exit')

    subparsers = parser.add_subparsers(title="Commands")

    # create the parser for the "conv" command
    parser_conv = subparsers.add_parser('conv',
        description='''Convolve input signal with kernel.
Perform convolution of infile and kernel. Normalize the result
and write it to outfile.''',
        help='Convolve imput with a kernel.')
    parser_conv.add_argument('infile', type=str)
    parser_conv.add_argument('kerfile', type=str)
    parser_conv.add_argument('outfile', type=str)
    parser_conv.set_defaults(func=conv)

    # create the parser for the "randph" command
    parser_randph = subparsers.add_parser('randph',
        description='''Randomize phases of Fourier coefficients.
Calculate the FFT of the entire signal; then randomize the phases of each
frequency bin by multiplying the frequency coefficient by a random phase:
e^{2pi \phi}, where $\phi$ is distributed uniformly on the interval [0,b).  By
default, b=0.1. The result is saved to outfile.''',
        help='Randomize phases of Fourier coefficients.')
    parser_randph.add_argument('infile', type=str)
    parser_randph.add_argument('outfile', type=str)
    parser_randph.add_argument('-b', type=float, default=0.1,
        help='phases disttibuted uniformly on [0,b)')
    parser_randph.set_defaults(func=randph)

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()

    if args.version:
        print(PROGNAME + '-' + VERSION)
        sys.exit(0)

    if args.verbose:
        logger.setLevel('INFO')
    else:
        logger.setLevel('WARNING')

    args.func(args)

    sys.exit(0)