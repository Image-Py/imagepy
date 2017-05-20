from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_opener(['gif'], imread)

class OpenFile(fileio.Opener):
	title = 'GIF Open'
	filt = ['GIF']

class SaveFile(fileio.Saver):
	title = 'GIF Save'
	filt = ['GIF']

	def write(self, path, img):
		imsave(path, img)

plgs = [OpenFile, SaveFile]