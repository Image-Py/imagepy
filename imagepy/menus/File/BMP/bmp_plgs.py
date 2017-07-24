from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_reader(['bmp'], imread)
fileio.add_writer(['bmp'], imsave)

class OpenFile(fileio.Reader):
	title = 'BMP Open'
	filt = ['BMP']

class SaveFile(fileio.Writer):
	title = 'BMP Save'
	filt = ['BMP']

plgs = [OpenFile, SaveFile]