from imagepy.core.util import fileio
from scipy.misc import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add('jpg', imread)
WriterManager.add('jpg', imsave)

class OpenFile(fileio.Reader):
	title = 'JPG Open'
	filt = ['JPG']

class SaveFile(fileio.Writer):
	title = 'JPG Save'
	filt = ['JPG']

plgs = [OpenFile, SaveFile]