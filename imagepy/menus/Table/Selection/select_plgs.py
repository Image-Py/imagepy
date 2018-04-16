from imagepy.core.engine import Table
import pandas as pd
import numpy as np

class Select(Table):
	title = 'Sel By C Name R Count'

	para = {'cn':[], 'call':False, 'r1':0, 'r2':0, 'rall':False}
	view = [('fields', 'cn'),
			(bool, 'all columns', 'call'),
			('any', 'start rows', 'r1'),
			('any', 'end rows', 'r2'),
			(bool, 'all rows', 'rall')]

	def run(self, tps, data, snap, para=None):
		if not para['call']:
			cmsk = para['cn']
		else: cmsk=[]
		if not para['rall']:
			rmsk = data.index[slice(para['r1'], para['r2'])]
		else: rmsk=[]
		print(para)
		print('plugins', rmsk, cmsk)
		tps.select(rmsk, cmsk)
			#signal.order_filter(snap[s], np.ones(para['r']*2+1), n)
		#IPy.table(tps.title+'-statistic', pd.DataFrame(rst))

plgs = [Select]