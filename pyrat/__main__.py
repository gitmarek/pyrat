#!/usr/bin/env python3

import argparse, sys

import pyrat
from pyrat import PROGNAME, VERSION, logger


# sub-command functions

def print_default_help_page(args):
    print(PROGNAME + '-' + VERSION)
    # Put your detailed help page here.
    # print("See -h option for more details.")


def conv(args):
    pyrat.conv.start(args)


def randph(args):
    pyrat.randph.start(args)



if __name__ == '__main__':

    # create the top-level parser
    parser = argparse.ArgumentParser(prog=PROGNAME,
        description='Raw tools for raw audio.')
    parser.add_argument('--verbose', action='store_true')
    parser.set_defaults(func=print_default_help_page)
    subparsers = parser.add_subparsers()

    # create the parser for the "conv" command
    parser_conv = subparsers.add_parser('conv',
        description='''
Convolve input signal with kernel.
Perform convolution of INFILE and KERNEL. Normalize the result
and write it to OUTFILE.
        ''')
    parser_conv.add_argument('infile', type=str)
    parser_conv.add_argument('kerfile', type=str)
    parser_conv.add_argument('outfile', type=str)
    parser_conv.set_defaults(func=conv)

    # create the parser for the "randph" command
    parser_randph = subparsers.add_parser('randph',
        description='''
Randomize phases of Fourier coefficients.
Read INFILE of 32-bit float mono samples, calculate the FFT of the entire
signal; then randomize the phases of each frequency bin by multiplying the
frequency coefficient by a random phase: e^{2pi \phi}, where $\phi$ is
distributed uniformly on the interval [0,b).  By default, b=0.1. The result is
saved in OUTFILE. You can put '-' as both INFILE and, OUTFILE (standard input
and output).
        ''')
    parser_randph.add_argument('infile', type=str)
    parser_randph.add_argument('outfile', type=str)
    parser_randph.add_argument('-b', type=float, default=0.1,
        help='parameter (float), default=0.1')
    parser_randph.set_defaults(func=randph)

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel('INFO')
    else:
        logger.setLevel('WARNING')

    args.func(args)

    exit(0)
