# -*- coding: utf-8 -*
from skimage import feature
from imagepy.core.engine import Filter
from imagepy.core.roi import PointRoi

class Harris(Filter):
	title = 'Harris'
	note = ['8-bit', 'preview']
	para = {'sigma':1.0, 'k':0.05}
	view = [(float, 'sigma', (0,10), 1,  'sigma', 'pix'),
			(float, 'k', (0.01,0.2), 2,  'K', ''),]

	def run(self, ips, snap, img, para = None):
		cimg = feature.corner_harris(img, sigma=para['sigma'], k=para['k'])
		pts = feature.corner_peaks(cimg, min_distance=1)
		self.ips.roi = PointRoi([tuple(i[::-1]) for i in pts])

class Kitchen(Filter):
	title = 'Kitchen Rosenfeld'
	note = ['8-bit', 'preview']
	para = {'cval':1.0}
	view = [(float, 'cval', (0,10), 1,  'cval', 'value')]

	def run(self, ips, snap, img, para = None):
		cimg = feature.corner_kitchen_rosenfeld(img, mode='constant', cval=para['cval'])
		pts = feature.corner_peaks(cimg, min_distance=1)
		self.ips.roi = PointRoi([tuple(i[::-1]) for i in pts])

class Moravec(Filter):
	title = 'Moravec'
	note = ['8-bit', 'preview']
	para = {'size':1.0}
	view = [(int, 'size', (0,10), 0,  'size', 'pix')]

	def run(self, ips, snap, img, para = None):
		cimg = feature.corner_moravec(img, window_size=para['size'])
		pts = feature.corner_peaks(cimg, min_distance=1)
		self.ips.roi = PointRoi([tuple(i[::-1]) for i in pts])

class Tomasi(Filter):
	title = 'Tomasi'
	note = ['8-bit', 'preview']
	para = {'sigma':1.0}
	view = [(float, 'sigma', (0,10), 1,  'sigma', 'pix')]

	def run(self, ips, snap, img, para = None):
		cimg = feature.corner_shi_tomasi(img, sigma=para['sigma'])
		pts = feature.corner_peaks(cimg, min_distance=1)
		self.ips.roi = PointRoi([tuple(i[::-1]) for i in pts])

plgs = [Harris, Kitchen, Moravec, Tomasi]