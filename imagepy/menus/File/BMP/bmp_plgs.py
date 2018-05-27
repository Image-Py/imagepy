from imagepy.core.util import fileio
from skimage.io import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add('bmp', imread)
WriterManager.add('bmp', imsave)

class OpenFile(fileio.Reader):
	title = 'BMP Open'
	filt = ['BMP']

class SaveFile(fileio.Writer):
	title = 'BMP Save'
	filt = ['BMP']

plgs = [OpenFile, SaveFile]