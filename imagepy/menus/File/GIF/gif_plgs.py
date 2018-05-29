from imagepy.core.util import fileio
from skimage.io import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add('gif', imread)
WriterManager.add('gif', imsave)

class OpenFile(fileio.Reader):
	title = 'GIF Open'
	filt = ['GIF']

class SaveFile(fileio.Writer):
	title = 'GIF Save'
	filt = ['GIF']

plgs = [OpenFile, SaveFile]