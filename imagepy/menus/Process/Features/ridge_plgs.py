from skimage.filters import frangi, sato, hessian ,meijering
from imagepy.core.engine import Filter, Simple
from imagepy import IPy

class Frangi(Simple):
	title = 'Frangi'
	note = ['float', '8-bit', 'int']
	para = {'start':1, 'end':10, 'step':2, 'alpha':0.5, 'beta':0.5, 'gamma':15, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma end', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(float, 'alpha', (0.1, 1), 1, 'alpha',''),
			(float, 'beta', (0.1, 1), 1, 'beta',''),
			(float, 'gamma', (1,30), 1, 'gamma',''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, imgs, para = None):
		lst = []
		for img in imgs:
			lst.append(frangi(img, range(para['start'], para['end'], para['step']), 
			alpha=para['alpha'], beta=para['beta'], gamma=para['gamma'], 
			black_ridges=para['bridges']))
		IPy.show_img(lst, ips.title + '-frangi')

class Meijering(Simple):
	title = 'Meijering'
	note = ['float', '8-bit', 'int']
	para = {'start':1, 'end':10, 'step':2, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma end', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, imgs, para=None):
		lst = []
		for img in imgs:
			lst.append(meijering(img, range(para['start'], para['end'], para['step']),
			black_ridges=para['bridges']))
		IPy.show_img(lst, ips.title + '-meijering')
		 

class Sato(Simple):
	title = 'Sato'
	note = ['float', '8-bit', 'int']
	para = {'start':1, 'end':10, 'step':2, 'bridges':False}
	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
		(int, 'end', (1,20), 0,  'sigma end', ''),
		(int, 'step', (1,5), 0,  'sigma step', ''),
		(bool, 'bridges', 'black ridges')]

	def run(self, ips, imgs, para = None):
		lst = []
		for img in imgs:
			lst.append(sato(img, range(para['start'], para['end'], para['step']),
				black_ridges=para['bridges']))
		IPy.show_img(lst, ips.title + '-sato')

class Hessian(Simple):
	title = 'Hessian'
	note = ['float', '8-bit', 'int']
	para = {'start':1, 'end':10, 'step':2, 'alpha':0.5, 'beta':0.5, 'gamma':15, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
		(int, 'end', (1,20), 0,  'sigma end', ''),
		(int, 'step', (1,5), 0,  'sigma step', ''),
		(float, 'alpha', (0.1, 1), 1, 'alpha',''),
		(float, 'beta', (0.1, 1), 1, 'beta',''),
		(float, 'gamma', (1,30), 1, 'gamma',''),
		(bool, 'bridges', 'black ridges')]

	def run(self, ips, imgs, para = None):
		lst = []
		for img in imgs:
			lst.append(hessian(img, range(para['start'], para['end'], para['step']), 
				alpha=para['alpha'], beta=para['beta'], gamma=para['gamma'], 
				black_ridges=para['bridges']))
		IPy.show_img(lst, ips.title + '-hessian')

plgs = [Frangi, Meijering, Sato, Hessian]
