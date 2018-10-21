import argparse, importlib, sys

import pyrat
from pyrat import name, version, logger


# This returns a function to be called by a subparser below
# We assume in the tool's submodule there's a function called 'start(args)'
# That takes over the execution of the program.
def tool_(tool_name):
    def f(args):
        submodule = importlib.import_module('pyrat.' + tool_name)
        getattr(submodule, 'start')(args)
    return f


if __name__ == '__main__':

    # create the top-level parser
    parser = argparse.ArgumentParser(prog=name,
        description='Raw tools for raw audio.',
        epilog= name+' <command> -h for more details.')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--quiet', action='store_true',
        help='takes precedence over \'verbose\'')
    parser.add_argument('-v', '--version', action='store_true',
        help='print version number and exit')

    subparsers = parser.add_subparsers(title="Commands")

    # create the parser for the "conv" command
    parser_conv = subparsers.add_parser('conv',
        description='''Convolve input signal with kernel.
Normalize the result and write it to outfile.''',
        help='Convolve input with a kernel.')
    parser_conv.add_argument('infile', type=argparse.FileType('r'))
    parser_conv.add_argument('kerfile', type=argparse.FileType('r'),
        help="kernel to be convolved with infile")
    parser_conv.add_argument('outfile', type=argparse.FileType('w'))
    parser_conv.set_defaults(func=tool_('conv'))

    # create the parser for the "randph" command
    parser_randph = subparsers.add_parser('randph',
        description='''Randomize phases of Fourier coefficients.
Calculate the FFT of the entire signal; then randomize the phases of each
frequency bin by multiplying the frequency coefficient by a random phase:
e^{2pi \phi}, where $\phi$ is distributed uniformly on the interval [0,b).  By
default, b=0.1. The result is saved to outfile.''',
        help='Randomize phases of Fourier coefficients.')
    parser_randph.add_argument('infile', type=argparse.FileType('r'))
    parser_randph.add_argument('outfile', type=argparse.FileType('w'))
    parser_randph.add_argument('-b', type=float, default=0.1,
        help='phases disttibuted uniformly on [0,b)')
    parser_randph.set_defaults(func=tool_('randph'))

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()

    if args.version:
        print(name + '-' + version)
        sys.exit(0)

    if args.verbose:
        logger.setLevel('INFO')
    else:
        logger.setLevel('WARNING')
    if args.quiet:
        logger.setLevel(60) # above 'CRITICAL'

    args.func(args)

    sys.exit(0)
