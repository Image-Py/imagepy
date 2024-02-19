from skimage.filters import frangi, sato, hessian ,meijering
from sciapp.action import Filter, Simple

class Frangi(Simple):
	title = 'Frangi 3D'
	note = ['float', 'auto_msk', 'auto_snap', 'stack3d']
	para = {'start':1, 'end':10, 'step':2, 'alpha':0.5, 'beta':0.5, 'gamma':15, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma end', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(float, 'alpha', (0.1, 1), 1, 'alpha',''),
			(float, 'beta', (0.1, 1), 1, 'beta',''),
			(float, 'gamma', (1,30), 1, 'gamma',''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, imgs, para = None):
		IPy.show_img(frangi(imgs, range(para['start'], para['end'], para['step']), 
			alpha=para['alpha'], beta=para['beta'], gamma=para['gamma'], 
			black_ridges=para['bridges']), ips.title+'-frangi')


class Meijering(Simple):
	title = 'Meijering 3D'
	note = ['float', 'auto_msk', 'auto_snap','stack3d']
	para = {'start':1, 'end':10, 'step':2, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma end', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, imgs, para=None):
		IPy.show_img(meijering(imgs, range(para['start'], para['end'], para['step']),
			black_ridges=para['bridges']), ips.title+'-meijering')

class Sato(Simple):
	title = 'Sato 3D'
	note = ['float', 'auto_msk', 'auto_snap', 'stack3d']
	para = {'start':1, 'end':10, 'step':2, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma end', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, imgs, para=None):
		IPy.show_img(sato(imgs, range(para['start'], para['end'], para['step']),
			black_ridges=para['bridges']), ips.title+'-sato')

class Hessian(Simple):
	title = 'Hessian 3D'
	note = ['float', 'auto_msk', 'auto_snap','stack3d']
	para = {'start':1, 'end':10, 'step':2, 'alpha':0.5, 'beta':0.5, 'gamma':15, 'bridges':True}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma end', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(float, 'alpha', (0.1, 1), 1, 'alpha',''),
			(float, 'beta', (0.1, 1), 1, 'beta',''),
			(float, 'gamma', (1,30), 1, 'gamma',''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, imgs, para = None):
		IPy.show_img(hessian(imgs, range(para['start'], para['end'], para['step']), 
			alpha=para['alpha'], beta=para['beta'], gamma=para['gamma'], 
			black_ridges=para['bridges']), ips.title+'-hessian')

plgs = [Frangi, Meijering, Sato, Hessian]
