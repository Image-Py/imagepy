from imagepy.core.util import fileio
from skimage.io import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add(name='gif', obj=imread)
WriterManager.add(name='gif', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'GIF Open'
	filt = ['GIF']

class SaveFile(fileio.Writer):
	title = 'GIF Save'
	filt = ['GIF']

plgs = [OpenFile, SaveFile]