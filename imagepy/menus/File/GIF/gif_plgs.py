from imagepy.core.engine import dataio
from imagepy.core.engine import Simple
from skimage.io import imread, imsave
from sciapp import Source
import imageio

Source.manager('reader').add('gif', imread, 'img')
Source.manager('writer').add('gif', imsave, 'img')
Source.manager('reader').add('gif', imageio.mimread, 'imgs')

class OpenFile(dataio.Reader):
	title = 'GIF Open'
	tag = 'img'
	filt = ['GIF']

class SaveFile(dataio.ImageWriter):
	title = 'GIF Save'
	tag = 'img'
	filt = ['GIF']

class SaveAnimate(Simple):
	title = 'GIF Animate Save'
	note = ['all']
	filt = ['gif']
	para={'path':'', 'dur':0.2}
	view = [(int, 'dur', (0.01, 10), 2, 'duration', 's')]

	def load(self, ips):
		self.para['path'] = self.app.getpath('Save..', self.filt, 'save', '')
		return not self.para['path'] is None

	def run(self, ips, imgs, para = None):
		imageio.mimsave(para['path'], imgs, 'gif', duration = para['dur'])  

class OpenAnimate(dataio.Reader):
	title = 'GIF Animate Open'
	filt = ['GIF']
	tag = 'imgs'
	note = ['8-bit', 'rgb', 'stack']

plgs = [OpenFile, SaveFile, '-', OpenAnimate, SaveAnimate]