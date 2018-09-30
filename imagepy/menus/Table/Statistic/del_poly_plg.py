from imagepy.core.engine import Table
import pandas as pd
from imagepy import IPy

class DelPoly(Table):
	title = 'Del choosen'

	# para = {'major':None, 'minor':None, 'descend':False}
		
	# view = [('field', 'major', 'major', 'key'),
	# 		('field', 'minor', 'minor', 'key'),
	# 		(bool, 'descend', 'descend')]
	para = {'major':None, 'minor':None, 'descend':False}
		
	view = [('field', 'major', 'major', 'key'),
			('field', 'minor', 'minor', 'index'),
			(bool, 'descend', 'descend')]

	def run(self, tps, data, snap, para=None):
		# tps.data.sort_values(by=[para['major'], para['minor']], 
		# 	axis=0, ascending=not para['descend'], inplace=True)
		print('para major :{}'.format(para['major']))
		tps.data = tps.data.drop(para['major'],axis=1)
		print('tps.data:{}'.format(tps.data))

plgs = [DelPoly]