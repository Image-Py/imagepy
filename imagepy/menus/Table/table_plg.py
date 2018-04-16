from imagepy.core.engine import Free
import pandas as pd
from imagepy import IPy

class Plugin(Free):
	title = 'Table Test'

	def progress(self, i, n):
		self.prgs = (i, n)

	def run(self, para=None):
		data = [[1,2,3,4,5],[6,7,8,9,0]]
		dataframe = pd.DataFrame(data, [1,2], list('abcde'))
		IPy.table('table-1', dataframe)