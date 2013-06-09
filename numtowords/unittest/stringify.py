
import unittest
from ..stringify import *

class TestNumEngBaseStringifier(unittest.TestCase):
	def testStringifyBase(self):
		self.assertEquals(NumEngStringifier.stringify(3000012),'millinillitrillion')
		self.assertEquals

class TestNumEngStrinfier(unittest.TestCase):
	def testStrinfiyPart(self):
		self.assertEquals(NumEngStringifier.stringify(1012),'one thousand and twelve')
		self.assertEquals(NumEngStringifier.stringify(1024),'one thousand and twenty four')
