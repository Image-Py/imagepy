from images2gif import writeGif, readGif
from imagepy.core.util import fileio
from imagepy import IPy
import os

class SaveAnimate(fileio.Writer):
	title = 'GIF Animate Save'
	filt = ['GIF']
	note = ['8-bit', 'rgb', 'stack']

	#process
	def run(self, ips, imgs, para = None):
		writeGif(para['path'], imgs, duration=0.2, subRectangles = False)

class OpenAnimate(fileio.Reader):
	title = 'GIF Animate Open'
	filt = ['GIF']
	note = ['8-bit', 'rgb', 'stack']

	#process
	def run(self, para = None):
		imgs = readGif(para['path'])
		for i in range(len(imgs)):
			if imgs[i].ndim==3 and imgs[i].shape[2]>3:
				imgs[i] = imgs[i][:,:,:3].copy()
		fp, fn = os.path.split(para['path'])
		fn, fe = os.path.splitext(fn) 
		IPy.show_img(imgs, fn)

plgs = [OpenAnimate, SaveAnimate]