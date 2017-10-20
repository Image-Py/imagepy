# -*- coding: utf-8 -*
import scipy.ndimage as ndimg
from imagepy.core.engine import Filter, Simple
import numpy as np

class Gaussian3D(Simple):
	title = 'Gaussian 3D'
	note = ['all', 'stack3d']

	#parameter
	para = {'sigma':2}
	view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

	#process
	def run(self, ips, imgs, para = None):
		imgs[:] = ndimg.gaussian_filter(imgs, para['sigma'])

class Uniform3D(Simple):
	title = 'Uniform 3D'
	note = ['all', 'stack3d']

	#parameter
	para = {'size':2}
	view = [(float, (0,30), 1,  'size', 'size', 'pix')]

	#process
	def run(self, ips, imgs, para = None):
		imgs[:] = ndimg.uniform_filter(imgs, para['size'])

plgs = [Gaussian3D, Uniform3D]