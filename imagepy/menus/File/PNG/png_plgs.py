from imagepy.core.util import fileio
from skimage.io import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add('png', imread)
WriterManager.add('png', imsave)

class OpenFile(fileio.Reader):
	title = 'PNG Open'
	filt = ['PNG']

class SaveFile(fileio.Writer):
	title = 'PNG Save'
	filt = ['PNG']

plgs = [OpenFile, SaveFile]