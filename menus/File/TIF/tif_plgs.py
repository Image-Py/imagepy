from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_opener(['tif'], imread)

class OpenFile(fileio.Opener):
	title = 'TIF Open'
	filt = ['TIF']

class SaveFile(fileio.Saver):
	title = 'TIF Save'
	filt = ['TIF']

	def write(self, path, img):
		imsave(path, img)

plgs = [OpenFile, SaveFile]