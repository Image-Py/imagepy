from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_reader(['jpg'], imread)
fileio.add_writer(['jpg'], imsave)

class OpenFile(fileio.Reader):
	title = 'JPG Open'
	filt = ['JPG']

class SaveFile(fileio.Writer):
	title = 'JPG Save'
	filt = ['JPG']

plgs = [OpenFile, SaveFile]