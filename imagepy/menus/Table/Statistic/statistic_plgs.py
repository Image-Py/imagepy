from imagepy.core.engine import Table
import pandas as pd
from imagepy import IPy

class Statistic(Table):
	title = 'Table Statistic'
	note = ['snap', 'only_num', 'row_msk', 'col_msk']

	para = {'axis':'Column', 'sum':True, 'mean':True,'max':False, 
		'min':False,'var':False,'std':False,'skew':False,'kurt':False}
		
	view = [(list, 'axis', ['Row', 'Column'], str, 'axis', ''),
			(bool, 'sum', 'sum'),
			(bool, 'mean', 'mean'),
			(bool, 'max', 'max'),
			(bool, 'min', 'min'),
			(bool, 'var', 'var'),
			(bool, 'std', 'std'),
			(bool, 'skew', 'skew'),
			(bool, 'kurt', 'kurt')]

	def run(self, tps, data, snap, para=None):
		rst, axis = {}, (0,1)[para['axis']=='Row']
		if para['sum']:rst['sum'] = snap.sum(axis=axis)
		if para['mean']:rst['mean'] = snap.mean(axis=axis)
		if para['max']:rst['max'] = snap.max(axis=axis)
		if para['min']:rst['min'] = snap.min(axis=axis)
		if para['var']:rst['var'] = snap.var(axis=axis)
		if para['std']:rst['std'] = snap.std(axis=axis)
		if para['skew']:rst['skew'] = snap.skew(axis=axis)
		if para['kurt']:rst['kurt'] = snap.kurt(axis=axis)
		IPy.show_table(pd.DataFrame(rst), tps.title+'-statistic')

plgs = [Statistic]