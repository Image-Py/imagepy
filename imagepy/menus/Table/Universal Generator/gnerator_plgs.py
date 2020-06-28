from sciapp.action import Free
import numpy as np
import pandas as pd

class One(Free):
	title = 'Unit Matrix'
	para = {'size':3}
	view = [(int, 'size', (1,10240), 0, 'size', '')]

	def run(self, para=None):
		data = np.eye(para['size'])
		dataframe = pd.DataFrame(data)
		self.app.show_table(dataframe, 'Eye[%s,%s]'%data.shape)

class Random01(Free):
	title = 'Uniform Random'
	para = {'row':3, 'col':5, 'low':0, 'high':1}
	view = [(float, 'low',  (-1024,1024), 0, 'low', ''),
			(float, 'high', (-1024,1024), 0, 'high', ''),
			(int, 'row', (1,10240), 0, 'row', ''),
			(int, 'col', (1,10240), 0, 'col', '')]

	def run(self, para=None):
		data = np.random.rand(para['row'], para['col'])
		data *= para['high']-para['low']
		data -= para['low']
		dataframe = pd.DataFrame(data)
		self.app.show_table(dataframe, 'Random01[%s,%s]'%data.shape)

class RandomN(Free):
	title = 'Gaussian Random'
	para = {'row':3, 'col':5, 'mean':0, 'std':1}
	view = [(float, 'mean', (-1024,1024), 0, 'mean', ''),
			(float, 'std',  (-1024,1024), 0, 'std', ''),
			(int, 'row', (1,10240), 0, 'row', ''),
			(int, 'col', (1,10240), 0, 'col', '')]

	def run(self, para=None):
		data = np.random.randn(para['row'], para['col'])
		data *= para['std']
		data += para['mean']
		dataframe = pd.DataFrame(data)
		self.app.show_table(dataframe, 'RandomN[%s,%s]'%data.shape)

class Calendar(Free):
	title = 'Calendar'
	para = {'year':2018, 'month':2}
	view = [(int, 'year',  (-9999,9999), 0, 'year', ''),
			(int, 'month', (1,12), 0, 'month', '')]

	def run(self, para=None):
		import calendar
		ls = calendar.month(para['year'], para['month']).split('\n')
		title = ls[0].strip()
		titles = ls[1].split(' ')
		table = []
		for i in ls[2:-1]:
			a = i.replace('   ', ' None ').strip()
			table.append(a.replace('  ', ' ').split(' '))
		dataframe = pd.DataFrame(table, columns=titles)
		self.app.show_table(dataframe, ls[0].strip())

plgs = [One, Random01, RandomN, Calendar]