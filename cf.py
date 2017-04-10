#!/usr/bin/env python

from cf import CurrencyFair
from argparse import ArgumentParser
import logging
import sys


def parse_arguments():
    log.debug('Parsing arguments')

    description = 'Reads currency rates from CyrrenciFair.'

    parser = ArgumentParser(description=description)
    parser.add_argument(
        '-f', '--from',
        metavar='STR',
        dest='frm',
        required=True,
        help='from currency (e.g. GBP)')
    parser.add_argument(
        '-t', '--to',
        metavar='STR',
        required=True,
        help='to currency (e.g. CZK)')
    parser.add_argument(
        '-a', '--amount',
        metavar='NUM',
        required=True,
        help='amount (e.g. 1000)')
    parser.add_argument(
        '-d', '--direction',
        choices=['BUY', 'SELL'],
        default='SELL',
        metavar='STR',
        help='buy or sell (default: SELL)')
    parser.add_argument(
        '-k', '--keys',
        default='cfRate',
        metavar='STR',
        help=(
            'list of keys from the JSON message separated by comma. Use ALL '
            'to show all keys. (default: cfRate)'))
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='verbose output')

    return parser.parse_args()


def main():
    # Set logging
    global log
    log = logging.getLogger(__name__)
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=logging.ERROR)

    # Parse command line arguments
    args = parse_arguments()

    # Enable verbose mode
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    log.debug('START')

    # Instantiate the CyrrencyFair object
    cf = CurrencyFair(args.frm, args.to, args.amount, args.direction)
    keys = args.keys.split(',')

    values = None
    try:
        # Fetch the data from web
        values = cf.get_data(keys)
    except Exception as e:
        log.error('Can not get data: %s' % (e))
        sys.exit(1)

    # Print results
    for key, value in values.items():
        print('%s: %s' % (key, value))

    log.debug('END')


if __name__ == '__main__':
    main()
