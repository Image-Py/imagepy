from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_opener(['bmp'], imread)

class OpenFile(fileio.Opener):
	title = 'BMP Open'
	filt = ['BMP']

class SaveFile(fileio.Saver):
	title = 'BMP Save'
	filt = ['BMP']

	def write(self, path, img):
		imsave(path, img)

plgs = [OpenFile, SaveFile]