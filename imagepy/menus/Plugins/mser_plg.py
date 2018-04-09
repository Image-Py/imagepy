# -*- coding: utf-8 -*
import scipy.ndimage as nimg
from imagepy.core.engine import Filter
import numpy as np
import cv2

class Plugin(Filter):
	"""Gaussian: derived from imagepy.core.engine.Filter """
	title = 'MSER'
	note = ['8-bit', 'auto_msk', 'auto_snap','preview']
	para = {'delta':5, 'max':60, 'min':2000,'max_var':25,'min_div':20}
	view = [(int, (0,50), 0,  'delta', 'delta', ''),
			(int, (0,100), 0,  'max_area', 'max', ''),
			(int, (0,5000), 0,  'min_area', 'min', ''),
			(int, (0,100), 0,  'max_var', 'max_var', ''),
			(int, (0,100), 0,  'min_div', 'min_div', '')]

	def run(self, ips, snap, img, para = None):
		mser = cv2.MSER_create(para['delta'], para['max'], para['min'], para['max_var'], para['min_div'])
		regions = mser.detectRegions(img)
		img[:] = snap
		for i in regions[0][:]:
			img[i[:,1],i[:,0]] = 255