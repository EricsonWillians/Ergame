class ParsingError(Exception):
	pass
 
class R:
 
	def __init__(self, r):
 
		self.raw = r
		if "-" in self.raw:
			self.r = self.raw.split("-")
		else:
			raise ParsingError
 
		try:
			self.r = range(int(self.r[0]), int(self.r[1]))
		except:
			raise ParsingError("Wrong range format, when considering that the correct format is N-N.")
 
	def get(self):
 
		return self.r
		
	def __call__(self):
		
		return self.r
 
	def it(self):
 
		for n in self.get():
			print n
 
	def _sum(self):
 
		return sum(self.r)
 
	def __str__(self):
		return str(self.r)
