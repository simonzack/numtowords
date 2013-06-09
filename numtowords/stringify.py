
class NumBaseEngStringifier:
	'''
	for larger powers the naming used is the one by John Horton Conway/Richard Kenneth Guy/Allan Wechsler,
		an extension of the standard dictionary numbers (see wikipedia)

	this system is designed to represent 10**n
		the power, n, is divided by 3 (since the usual bases, thousand, million, billion go up in powers of 3)
		the power is then split up into chunks of 3 digits
	each chunk is then split into units, tens, hundreds:
		a reverse prefix order is used: units, tens, hundreds
		when preceding a component marked s or x, "tre" increases to "tres" and "se" to "ses" or "sex"
		when preceding a component marked m or n, "septe" and "nove" increase to "septem" and "novem" or "septen" and "noven"
		e.g. tre-viginti becomes tre-s-viginti, as 's' and 'ms' share 's'
	if a chunk is 0, then a placeholder, 'nilli' is used
	all the chunks are then concacted together, from the highest power to the lowest power

	alternative naming schemes:
		Landon Curt Noll:
			http://www.isthe.com/chongo/tech/math/number/howhigh.html
	'''

	def __init__(self,useStandardPrefs=True):
		self.useStandardPrefixes=useStandardPrefs

	thousand='thousand'

	#only used for powers 6-33 (i.e. the smallest) for every 3000 increase in power
	smallPrefixes=['','mi','bi','tri','quadri','quinti','sexti','septi','octi','noni','deci']

	#dictionary definitions which might have conflicts with the naming system
	standardPrefixes={
		48:		'quindeci',
		51:		'sexdeci',
		60:		'novemdeci',
	}

	infix='illi'
	suffix='on'

	placeholderInfix='ni'

	#the second tuple elements are the rules
	units=[
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
	def _powerToBaseNum(power):
		#-1 since the smallest prefix is million, which is 10**6, and the largest prefix is decillion, whic his 10**33
		return power//3-1

	@staticmethod
	def _baseNumToPower(base):
		return (base+1)*3

	@staticmethod
	def _getUnitSuffix(unitNum,thRule):
		'''
		get the suffix of the unit, given the ten rule or hundred rule (if the ten rule is not present)
		'''
		if unitNum==3 and ('s' in thRule or 'x' in thRule):
			return 's'
		elif unitNum==6:
			if 's' in thRule:
				return 's'
			if 'x' in thRule:
				return 'x'
		elif unitNum in (7,9):
			if 'm' in thRule:
				return 'm'
			if 'n' in thRule:
				return 'n'
		return ''

	def _getPrefixBase(self,base):
		curBase=base%1000
		prefBase=base//1000
		prefix=self._getPrefixBase(prefBase) if prefBase>0 else ''
		if curBase==0:
			if prefix:
				res=self.placeholderInfix
			else:
				return ''
		elif 1<=curBase<=10:
			res=self.smallPrefixes[curBase]
		elif self.useStandardPrefixes and self._baseNumToPower(curBase) in self.standardPrefixes:
			res=self.standardPrefixes[self._baseNumToPower(curBase)]
		else:
			hundredNum=curBase//100
			tenNum=(curBase//10)%10
			unitNum=curBase%10
			(hundredPrefix,hundredRule)=self.hundreds[hundredNum]
			(tenPrefix,tenRule)=self.tens[tenNum]
			unitPrefix=self.units[unitNum]
			if tenRule:
				unitPrefix+=self._getUnitSuffix(unitNum,tenRule)
			elif hundredRule:
				unitPrefix+=self._getUnitSuffix(unitNum,hundredRule)
			res=unitPrefix+tenPrefix+hundredPrefix
		#change 'a' to 'i' if res ends with 'a'
		return prefix+res[:-1]+self.infix

	def _getPrefix(self,power):
		return self._getPrefixBase(self._powerToBaseNum(power))

	def stringify(self,power):
		if power<0 or power%3!=0:
			raise ValueError('power')
		elif power==0:
			return ''
		elif power==3:
			return self.thousand
		return self._getPrefix(power)+self.suffix


class NumBaseMaxEngStringifier(NumBaseEngStringifier):
	def __init__(self,maxPower,useStandardPrefs=True):
		'''
		args:
			maxPower:
				maximum power word representation used, e.g. if maxPower==9,
					'billion billion' will be used instead to represent 10**18,
		'''
		super().__init__(useStandardPrefs)
		if maxPower<0 or maxPower%3!=0:
			raise ValueError('maxPower')
		self.maxPower=maxPower
		self.maxPowerStr=super().stringify(self.maxPower)

	def stringify(self,power):
		curPower=power%self.maxPower
		maxPowerNum=power//self.maxPower
		if curPower==0:
			tokens=[]
		else:
			tokens=[super().stringify(curPower)]
		tokens.extend([self.maxPowerStr]*maxPowerNum)
		return ' '.join(tokens)


class NumEngStringifier:
	'''
	use of 'and':
		american english does not use 'and' anywhere (see wikitionary)
	'''
	def __init__(self,numBaseStringifier,british=False):
		self.numBaseStringifier=numBaseStringifier
		self.british=british

	units=['','one','two','three','four','five','six','seven','eight','nine']
	tenUnits=['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
	tens=['','ten','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety']
	hundred='hundred'
	thousand='thousand'
	infix='and'

	def stringifyComponent(self,n):
		hundredRem=n%100
		hundredNum=n//100
		res=[]
		if hundredNum!=0:
			res.extend([self.units[hundredNum],self.hundred])
		if hundredRem!=0:
			if res and self.british:
				res.append(self.infix)
			if hundredRem<20:
				if hundredRem<10:
					res.append(self.units[hundredRem])
				else:
					res.append(self.tenUnits[hundredRem-10])
			else:
				unitNum=hundredRem%10
				tenNum=hundredRem//10
				tenRes=[]
				if tenNum!=0:
					tenRes.append(self.tens[tenNum])
				if unitNum!=0:
					tenRes.append(self.units[unitNum])
				res.append('-'.join(tenRes))
		return ' '.join(res)

	def stringify(self,n):
		res=[]
		curPow=0
		nRem=n%1000
		while True:
			rem=n%1000
			quot=n//1000
			curRes=[]
			if rem!=0:
				curRes.append(self.stringifyComponent(rem))
				if curPow>0:
					curRes.append(self.numBaseStringifier.stringify(curPow))
				if self.british and curPow==3 and nRem!=0:
					curRes.append(self.infix)
				res.append(' '.join(curRes))
			if quot==0:
				break
			n=quot
			curPow+=3

		return ' '.join(reversed(res))
