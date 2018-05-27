from imagepy.core.util import fileio
from skimage.io import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add('tif', imread)
WriterManager.add('tif', imsave)

class OpenFile(fileio.Reader):
	title = 'TIF Open'
	filt = ['TIF']

class SaveFile(fileio.Writer):
	title = 'TIF Save'
	filt = ['TIF']

plgs = [OpenFile, SaveFile]