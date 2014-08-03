
import unittest
from numtowords.stringify import *


class TestPosIntBaseEngStringifier(unittest.TestCase):
    def setUp(self):
        self.stringifier = PosIntBaseEngStringifier(use_standard_prefs=False)

    def test_stringify_base(self):
        #most from wikipedia
        base_strs = {
            3:              'thousand',
            6:              'million',
            9:              'billion',
            12:             'trillion',
            15:             'quadrillion',
            18:             'quintillion',
            21:             'sextillion',
            24:             'septillion',
            27:             'octillion',
            30:             'nonillion',
            33:             'decillion',
            36:             'undecillion',
            39:             'duodecillion',
            42:             'tredecillion',
            45:             'quattuordecillion',
            48:             'quinquadecillion',
            51:             'sedecillion',
            54:             'septendecillion',
            57:             'octodecillion',
            60:             'novendecillion',
            63:             'vigintillion',
            66:             'unvigintillion',
            69:             'duovigintillion',
            72:             'tresvigintillion',
            75:             'quattuorvigintillion',
            78:             'quinquavigintillion',
            81:             'sesvigintillion',
            84:             'septemvigintillion',
            87:             'octovigintillion',
            90:             'novemvigintillion',
            93:             'trigintillion',
            96:             'untrigintillion',
            99:             'duotrigintillion',
            102:            'trestrigintillion',
            105:            'quattuortrigintillion',
            108:            'quinquatrigintillion',
            111:            'sestrigintillion',
            114:            'septentrigintillion',
            117:            'octotrigintillion',
            120:            'noventrigintillion',
            123:            'quadragintillion',
            153:            'quinquagintillion',
            183:            'sexagintillion',
            213:            'septuagintillion',
            243:            'octogintillion',
            273:            'nonagintillion',
            303:            'centillion',
            306:            'uncentillion',
            309:            'duocentillion',
            312:            'trescentillion',
            333:            'decicentillion',
            336:            'undecicentillion',
            363:            'viginticentillion',
            366:            'unviginticentillion',
            393:            'trigintacentillion',
            423:            'quadragintacentillion',
            453:            'quinquagintacentillion',
            483:            'sexagintacentillion',
            513:            'septuagintacentillion',
            543:            'octogintacentillion',
            573:            'nonagintacentillion',
            603:            'ducentillion',
            903:            'trecentillion',
            1203:           'quadringentillion',
            1503:           'quingentillion',
            1803:           'sescentillion',
            2103:           'septingentillion',
            2403:           'octingentillion',
            2703:           'nongentillion',
            3003:           'millinillion',
            3000012:        'millinillitrillion',
        }
        for key, val in base_strs.items():
            self.assertEqual(val, self.stringifier.stringify(key))

        with self.assertRaises(ValueError):
            self.stringifier.stringify(0)

    def test_get_prefix_base(self):
        self.assertEqual('', self.stringifier._get_prefix_from_base(0))


class TestPosIntBaseMaxEngStringifier(unittest.TestCase):
    def setUp(self):
        self.stringifier = PosIntBaseMaxEngStringifier(9, use_standard_prefs=False)

    def test_stringify_base(self):
        self.assertEqual('million billion', self.stringifier.stringify(15))
        self.assertEqual('billion billion', self.stringifier.stringify(18))


class TestPosIntEngStrinfier(unittest.TestCase):
    def setUp(self):
        self.base_stringifier = PosIntBaseEngStringifier(use_standard_prefs=False)
        self.stringifier = PosIntEngStringifier(self.base_stringifier, british=True)

    def test_stringify(self):
        '''
        test sources:
            http://english.stackexchange.com/questions/71770/usage-of-and-and-comma-when-writing-numbers-uk-style
            http://english.stackexchange.com/questions/97755/when-writing-out-large-numbers-in-words-should-commas-be-placed-at-thousand-sep
            http://english.stackexchange.com/questions/116236/placement-of-commas-and-and-in-english-numerals
        '''
        num_strs = {
            21:         'twenty-one',
            25:         'twenty-five',
            32:         'thirty-two',
            58:         'fifty-eight',
            64:         'sixty-four',
            79:         'seventy-nine',
            83:         'eighty-three',
            99:         'ninety-nine',
            100:        'one hundred',
            200:        'two hundred',
            900:        'nine hundred',
            1000:       'one thousand',
            1203:       'one thousand, two hundred and three',
            2000:       'two thousand',
            10000:      'ten thousand',
            11000:      'eleven thousand',
            20000:      'twenty thousand',
            21000:      'twenty-one thousand',
            30000:      'thirty thousand',
            85000:      'eighty-five thousand',
            100000:     'one hundred thousand',
            100101:     'one hundred thousand, one hundred and one',
            102304:     'one hundred and two thousand, three hundred and four',
            999000:     'nine hundred and ninety-nine thousand',
            987654:     'nine hundred and eighty-seven thousand, six hundred and fifty-four',
            1000000:    'one million',
            1000200:    'one million, two hundred',
            1002000:    'one million, two thousand',
            1002003:    'one million, two thousand and three',
            1023045:    'one million, twenty-three thousand and forty-five',
            1203450:    'one million, two hundred and three thousand, four hundred and fifty',
            5629296:    'five million, six hundred and twenty-nine thousand, two hundred and ninety-six',
            10000000:   'ten million',
            12345678:   'twelve million, three hundred and forty-five thousand, six hundred and seventy-eight',
            100000300:  'one hundred million, three hundred',
            102304567:  'one hundred and two million, three hundred and four thousand, five hundred and sixty-seven',

            #last block has an 'and' prefix
            101:        'one hundred and one',
            102:        'one hundred and two',
            109:        'one hundred and nine',
            110:        'one hundred and ten',
            120:        'one hundred and twenty',
            152:        'one hundred and fifty-two',
            208:        'two hundred and eight',
            334:        'three hundred and thirty-four',
            999:        'nine hundred and ninety-nine',
            1001:       'one thousand and one',
            1002:       'one thousand and two',
            1012:       'one thousand and twelve',
            1024:       'one thousand and twenty-four',
            1000002:    'one million and two',
            1000020:    'one million and twenty',

            #comma before the last 'and'
            101024:     'one hundred and one thousand, and twenty-four',
            102003:     'one hundred and two thousand, and three',
            102000003:  'one hundred and two million, and three',
        }
        for n, s in num_strs.items():
            self.assertEqual(s, self.stringifier.stringify(n))

        with self.assertRaises(ValueError):
            self.stringifier.stringify(0)


class TestIntEngStrinfier(unittest.TestCase):
    def setUp(self):
        self.baseStringifier = PosIntBaseEngStringifier(use_standard_prefs=False)
        self.stringifier = IntEngStringifier(self.baseStringifier, british=True)

    def test_stringify(self):
        num_strs = {
            0:          'zero',
            -25:        'negative twenty-five',
        }
        for n, s in num_strs.items():
            self.assertEqual(s, self.stringifier.stringify(n))
