from imagepy.core.util import fileio
from scipy.misc import imread, imsave


fileio.add_reader(['gif'], imread)
fileio.add_writer(['gif'], imsave)

class OpenFile(fileio.Reader):
	title = 'GIF Open'
	filt = ['GIF']

class SaveFile(fileio.Writer):
	title = 'GIF Save'
	filt = ['GIF']

plgs = [OpenFile, SaveFile]