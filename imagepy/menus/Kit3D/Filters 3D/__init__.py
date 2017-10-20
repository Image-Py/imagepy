# -*- coding: utf-8 -*
import scipy.ndimage as nimg
from imagepy.core.engine import Filter, Simple
import numpy as np

class Gaussian3D(Simple):
	title = 'Gaussian 3D'
	note = ['all', 'stack3d']

	#parameter
	para = {'sigma':2}
	view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

	#process
	def run(self, ips, img, para = None):
		img[:] = nimg.gaussian_filter(img, para['sigma'])