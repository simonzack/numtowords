
import math

class NumEngBaseStringifier:
	#only used for powers 6-33 (i.e. the smallest) for every 3000 increase in power
	smallPrefixes=['','m','b','tr','quadr','quint','sext','sept','oct','non','dec']

	infix='illi'
	suffix='on'

	#for larger powers the representation used is the one by Landon Curt Noll/John Horton Conway/Richard Kenneth Guy/Allan Wechsler,
	#	an extension of the standard dictionary numbers (see wikipedia)

	#this system is designed to represent 10**n
	#	the power, n, is divided by 3 (since the usual bases, thousand, million, billion go up in powers of 3)
	#	the power is then split up into chunks of 3 digits
	#each chunk is then split into units, tens, hundreds:
	#	a reverse prefix order is used: units, tens, hundreds
	#	if the prefix B (a ten or a hundred), following a unit, A, starts with a character in B's rule,
	#		then whatever char A's rule and B's rule
	#		share is added to A
	#	e.g. tre-viginti becomes tre-s-viginti, as 's' and 'ms' share 's'
	#if a chunk is 0, then a placeholder, 'nilli' is used
	#all the chunks are then concacted together, from the highest power to the lowest power

	placeholderInfix='nilli'

	#the second tuple elements are the rules
	units=[
		('',None),
		('un',None),
		('duo',None),
		('tre','s'),
		('quattuor',None),
		('quinqua',None),
		('se','sx'),
		('septe','mn'),
		('octo',None),
		('nove','mn')
	]
	tens=[
		('',None),
		('deci','n'),
		('viginti','ms'),
		('triginta','ns'),
		('quadraginta','ns'),
		('quinquaginta','ns'),
		('sexaginta','n'),
		('septuaginta','n'),
		('octoginta','mx'),
		('nonaginta',None),
	]
	hundreds=[
		('',None),
		('centi','nx'),
		('ducenti','n'),
		('trecenti','ns'),
		('quadringenti','ns'),
		('quingenti','ns'),
		('sescenti','n'),
		('septingenti','n'),
		('octingenti','mx'),
		('nongenti',None),
	]

	@staticmethod
	def _getUnitSuffix(unitsSufRule,thRule):
		'''
		get the suffix of the unit, given the ten rule or hundred rule (if the ten rule is not present)
		'''
		return next(iter(set(unitsSufRule).intersection(thRule)))

	@classmethod
	def _getPrefixRaw(cls,power):
		curPower=power%1000
		prefPower=power//1000
		prefix=cls._getPrefixRaw(prefPower) if prefPower>0 else ''
		if curPower==0:
			if prefix:
				return prefix+cls.placeholderInfix
			else:
				return ''
		elif 1<=curPower<=10:
			return prefix+cls.smallPrefixes[curPower-1]
		else:
			hundredsNum=curPower//100
			tensNum=(curPower//10)%10
			unitsNum=curPower%10
			(hundredsPrefix,hundredsRule)=cls.hundreds[hundredsNum]
			(tensPrefix,tensRule)=cls.tens[tensNum]
			(unitsPrefix,unitsSufRule)=cls.units[unitsNum]
			if tensRule:
				unitsPrefix+=cls._getUnitSuffix(unitsSufRule,tensRule)
			elif hundredsRule:
				unitsPrefix+=cls._getUnitSuffix(unitsSufRule,hundredsRule)
			return unitsPrefix+tensPrefix+hundredsPrefix

	@classmethod
	def _getPrefix(cls,power):
		#-1 since the smallest prefix is million, which is 10**6, and the largest prefix is decillion, whic his 10**33
		return cls._getPrefixRaw(power//3-1)

	@classmethod
	def _getBase(cls,power):
		if power<0 or power%3!=0:
			raise ValueError('power')
		return cls._getPrefix(power)+cls.suffix

	@classmethod
	def stringify(cls,power):
		return cls._getBase(power)


class NumEngStringifier:
	pass
	##tokens <=90
	#_SMALL = {
	#	'0' : '',
	#	'1' : 'one',
	#	'2' : 'two',
	#	'3' : 'three',
	#	'4' : 'four',
	#	'5' : 'five',
	#	'6' : 'six',
	#	'7' : 'seven',
	#	'8' : 'eight',
	#	'9' : 'nine',
	#	'10' : 'ten',
	#	'11' : 'eleven',
	#	'12' : 'twelve',
	#	'13' : 'thirteen',
	#	'14' : 'fourteen',
	#	'15' : 'fifteen',
	#	'16' : 'sixteen',
	#	'17' : 'seventeen',
	#	'18' : 'eighteen',
	#	'19' : 'nineteen',
	#	'20' : 'twenty',
	#	'30' : 'thirty',
	#	'40' : 'forty',
	#	'50' : 'fifty',
	#	'60' : 'sixty',
	#	'70' : 'seventy',
	#	'80' : 'eighty',
	#	'90' : 'ninety'
	#}
	#
	#def get_num(num):
	#	'''Get token <= 90, return '' if not matched'''
	#	return _SMALL.get(num, '')
	#
	#def triplets(l):
	#	'''Split list to triplets. Pad last one with '' if needed'''
	#	res = []
	#	for i in range(int(math.ceil(len(l) / 3.0))):
	#		sect = l[i * 3 : (i + 1) * 3]
	#		if len(sect) < 3: # Pad last section
	#			sect += [''] * (3 - len(sect))
	#		res.append(sect)
	#	return res
	#
	#def norm_num(num):
	#	"""Normelize number (remove 0's prefix). Return number and string"""
	#	n = int(num)
	#	return n, str(n)
	#
	#@classmethod
	#def stringifyPart(num):
	#	'''English representation of a number <= 999'''
	#	n, num = norm_num(num)
	#	hundred = ''
	#	ten = ''
	#	if len(num) == 3: # Got hundreds
	#		hundred = get_num(num[0]) + ' hundred'
	#		num = num[1:]
	#		n, num = norm_num(num)
	#	if (n > 20) and (n != (n / 10 * 10)): # Got ones
	#		tens = get_num(num[0] + '0')
	#		ones = get_num(num[1])
	#		ten = tens + ' ' + ones
	#	else:
	#		ten = get_num(num)
	#	if hundred and ten:
	#		return hundred + ' ' + ten
	#		#return hundred + ' and ' + ten
	#	else: # One of the below is empty
	#		return hundred + ten
	#
	#@classmethod
	#def stringify(cls,num):
	#	'''English representation of a number'''
	#	num = str(num) # Convert to string, throw if bad number
	#	if (len(num) / 3 >= len(_PRONOUNCE)): # Sanity check
	#		raise ValueError('Number too big')
	#
	#	if num == '0': # Zero is a special case
	#		return 'zero'
	#
	#	# Create reversed list
	#	x = list(num)
	#	x.reverse()
	#	pron = [] # Result accumolator
	#	ct = len(_PRONOUNCE) - 1 # Current index
	#	for a, b, c in triplets(x): # Work on triplets
	#		p = cls.stringifyPart(c + b + a)
	#		if p:
	#			pron.append(p + ' ' + _PRONOUNCE[ct])
	#		ct -= 1
	#	# Create result
	#	pron.reverse()
	#	return ', '.join(pron)

