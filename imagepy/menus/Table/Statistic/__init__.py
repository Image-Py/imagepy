from imagepy.core.engine import Table
from imagepy import IPy

class Transpose(Table):
	title = 'Table Statistic'
	para = {'sum':True, 'mean':True, 'max':False, 'min':False, 'std':False, 'var':False, 'only':True}
	para = [(bool, 'only', 'only number columns'),
			('lab', None, '=========  indecate  ========='),
			(bool, 'sum', 'sum'),
			(bool, 'mean', 'mean'),
			(bool, 'max', 'max'),
			(bool, 'min', 'min'),
			(bool, 'std', 'std'),
			(bool, 'var', 'var')]

	def run(self, tps, data, para = None):
		pass