from sciapp.action import Table
import pandas as pd
import numpy as np

class Count(Table):
	title = 'Values Frequency'
	para = {'cn':[]}
	view = [('fields', 'cn', 'fields to count')]

	def run(self, tps, snap, data, para=None):
		for i in para['cn']:
			df = pd.DataFrame(data[i].value_counts())
			df.columns = ['%s-vf'%i]
			self.app.show_table(df, '%s-values-frequency'%i)

class Frequency(Table):
	title = 'Table Bins Frequency'

	para = {'bins':10, 'max':1, 'min':0, 'auto':True, 'count':True, 'fre':False, 'weight':False, 'cn':[]}
		
	view = [(int, 'bins', (3,1024), 0, 'bins', 'n'),
			(bool, 'auto', 'auto scale'),
			(int, 'min', (-1e8, 1e8), 5, 'min range', ''),
			(int, 'max', (-1e8, 1e8), 5, 'max range', ''),
			('fields', 'cn', 'fields to count'),
			(bool, 'count', 'count times'),
			(bool, 'fre', 'count frequency'),
			(bool, 'weight', 'count weight')]

	def run(self, tps, snap, data, para=None):
		rg = None if para['auto'] else (para['min'], para['max'])
		for i in para['cn']:
			hist, bins = np.histogram(data[i], para['bins'], rg)
			vs = {'bins':bins[:-1]}
			if para['count']:vs['count'] = hist
			if para['fre']:vs['frequency'] = hist/hist.sum()
			if para['weight']:vs['weight'] = np.histogram(data[i], bins, rg, weights=data[i])[0]
			df = pd.DataFrame(vs, columns = [i for i in ['bins', 'count', 'frequency', 'weight'] if i in vs])
			self.app.show_table(df, '%s-frequency'%i)

plgs = [Count, Frequency]