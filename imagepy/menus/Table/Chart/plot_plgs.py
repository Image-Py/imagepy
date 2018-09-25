from imagepy.core.engine import Table
from imagepy import IPy
import matplotlib.pyplot as plt

class Plot(Table):
	title = 'Plot Chart'
	para = {'cn':[], 'lw':1}
	asyn = False
	view = [('fields', 'cn', 'fields'),
			(int, 'lw', (1,5), 0, 'line width', '')]

	def run(self, tps, data, snap, para = None):
		data[para['cn']].plot(lw=para['lw'])
		plt.show()

class Bar(Table):
	title = 'Bar Chart'
	para = {'cn':[], 'dir':False, 'stack':False}
	asyn = False
	view = [('fields', 'cn', 'fields'),
			(bool, 'dir', 'horizon'),
			(bool, 'stack', 'stacked')]

	def run(self, tps, data, snap, para = None):
		if para['dir']:
			data[para['cn']].plot.barh(stacked=para['stack'])
		else: data[para['cn']].plot.bar(stacked=para['stack'])
		plt.show()

class Hist(Table):
	title = 'Hist Chart'
	para = {'cn':[], 'dir':'vertical', 'stack':False, 'bins':10, 'alpha':1.0, 'overlay':False}
	asyn = False
	view = [('fields', 'cn', 'fields'),
			(int, 'bins', (3,1000), 0, 'bins', ''),
			(float, 'alpha', (0,1), 1, 'alpha', '0~1'),
			(list, 'dir', ['horizontal', 'vertical'], str, 'orientation', ''),
			(bool, 'stack', 'stacked'),
			(bool, 'overlay', 'draw every columns in one')]

	def run(self, tps, data, snap, para = None):
		print(para)
		f = [data[para['cn']].hist, data[para['cn']].plot.hist][para['overlay']]
		f(stacked=para['stack'], bins=para['bins'], alpha=para['alpha'],
			orientation=para['dir'])
		plt.show()

plgs = [Plot, Bar, Hist]