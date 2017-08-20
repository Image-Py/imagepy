# -*- coding: utf-8 -*
from skimage import feature
from imagepy.core.engine import Filter
from imagepy.core.roi import PointRoi

class Harris(Filter):
	title = 'Harris'
	note = ['8-bit', 'preview']
	para = {'sigma':1.0, 'k':0.05}
	view = [(float, (0,10), 1,  'sigma', 'sigma', 'pix'),
			(float, (0.01,0.2), 2,  'K', 'k', ''),]

	def run(self, ips, snap, img, para = None):
		harris = feature.corner_harris(img, sigma=para['sigma'], k=para['k'])
		pts = feature.corner_peaks(harris, min_distance=1)
		self.ips.roi = PointRoi([tuple(i[::-1]) for i in pts])

plgs = [Harris]