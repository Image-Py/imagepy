from imagepy.core.util import fileio
from imagepy.core.engine import Simple
from imagepy import IPy, root_dir
import os, imageio
import numpy as np

class SaveAnimate(Simple):
	title = 'GIF Animate Save'
	note = ['all']
	para={'path':root_dir, 'dur':0.2}
	view = [(int, 'dur', (0.01, 10), 2, 'duration', 's')]

	def load(self, ips):
		filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in ['GIF']])
		return IPy.getpath('Save..', filt, 'save', self.para)

	#process
	def run(self, ips, imgs, para = None):
		imageio.mimsave(para['path'], imgs, 'GIF', duration = para['dur'])  

class OpenAnimate(fileio.Reader):
	title = 'GIF Animate Open'
	filt = ['GIF']
	note = ['8-bit', 'rgb', 'stack']

	#process
	def run(self, para = None):
		#imgs = readGif(para['path'])

		imgs = imageio.mimread(para['path'])
		fp, fn = os.path.split(para['path'])
		fn, fe = os.path.splitext(fn) 
		IPy.show_img(imgs, fn)

plgs = [OpenAnimate, SaveAnimate]