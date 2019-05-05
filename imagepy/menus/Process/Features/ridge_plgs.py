from skimage.filters import frangi, sato, hessian ,meijering
from imagepy.core.engine import Filter

class Frangi(Filter):
	title = 'Frangi'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'start':1, 'end':10, 'step':2, 'alpha':0.5, 'beta':0.5, 'gamma':15, 'bridges':True}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma start', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(float, 'alpha', (0.1, 1), 1, 'alpha',''),
			(float, 'beta', (0.1, 1), 1, 'beta',''),
			(float, 'gamma', (1,30), 1, 'gamma',''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, snap, img, para = None):
		rst = frangi(snap, range(para['start'], para['end'], para['step']), 
			alpha=para['alpha'], beta=para['beta'], gamma=para['gamma'], black_ridges=para['bridges'])

class Meijering(Filter):
	title = 'Meijering'

class Sato(Filter):
	title = 'Sato'

class Hessian(Filter):
	title = 'Hessian'

plgs = [Frangi, Meijering, Sato, Hessian]