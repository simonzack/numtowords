
class PosIntBaseEngStringifier:
    '''
    For larger powers the naming used is the one by John Horton Conway/Richard
    Kenneth Guy/Allan Wechsler, an extension of the standard dictionary
    numbers (see wikipedia).

    This system is designed to represent 10**n, starting from 10**6. It does
    not start from 'thousand' since the usual bases all end with 'illion'. The
    power, n, is divided by 3 (since the usual bases, million, billion go up
    in powers of 3). The power is then split up into chunks of 3 digits.

    Each chunk is then split into units, tens, hundreds:

    - A reverse prefix order is used: units, tens, hundreds.
    - When preceding a component marked s or x, "tre" increases to "tres" and
      "se" to "ses" or "sex".
    - When preceding a component marked m or n, "septe" and "nove" increase to
      "septem" and "novem" or "septen" and "noven". e.g. tre-viginti becomes
      tre-s-viginti, as 's' and 'ms' share 's'
    - If a chunk is 0, then a placeholder, 'nilli' is used.

    All the chunks are then concacted together, from the highest power to the
    lowest power.

    Alternative naming schemes:

    [Landon Curt Noll](http://www.isthe.com/chongo/tech/math/number/howhigh.html)
    '''

    def __init__(self, use_standard_prefs=True):
        self.use_standard_prefixes = use_standard_prefs

    thousand = 'thousand'

    # only used for powers 6-33 (i.e. the smallest) for every 3000 increase in
    # power
    small_prefixes = ['', 'mi', 'bi', 'tri', 'quadri', 'quinti', 'sexti', 'septi', 'octi', 'noni', 'deci']

    # dictionary definitions which might have conflicts with the naming system
    standard_prefixes = {
        48:     'quindeci',
        51:     'sexdeci',
        60:     'novemdeci',
    }

    infix = 'illi'
    suffix = 'on'

    placeholder_infix = 'ni'

    # the second tuple elements are the rules
    units = [
        '',
        'un',
        'duo',
        'tre',
        'quattuor',
        'quinqua',
        'se',
        'septe',
        'octo',
        'nove',
    ]

    tens = [
        ('', None),
        ('deci', 'n'),
        ('viginti', 'ms'),
        ('triginta', 'ns'),
        ('quadraginta', 'ns'),
        ('quinquaginta', 'ns'),
        ('sexaginta', 'n'),
        ('septuaginta', 'n'),
        ('octoginta', 'mx'),
        ('nonaginta', None),
    ]

    hundreds = [
        ('', None),
        ('centi', 'nx'),
        ('ducenti', 'n'),
        ('trecenti', 'ns'),
        ('quadringenti', 'ns'),
        ('quingenti', 'ns'),
        ('sescenti', 'n'),
        ('septingenti', 'n'),
        ('octingenti', 'mx'),
        ('nongenti', None),
    ]

    @staticmethod
    def _power_to_base_num(power):
        # -1 since the smallest prefix is million, which is 10**6, and the
        # largest prefix is decillion, whic his 10**33
        return power//3-1

    @staticmethod
    def _base_num_to_power(base):
        return (base+1)*3

    @staticmethod
    def _get_unit_suffix(unit_num, th_rule):
        '''
        Get the suffix of the unit, given the ten rule or hundred rule (if the
        ten rule is not present).
        '''
        if unit_num == 3 and ('s' in th_rule or 'x' in th_rule):
            return 's'
        elif unit_num == 6:
            if 's' in th_rule:
                return 's'
            if 'x' in th_rule:
                return 'x'
        elif unit_num in (7, 9):
            if 'm' in th_rule:
                return 'm'
            if 'n' in th_rule:
                return 'n'
        return ''

    def _get_prefix_from_base(self, base):
        cur_base = base % 1000
        pref_base = base // 1000
        prefix = self._get_prefix_from_base(pref_base) if pref_base > 0 else ''
        if cur_base == 0:
            if prefix:
                res = self.placeholder_infix
            else:
                return ''
        elif 1 <= cur_base <= 10:
            res = self.small_prefixes[cur_base]
        elif self.use_standard_prefixes and self._base_num_to_power(cur_base) in self.standard_prefixes:
            res = self.standard_prefixes[self._base_num_to_power(cur_base)]
        else:
            hundred_num = cur_base // 100
            ten_num = (cur_base // 10) % 10
            unit_num = cur_base % 10
            hundred_prefix, hundred_rule = self.hundreds[hundred_num]
            ten_prefix, ten_rule = self.tens[ten_num]
            unit_prefix = self.units[unit_num]
            if ten_rule:
                unit_prefix += self._get_unit_suffix(unit_num, ten_rule)
            elif hundred_rule:
                unit_prefix += self._get_unit_suffix(unit_num, hundred_rule)
            res = unit_prefix + ten_prefix + hundred_prefix
        # change 'a' to 'i' if res ends with 'a'
        return prefix+res[:-1]+self.infix

    def _get_prefix_from_power(self, power):
        return self._get_prefix_from_base(self._power_to_base_num(power))

    @staticmethod
    def is_power_valid(power):
        return isinstance(power, int) and power > 0 and power % 3 == 0

    def stringify(self, power):
        if not self.is_power_valid(power):
            raise ValueError('power')
        if power == 3:
            return self.thousand
        return self._get_prefix_from_power(power) + self.suffix


class PosIntBaseMaxEngStringifier(PosIntBaseEngStringifier):
    def __init__(self, max_power, use_standard_prefs=True):
        '''
        args:
            max_power:
                Maximum power word representation used, e.g. if max_power==9,
                'billion billion' will be used instead to represent 10**18.
        '''
        if not self.is_power_valid(max_power) or max_power == 0:
            raise ValueError('max_power')
        super().__init__(use_standard_prefs)
        self.maxPower = max_power
        self.maxPowerStr = super().stringify(self.maxPower)

    def stringify(self, power):
        if not self.is_power_valid(power):
            raise ValueError('power')
        cur_power = power % self.maxPower
        max_power_num = power // self.maxPower
        if cur_power == 0:
            tokens = []
        else:
            tokens = [super().stringify(cur_power)]
        tokens.extend([self.maxPowerStr]*max_power_num)
        return ' '.join(tokens)


class PosIntEngStringifier:
    '''
    # Use of 'and'

    American english does not use 'and' anywhere (see wikitionary). Nobody
    does this, but not enforcing this also might introduces ambiguity which
    isn't resolved.
    '''

    units = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    ten_units = [
        'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'
    ]
    tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    hundred = 'hundred'
    thousand = 'thousand'
    infix = 'and'

    def __init__(self, num_base_stringifier, british=True, commas=True):
        self.num_base_stringifier = num_base_stringifier
        self.british = british
        self.commas = commas

    def _string_block_coeff(self, n):
        hundred_rem = n % 100
        hundred_num = n // 100
        res = []
        if hundred_num != 0:
            res.extend([self.units[hundred_num], self.hundred])
        if hundred_rem != 0:
            if res and self.british:
                res.append(self.infix)
            if hundred_rem < 20:
                if hundred_rem < 10:
                    res.append(self.units[hundred_rem])
                else:
                    res.append(self.ten_units[hundred_rem-10])
            else:
                unit_num = hundred_rem % 10
                ten_num = hundred_rem // 10
                ten_res = []
                if ten_num != 0:
                    ten_res.append(self.tens[ten_num])
                if unit_num != 0:
                    ten_res.append(self.units[unit_num])
                res.append('-'.join(ten_res))
        return ' '.join(res)

    def is_n_valid(self, n):
        return isinstance(n, int) and n > 0

    def stringify(self, n):
        '''
        # Algorithm (british)

        Stringify is done in base 1000, call each digit in base 1000 a block.
        
        For each block, an 'and' is inserted if the coefficient of 10 is 0,
        e.g. 'one hundred and two'.

        Each block is stringified by concatenating the digit and the power,
        e.g. 'one hundred and two', 'million'. Blocks with 0-value are
        skipped.

        If there's more than 1 block, and the last block has no 'and', then an
        'and' is inserted before the last block, e.g. 'one million and two'.

        If the last block has an 'and' prefix, and the second last non-zero
        block has an 'and', then a comma is inserted before the last block's
        'and', e.g. 'one hundred and two thousand, and three', but not 'one
        hundred and two thousand, one hundred and one'.

        # Algorithm (american)
        
        This is just the algorithm for british nuemrals being stripped of
        'and's.
        '''
        if not self.is_n_valid(n):
            raise ValueError('n')
        res = []
        cur_pow = 0
        block_coeffs = []
        block_coeffs_non_zero = []
        while True:
            rem = n % 1000
            quot = n // 1000
            block_res = []
            if len(block_coeffs) < 2:
                block_coeffs.append(rem)
            if rem != 0:
                if len(block_coeffs_non_zero) < 2:
                    block_coeffs_non_zero.append(rem)
                # stringify the digit in base 1000
                block_res.append(self._string_block_coeff(rem))
                if cur_pow > 0:
                    # concatenate power
                    block_res.append(self.num_base_stringifier.stringify(cur_pow))
                res.append(' '.join(block_res))
            if quot == 0:
                break
            n = quot
            cur_pow += 3
        if self.british:
            try:
                # there's more than 1 block, and the last block has no 'and'
                if 0 < block_coeffs[0] < 100 and block_coeffs[1] is not None:
                    res[0] = self.infix + ' ' + res[0]
                    if self.commas:
                        # the last block has an 'and' prefix, and the second
                        # last non-zero block has an 'and' remove the comma by
                        # merging
                        if 0 < block_coeffs[0] < 100 and 0 < block_coeffs_non_zero[1] < 100:
                            res0 = res.pop(0)
                            res1 = res.pop(0)
                            res.insert(0, '{} {}'.format(res1, res0))
            except IndexError:
                pass

        if self.commas:
            return ', '.join(reversed(res))
        else:
            return ' '.join(reversed(res))


class IntEngStringifier(PosIntEngStringifier):
    zero = 'zero'
    negative = 'negative'

    def is_n_valid(self, n):
        return isinstance(n, int)

    def stringify(self, n):
        if n == 0:
            return self.zero
        elif n < 0:
            return '{} {}'.format(self.negative, super().stringify(-n))
        else:
            return super().stringify(n)
