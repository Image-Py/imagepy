from imagepy.core.engine import Table
from imagepy import IPy

class Plugin(Table):
	title = 'Table Transpose'

	def run(self, tps, data, para = None):
		IPy.table('trans', data.T)