import numpy as np
from imagepy.core.engine import Simple, Filter
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from imagepy import IPy

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
		IPy.show_img(rst, '%s-fft'%ips.title)

class LogPower(Simple):
	title = 'Log Power'
	note = ['complex']
	para = {'slice':False, 'type':'float', 'log':2.718}
	view = [(float, 'log', (2,30), 3, 'log', ''),
			(list, 'type', ['uint8', 'int', 'float'], str, 'type', ''),
			(bool, 'slice', 'slices')]

	def run(self, ips, imgs, para = None):
		if not para['slice']: imgs = [ips.img]
		tp = {'uint8':np.uint8, 'int':np.int32, 'float':np.float32}
		rst, tp = [], tp[para['type']]
		for i in range(len(imgs)):
			zs = np.log(np.abs(imgs[i]))
			zs /= np.log(para['log'])
			rst.append(zs.astype(tp))
			self.progress(i, len(imgs))
		IPy.show_img(rst, '%s-fft'%ips.title)

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
		IPy.show_img(rst, '%s-ifft'%ips.title)

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

plgs = [FFT, IFFT, '-', Shift, IShift, LogPower]