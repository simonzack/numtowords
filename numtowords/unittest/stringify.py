
import unittest
from numtowords.stringify import *

class TestNumBaseEngStringifier(unittest.TestCase):
	def setUp(self):
		self.stringifier=NumBaseEngStringifier(useStandardPrefs=False)

	def testStringifyBase(self):
		#most from wikipedia
		baseStrs={
			0:				'',
			3:				'thousand',
			6: 				'million',
			9: 				'billion',
			12: 			'trillion',
			15: 			'quadrillion',
			18: 			'quintillion',
			21: 			'sextillion',
			24: 			'septillion',
			27: 			'octillion',
			30: 			'nonillion',
			33: 			'decillion',
			36: 			'undecillion',
			39: 			'duodecillion',
			42: 			'tredecillion',
			45: 			'quattuordecillion',
			48: 			'quinquadecillion',
			51: 			'sedecillion',
			54: 			'septendecillion',
			57: 			'octodecillion',
			60: 			'novendecillion',
			63: 			'vigintillion',
			66: 			'unvigintillion',
			69: 			'duovigintillion',
			72: 			'tresvigintillion',
			75: 			'quattuorvigintillion',
			78: 			'quinquavigintillion',
			81: 			'sesvigintillion',
			84: 			'septemvigintillion',
			87: 			'octovigintillion',
			90: 			'novemvigintillion',
			93: 			'trigintillion',
			96: 			'untrigintillion',
			99: 			'duotrigintillion',
			102: 			'trestrigintillion',
			105: 			'quattuortrigintillion',
			108: 			'quinquatrigintillion',
			111: 			'sestrigintillion',
			114: 			'septentrigintillion',
			117: 			'octotrigintillion',
			120: 			'noventrigintillion',
			123: 			'quadragintillion',
			153: 			'quinquagintillion',
			183: 			'sexagintillion',
			213: 			'septuagintillion',
			243: 			'octogintillion',
			273: 			'nonagintillion',
			303: 			'centillion',
			306: 			'uncentillion',
			309: 			'duocentillion',
			312: 			'trescentillion',
			333: 			'decicentillion',
			336: 			'undecicentillion',
			363: 			'viginticentillion',
			366: 			'unviginticentillion',
			393: 			'trigintacentillion',
			423: 			'quadragintacentillion',
			453: 			'quinquagintacentillion',
			483: 			'sexagintacentillion',
			513: 			'septuagintacentillion',
			543: 			'octogintacentillion',
			573: 			'nonagintacentillion',
			603: 			'ducentillion',
			903: 			'trecentillion',
			1203: 			'quadringentillion',
			1503: 			'quingentillion',
			1803: 			'sescentillion',
			2103: 			'septingentillion',
			2403: 			'octingentillion',
			2703: 			'nongentillion',
			3003: 			'millinillion',
			3000012:		'millinillitrillion',
		}
		for key,val in baseStrs.items():
			self.assertEquals(val,self.stringifier.stringify(key))

	def testGetPrefixBase(self):
		self.assertEquals('',self.stringifier._getPrefixBase(0))


class TestNumBaseMaxEngStringifier(unittest.TestCase):
	def setUp(self):
		self.stringifier=NumBaseMaxEngStringifier(9,useStandardPrefs=False)

	def testStringifyBase(self):
		self.assertEquals('',self.stringifier.stringify(0))
		self.assertEquals('million billion',self.stringifier.stringify(15))
		self.assertEquals('billion billion',self.stringifier.stringify(18))


class TestNumEngStrinfier(unittest.TestCase):
	def setUp(self):
		self.baseStringifier=NumBaseMaxEngStringifier(9,useStandardPrefs=False)
		self.stringifier=NumEngStringifier(self.baseStringifier,british=True)

	def testStrinfiy(self):
		numStrs={
			21:			'twenty-one',
			25:			'twenty-five',
			32:			'thirty-two',
			58:			'fifty-eight',
			64:			'sixty-four',
			79:			'seventy-nine',
			83:			'eighty-three',
			99:			'ninety-nine',
			100: 		'one hundred',
			101:		'one hundred and one',
			109:		'one hundred and nine',
			110:		'one hundred and ten',
			120:		'one hundred and twenty',
			152:		'one hundred and fifty-two',
			208:		'two hundred and eight',
			334:		'three hundred and thirty-four',
			200: 		'two hundred',
			900: 		'nine hundred',
			999:		'nine hundred and ninety-nine',
			1000: 		'one thousand',
			1012:		'one thousand and twelve',
			1024:		'one thousand and twenty-four',
			2000: 		'two thousand',
			10000: 		'ten thousand',
			11000: 		'eleven thousand',
			20000: 		'twenty thousand',
			21000: 		'twenty-one thousand',
			30000: 		'thirty thousand',
			85000: 		'eighty-five thousand',
			100000: 	'one hundred thousand',
			999000: 	'nine hundred and ninety-nine thousand',
			1000000: 	'one million',
			10000000: 	'ten million',
		}
		for n,s in numStrs.items():
			self.assertEquals(s,self.stringifier.stringify(n))

