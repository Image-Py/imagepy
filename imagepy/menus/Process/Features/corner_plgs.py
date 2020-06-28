# -*- coding: utf-8 -*
from skimage import feature
from sciapp.action import Filter
from sciapp.object import Points, ROI

class Harris(Filter):
	title = 'Harris'
	note = ['8-bit', 'preview']
	para = {'sigma':1.0, 'k':0.05}
	view = [(float, 'sigma', (0,10), 1,  'sigma', 'pix'),
			(float, 'k', (0.01,0.2), 2,  'K', ''),]

	def run(self, ips, snap, img, para = None):
		cimg = feature.corner_harris(img, sigma=para['sigma'], k=para['k'])
		pts = feature.corner_peaks(cimg, min_distance=1)
		ips.roi = ROI([Points(pts[:,::-1])])

class Kitchen(Filter):
	title = 'Kitchen Rosenfeld'
	note = ['8-bit', 'preview']
	para = {'cval':1.0}
	view = [(float, 'cval', (0,10), 1,  'cval', 'value')]

	def run(self, ips, snap, img, para = None):
		cimg = feature.corner_kitchen_rosenfeld(img, mode='constant', cval=para['cval'])
		pts = feature.corner_peaks(cimg, min_distance=1)
		ips.roi = ROI([Points(pts[:,::-1])])

class Moravec(Filter):
	title = 'Moravec'
	note = ['8-bit', 'preview']
	para = {'size':1.0}
	view = [(int, 'size', (0,10), 0,  'size', 'pix')]

	def run(self, ips, snap, img, para = None):
		cimg = feature.corner_moravec(img, window_size=para['size'])
		pts = feature.corner_peaks(cimg, min_distance=1)
		ips.roi = ROI([Points(pts[:,::-1])])

class Tomasi(Filter):
	title = 'Tomasi'
	note = ['8-bit', 'preview']
	para = {'sigma':1.0}
	view = [(float, 'sigma', (0,10), 1,  'sigma', 'pix')]

	def run(self, ips, snap, img, para = None):
		cimg = feature.corner_shi_tomasi(img, sigma=para['sigma'])
		pts = feature.corner_peaks(cimg, min_distance=1)
		ips.roi = ROI([Points(pts[:,::-1])])

plgs = [Harris, Kitchen, Moravec, Tomasi]