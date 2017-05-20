from images2gif import writeGif, readGif
from imagepy.core.util import fileio
from imagepy import IPy
import os

class SaveAnimate(fileio.Saver):
	title = 'GIF Animate Save'
	filt = ['GIF']
	note = ['8-bit', 'rgb', 'stack']

	#process
	def run(self, ips, imgs, para = None):
		writeGif(para['path'], imgs, duration=0.2, subRectangles = False)

class OpenAnimate(fileio.Opener):
	title = 'GIF Animate Open'
	filt = ['GIF']
	note = ['8-bit', 'rgb', 'stack']

	#process
	def run(self, para = None):
		imgs = readGif(para['path'])
		fp, fn = os.path.split(para['path'])
		fn, fe = os.path.splitext(fn) 
		IPy.show_img(imgs, fn)

plgs = [OpenAnimate, SaveAnimate]