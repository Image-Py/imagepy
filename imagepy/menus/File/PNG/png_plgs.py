from imagepy.core.util import fileio
from scipy.misc import imread, imsave

fileio.add_reader(['png'], imread)
fileio.add_writer(['png'], imsave)

class OpenFile(fileio.Reader):
	title = 'PNG Open'
	filt = ['PNG']

class SaveFile(fileio.Writer):
	title = 'PNG Save'
	filt = ['PNG']

plgs = [OpenFile, SaveFile]