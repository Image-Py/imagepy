from sciapp.action import Table
import matplotlib.pyplot as plt
#from imagepy.core.manager import ColorManager
from matplotlib import colors
from imagepy.app import ColorManager

class Plot(Table):
	title = 'Plot Chart'
	para = {'cn':[], 'lw':1, 'grid':False, 'title':''}
	asyn = False
	view = [(str, 'title', 'title', ''),
			('fields', 'cn', 'select fields'),
			(int, 'lw', (1,5), 0, 'line width', ''),
			(bool, 'grid', 'grid')]

	def run(self, tps, snap, data, para = None):
		plt = self.app.show_plot(para['title'])
		data[para['cn']].plot(lw=para['lw'], grid=para['grid'], 
			title=para['title'], ax=plt.add_subplot())
		plt.Show()

class Bar(Table):
	title = 'Bar Chart'
	para = {'cn':[], 'dir':False, 'stack':False,'grid':False, 'title':''}
	asyn = False
	view = [(str, 'title', 'title', ''),
			('fields', 'cn', 'select fields'),
			(bool, 'dir', 'horizon'),
			(bool, 'stack', 'stacked'),
			(bool, 'grid', 'grid')]

	def run(self, tps, snap, data, para = None):
		plt = self.app.show_plot(para['title'])
		if para['dir']:
			data[para['cn']].plot.barh(stacked=para['stack'], grid=para['grid'], 
				title=para['title'], ax=plt.add_subplot())
		else: data[para['cn']].plot.bar(stacked=para['stack'], grid=para['grid'], 
			title=para['title'], ax=plt.add_subplot())
		plt.Show()

class Hist(Table):
	title = 'Hist Chart'
	para = {'cn':[], 'dir':'vertical', 'stack':False, 'bins':10, 'alpha':1.0, 
		'overlay':False, 'grid':False, 'title':''}
	asyn = False
	view = [(str, 'title', 'title', ''),
			('fields', 'cn', 'select fields'),
			(int, 'bins', (3,1000), 0, 'bins', ''),
			(float, 'alpha', (0,1), 1, 'alpha', '0~1'),
			(list, 'dir', ['horizontal', 'vertical'], str, 'orientation', ''),
			(bool, 'stack', 'stacked'),
			(bool, 'overlay', 'draw every columns in one'),
			(bool, 'grid', 'grid')]

	def run(self, tps, snap, data, para = None):
		plt = self.app.show_plot(para['title'])
		if para['overlay']:
			data[para['cn']].plot.hist(stacked=para['stack'], bins=para['bins'], alpha=para['alpha'],
				orientation=para['dir'], grid=para['grid'], title=para['title'], ax=plt.add_subplot())
		else:
			data[para['cn']].hist(stacked=para['stack'], bins=para['bins'], alpha=para['alpha'],
				orientation=para['dir'], grid=para['grid'], ax=plt.add_subplot())
		plt.Show()

class Box(Table):
	title = 'Box Chart'
	para = {'cn':[], 'hor':False, 'by':None, 'grid':False, 'title':''}
	asyn = False
	view = [(str, 'title', 'title', ''),
			('fields', 'cn', 'select fields'),
			('field', 'by', 'by', 'group'),
			(bool, 'hor', 'horizontal'),
			(bool, 'grid', 'grid')]

	def run(self, tps, snap, data, para = None):
		plt = self.app.show_plot(para['title'])
		data[para['cn']].plot.box(by=None, vert=~para['hor'], grid=para['grid'], 
			title=para['title'], ax=plt.add_subplot())
		plt.Show()

class Area(Table):
	title = 'Area Chart'
	para = {'cn':[], 'dir':'vertical', 'stack':False, 'bins':10, 'alpha':1.0, 'grid':False, 'title':''}
	asyn = False
	view = [(str, 'title', 'title', ''),
			('fields', 'cn', 'select fields'),
			(float, 'alpha', (0,1), 1, 'alpha', '0~1'),
			(bool, 'stack', 'stacked'),
			(bool, 'grid', 'grid')]

	def run(self, tps, snap, data, para = None):
		plt = self.app.show_plot(para['title'])
		data[para['cn']].plot.area(stacked=para['stack'], alpha=para['alpha'], 
			grid=para['grid'], title=para['title'], ax=plt.add_subplot())
		plt.Show()

class Scatter(Table):
	title = 'Scatter Chart'
	para = {'x':None, 'y':None, 's':1, 'alpha':1.0, 'rs':None, 'c':(0,0,255),
		 'cs':None, 'cm':None, 'grid':False, 'title':''}
	asyn = False
	view = [(str, 'title', 'title', ''),
			('field', 'x', 'x data', ''),
			('field', 'y', 'y data', ''),
			(int, 's', (0, 1024), 0, 'size', 'pix'),
			('field', 'rs', 'radius column', 'optional'),
			(float, 'alpha', (0,1), 1, 'alpha', '0~1'),
			('color', 'c', 'color', ''),
			('field', 'cs', 'color column', 'optional'),
			('cmap', 'cm', 'color map'),
			(bool, 'grid', 'grid')]

	def run(self, tps, snap, data, para = None):
		rs = data[para['rs']] * para['s'] if para['rs'] != 'None' else para['s']
		cs = data[para['cs']] if para['cs'] != 'None' else '#%.2x%.2x%.2x'%para['c']
		cm = ColorManager.get(para['cm'])/255.0
		cm = None if para['cs'] == 'None' else colors.ListedColormap(cm, N=256)
		plt = self.app.show_plot(para['title'])
		data.plot.scatter(x=para['x'], y=para['y'], s=rs, c=cs, alpha=para['alpha'], 
			cmap=cm, grid=para['grid'], title=para['title'], ax=plt.add_subplot())
		plt.Show()

class Pie(Table):
	title = 'Pie Chart'
	para = {'cn':[], 'title':''}
	asyn = False
	view = [(str, 'title', 'title', ''),
			('fields', 'cn', 'select fields')]

	def run(self, tps, snap, data, para = None):
		plt = self.app.show_plot(para['title'])
		data[para['cn']].plot.pie(subplots=True, title=para['title'], ax=plt.add_subplot())
		plt.Show()

plgs = [Plot, Area, Bar, Box, Hist, Pie, Scatter]