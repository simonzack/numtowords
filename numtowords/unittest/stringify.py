
import unittest
from ..stringify import *

class TestNumBaseEngStringifier(unittest.TestCase):
	def testStringifyBase(self):
		self.assertEquals(NumBaseEngStringifier.stringify(3000012),'millinillitrillion')
		self.assertEquals(NumBaseEngStringifier.stringify(9999999999),'tremilliamilliamilliatrecentretriginmilliamilliatrecentretriginmilliatrecendotrigintillion')

class TestNumEngStrinfier(unittest.TestCase):
	pass
	#def testStrinfiyPart(self):
	#	self.assertEquals(NumEngStringifier.stringify(1012),'one thousand and twelve')
	#	self.assertEquals(NumEngStringifier.stringify(1024),'one thousand and twenty four')
