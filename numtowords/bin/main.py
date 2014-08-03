
'''
Convert number to English words.
'''

import argparse
from numtowords.stringify import *


def main():
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument('nums', type=int, nargs='+')
    arg_parser.add_argument('--format', choices=['american', 'british'], default='british')
    arg_parser.add_argument('--basemaxpower', type=int, default=None)
    arg_parser.add_argument('--basestandardprefs', action='store_true')
    arg_parser.add_argument('--nocommas', action='store_true')
    args = arg_parser.parse_args()

    if args.basemaxpower is None:
        base_stringifier = PosIntBaseEngStringifier(
            use_standard_prefs=args.basestandardprefs
        )
    else:
        base_stringifier = PosIntBaseMaxEngStringifier(
            max_power=args.basemaxpower,
            use_standard_prefs=args.basestandardprefs
        )

    stringifier = IntEngStringifier(
        base_stringifier,
        british=(args.format == 'british'),
        commas=not args.nocommas
    )

    for n in args.nums:
        try:
            print(stringifier.stringify(n))
        except ValueError as e:
            print('Error: {}'.format(e))    

if __name__ == '__main__':
    main()
