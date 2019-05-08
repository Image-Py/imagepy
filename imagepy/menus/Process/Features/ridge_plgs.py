from skimage.filters import frangi, sato, hessian ,meijering
from imagepy.core.engine import Filter, Simple
from imagepy import IPy

def scale(img, low, high):
	img *= (high-low)/(max(img.ptp(), 1e-5))
	img += low - img.min()
	return img

class Frangi(Filter):
	title = 'Frangi'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'start':1, 'end':10, 'step':2, 'alpha':0.5, 'beta':0.5, 'gamma':15, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma end', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(float, 'alpha', (0.1, 1), 1, 'alpha',''),
			(float, 'beta', (0.1, 1), 1, 'beta',''),
			(float, 'gamma', (1,30), 1, 'gamma',''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, snap, img, para = None):
		rst = frangi(snap, range(para['start'], para['end'], para['step']), alpha=para['alpha'], 
			beta=para['beta'], gamma=para['gamma'], black_ridges=para['bridges'])
		img[:] = scale(rst, ips.range[0], ips.range[1])

class Meijering(Filter):
	title = 'Meijering'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'start':1, 'end':10, 'step':2, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
			(int, 'end', (1,20), 0,  'sigma end', ''),
			(int, 'step', (1,5), 0,  'sigma step', ''),
			(bool, 'bridges', 'black ridges')]

	def run(self, ips, snap, img, para = None):
		rst =meijering(snap, range(para['start'], para['end'], para['step']), black_ridges=para['bridges'])
		print('hahaha')
		img[:] = scale(rst, ips.range[0], ips.range[1])

class Sato(Filter):
	title = 'Sato'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'start':1, 'end':10, 'step':2, 'bridges':False}
	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
		(int, 'end', (1,20), 0,  'sigma end', ''),
		(int, 'step', (1,5), 0,  'sigma step', ''),
		(bool, 'bridges', 'black ridges')]

	def run(self, ips, snap, img, para = None):
		rst = sato(snap, range(para['start'], para['end'], para['step']), black_ridges=para['bridges'])
		img[:] = scale(rst, ips.range[0], ips.range[1])

class Hessian(Filter):
	title = 'Hessian'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'start':1, 'end':10, 'step':2, 'alpha':0.5, 'beta':0.5, 'gamma':15, 'bridges':False}

	view = [(int, 'start', (1,10), 0,  'sigma start', ''),
		(int, 'end', (1,20), 0,  'sigma end', ''),
		(int, 'step', (1,5), 0,  'sigma step', ''),
		(float, 'alpha', (0.1, 1), 1, 'alpha',''),
		(float, 'beta', (0.1, 1), 1, 'beta',''),
		(float, 'gamma', (1,30), 1, 'gamma',''),
		(bool, 'bridges', 'black ridges')]

	def run(self, ips, snap, img, para = None):
		rst = hessian(snap, range(para['start'], para['end'], para['step']), alpha=para['alpha'], 
			beta=para['beta'], gamma=para['gamma'],  black_ridges=para['bridges'])
		img[:] = scale(rst, ips.range[0], ips.range[1])

plgs = [Frangi, Meijering, Sato, Hessian]
