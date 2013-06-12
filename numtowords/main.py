
'''
Convert number to English words
'''

import argparse
from .stringify import PosIntEngStringifier

def main():
	argParser=argparse.ArgumentParser(description=__doc__)
	argParser.add_argument('nums',type=int,nargs='+')
	args=argParser.parse_args()
	for n in args.nums:
		try:
			print(PosIntEngStringifier.stringify(n))
		except ValueError as e:
			print('Error: {}'.format(e))	

if __name__ == '__main__':
	main()
