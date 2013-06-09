
'''
Convert number to English words
$ num2eng.py 1411893848129211
one quadrillion, four hundred and eleven trillion, eight hundred and ninety
three billion, eight hundred and forty eight million, one hundred and twenty
nine thousand, two hundred and eleven
'''

import argparse
from .stringify import NumEngStringifier

def main():
	argParser=argparse.ArgumentParser(description=__doc__)
	argParser.add_argument('nums',type=int,nargs='+')
	args=argParser.parse_args()
	for n in args.nums:
		try:
			print(NumEngStringifier.stringify(n))
		except ValueError as e:
			print('Error: {}'.format(e))	

if __name__ == '__main__':
	main()
