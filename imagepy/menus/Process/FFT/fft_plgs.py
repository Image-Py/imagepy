import numpy as np
from sciapp.action import Simple, Filter
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from sciapp.object import Image
#from imagepy.core import ImagePlus

class FFT(Simple):
	title = 'FFT'
	note = ['8-bit', '16-bit', 'int', 'float']
	para = {'shift':True, 'slice':False}
	view = [(bool, 'shift', 'zero center'),
			(bool, 'slice', 'slices')]

	def run(self, ips, imgs, para = None):
		if not para['slice']: imgs = [ips.img]
		shift = fftshift if para['shift'] else lambda x:x
		rst = []
		for i in range(len(imgs)):
			rst.append(shift(fft2(imgs[i])))
			self.progress(i, len(imgs))
		ips = Image(rst, '%s-fft'%ips.title)
		ips.log = True
		self.app.show_img(ips)

class IFFT(Simple):
	title = 'Inverse FFT'
	note = ['complex']
	para = {'shift':True, 'slice':False, 'type':'float'}
	view = [(list, 'type', ['uint8', 'int', 'float'], str, 'type', ''),
			(bool, 'shift', 'zero center'),
			(bool, 'slice', 'slices')]

	def run(self, ips, imgs, para = None):
		if not para['slice']: imgs = [ips.img]
		shift = ifftshift if para['shift'] else lambda x:x
		tp = {'uint8':np.uint8, 'int':np.int32, 'float':np.float32}
		rst, tp = [], tp[para['type']]
		for i in range(len(imgs)):
			rst.append(ifft2(shift(ips.img)).astype(tp))
			self.progress(i, len(imgs))
		self.app.show_img(rst, '%s-ifft'%ips.title)

class Shift(Filter):
	title = 'Zero Center'
	note = ['complex']

	def run(self, ips, snap, img, para = None):
		return fftshift(img)

class IShift(Filter):
	title = 'Zero Edge'
	note = ['complex']

	def run(self, ips, snap, img, para = None):
		return ifftshift(img)

class Split(Simple):
	title = 'Split Real And Image'
	note = ['complex']
	para = {'slice':False, 'copy':False}
	view = [(bool, 'slice', 'slices'),
			(bool, 'copy', 'memory copy')]

	def run(self, ips, imgs, para = None):
		if not para['slice']: imgs = [ips.img]
		copy = np.copy if para['copy'] else lambda x:x
		imags, reals = [], []
		for i in range(len(imgs)):
			reals.append(copy(imgs[i].real))
			imags.append(copy(imgs[i].imag))
			self.progress(i, len(imgs))
		self.app.show_img(reals, '%s-real'%ips.title)
		self.app.show_img(imags, '%s-image'%ips.title)

plgs = [FFT, IFFT, '-', Shift, IShift, '-', Split]