from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_reader(['tif'], imread)
fileio.add_writer(['tif'], imsave)

class OpenFile(fileio.Reader):
	title = 'TIF Open'
	filt = ['TIF']

class SaveFile(fileio.Writer):
	title = 'TIF Save'
	filt = ['TIF']

plgs = [OpenFile, SaveFile]