from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_opener(['jpg'], imread)

class OpenFile(fileio.Opener):
	title = 'JPG Open'
	filt = ['JPG']

class SaveFile(fileio.Saver):
	title = 'JPG Save'
	filt = ['JPG']

	def write(self, path, img):
		imsave(path, img)

plgs = [OpenFile, SaveFile]