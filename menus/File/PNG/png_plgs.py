from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_opener(['png'], imread)

class OpenFile(fileio.Opener):
	title = 'PNG Open'
	filt = ['PNG']

class SaveFile(fileio.Saver):
	title = 'PNG Save'
	filt = ['PNG']

	def write(self, path, img):
		imsave(path, img)

plgs = [OpenFile, SaveFile]