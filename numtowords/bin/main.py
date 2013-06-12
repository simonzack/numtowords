
'''
Convert number to English words
'''

import argparse
from numtowords.stringify import *

def main():
	argParser=argparse.ArgumentParser(description=__doc__)
	argParser.add_argument('nums',type=int,nargs='+')
	argParser.add_argument('--format',choices=['american','british'])
	argParser.add_argument('--basemaxpower',default=None)
	argParser.add_argument('--basestandardprefs',default=None)
	argParser.add_argument('--commas',default=True)
	args=argParser.parse_args()

	if args.basemaxpower is None:
		baseStringifier=PosIntBaseEngStringifier(
			useStandardPrefs=args.basestandardprefs
		)
	else:
		baseStringifier=PosIntBaseMaxEngStringifier(
			maxPower=args.basemaxpower,
			useStandardPrefs=args.basestandardprefs
		)

	stringifier=IntEngStringifier(
		baseStringifier,
		british=(args.format=='british'),
		commas=args.commas
	)

	for n in args.nums:
		try:
			print(stringifier.stringify(n))
		except ValueError as e:
			print('Error: {}'.format(e))	

if __name__ == '__main__':
	main()
