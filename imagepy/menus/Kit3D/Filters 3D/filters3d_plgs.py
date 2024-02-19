# -*- coding: utf-8 -*
import scipy.ndimage as ndimg
from sciapp.action import Filter, Simple
#from skimage.morphology import watershed
from imagepy.ipyalg import watershed
import numpy as np

class Gaussian3D(Simple):
	title = 'Gaussian 3D'
	note = ['all', 'stack3d']

	#parameter
	para = {'sigma':2}
	view = [(float, 'sigma', (0,30), 1,  'sigma', 'pix')]

	#process
	def run(self, ips, imgs, para = None):
		imgs[:] = ndimg.gaussian_filter(imgs, para['sigma'])

class Uniform3D(Simple):
	title = 'Uniform 3D'
	note = ['all', 'stack3d']

	#parameter
	para = {'size':2}
	view = [(float, 'size', (0,30), 1,  'size', 'pix')]

	#process
	def run(self, ips, imgs, para = None):
		imgs[:] = ndimg.uniform_filter(imgs, para['size'])

class Sobel3D(Simple):
	title = 'Sobel 3D'
	note = ['all', 'stack3d']

	#process
	def run(self, ips, imgs, para = None):
		gradient = np.zeros(imgs.shape, dtype=np.float32)
		gradient += ndimg.sobel(imgs, axis=0, output=np.float32)**2
		gradient += ndimg.sobel(imgs, axis=1, output=np.float32)**2
		gradient += ndimg.sobel(imgs, axis=2, output=np.float32)**2
		gradient **= 0.5
		gradient /= 8
		if imgs.dtype == np.uint8: np.clip(gradient, 0, 255, gradient)
		imgs[:] = gradient

class USM3D(Simple):
	title = 'Unsharp Mask 3D'
	note = ['all', 'stack3d']

	para = {'sigma':2, 'weight':0.5}
	view = [(float, 'sigma', (0,30), 1,  'sigma', 'pix'),
			(float, 'weight', (0,5), 1,  'weight', '')]

	#process
	def run(self, ips, imgs, para = None):
		blurimgs = ndimg.gaussian_filter(imgs, para['sigma'], output=np.float32)
		blurimgs -= imgs
		blurimgs *= -para['weight']
		blurimgs += imgs
		if imgs.dtype == np.uint8: np.clip(blurimgs, 0, 255, blurimgs)
		imgs[:] = blurimgs

class UPWatershed(Filter):
	title = 'Up Down Watershed 3D'
	note = ['8-bit', 'stack3d', 'not_slice', 'not_channel', 'preview']
	modal = False
	para = {'thr1':0, 'thr2':255}
	view = [('slide', 'thr1', (0,255), 0, 'Low'),
			('slide', 'thr2', (0,255), 0, 'High')]

	def load(self, ips):
		self.buflut = ips.lut
		ips.lut = ips.lut.copy()
		return True

	def cancel(self, ips):
		ips.lut = self.buflut
		ips.update()

	def preview(self, ips, para):
		ips.lut[:] = self.buflut
		ips.lut[:para['thr1']] = [0,255,0]
		ips.lut[para['thr2']:] = [255,0,0]
		ips.update()

	def run(self, ips, snap, img, para = None):
		imgs = ips.imgs
		gradient = np.zeros(imgs.shape, dtype=np.float32)
		gradient += ndimg.sobel(imgs, axis=0, output=np.float32)**2
		gradient += ndimg.sobel(imgs, axis=1, output=np.float32)**2
		gradient += ndimg.sobel(imgs, axis=2, output=np.float32)**2
		gradient **= 0.5

		msk = np.zeros(imgs.shape, dtype=np.uint8)
		msk[imgs>para['thr2']] = 1
		msk[imgs<para['thr1']] = 2

		#rst = watershed(gradient, msk)
		rst = watershed(gradient, msk.astype(np.uint16))
		imgs[:] = (rst==1)*255
		ips.lut = self.buflut

plgs = [Gaussian3D, Uniform3D, '-', Sobel3D, USM3D, '-', UPWatershed]