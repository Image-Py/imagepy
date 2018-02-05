from imagepy.core.util import fileio
from imagepy import IPy
import os
import numpy as np
from PIL import Image, ImageSequence



class SaveAnimate(fileio.Writer):
	title = 'GIF Animate Save'
	filt = ['GIF']
	note = ['8-bit', 'rgb', 'stack']

	#process
	def run(self, ips, imgs, para = None):
		imgs = [Image.fromarray(i) for i in imgs] 
		imgs[0].save(para['path'], save_all=True, loop=0, append_images=imgs[1:])

class OpenAnimate(fileio.Reader):
	title = 'GIF Animate Open'
	filt = ['GIF']
	note = ['8-bit', 'rgb', 'stack']

	#process
	def run(self, para = None):
		#imgs = readGif(para['path'])

		imgs = Image.open(para['path'])
		imgs = ImageSequence.Iterator(imgs)
		imgs = [np.array(i.convert('RGB')) for i in imgs]
		for i in range(len(imgs)):
			if imgs[i].ndim==3 and imgs[i].shape[2]>3:
				imgs[i] = imgs[i][:,:,:3].copy()
		fp, fn = os.path.split(para['path'])
		fn, fe = os.path.splitext(fn) 
		IPy.show_img(imgs, fn)

plgs = [OpenAnimate, SaveAnimate]