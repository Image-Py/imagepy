from skimage.io import imread, imsave
from imagepy.core.util import fileio
from imagepy import IPy
import os

class Save(fileio.Writer):
	title = 'TIF 3D Save'
	filt = ['TIF']
	note = ['8-bit', 'rgb', 'stack']

	#process
	def run(self, ips, imgs, para = None):
		imsave(para['path'], imgs)

class Open(fileio.Reader):
	title = 'TIF 3D Open'
	filt = ['TIF']

	#process
	def run(self, para = None):
		imgs = imread(para['path']).transpose(2,0,1)
		fp, fn = os.path.split(para['path'])
		fn, fe = os.path.splitext(fn) 
		IPy.show_img(imgs, fn)

plgs = [Open, Save]