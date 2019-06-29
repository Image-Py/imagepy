from imagepy.core.util import fileio
from skimage.io import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add('tif', imread)
WriterManager.add('tif', imsave)

class OpenFile(fileio.Reader):
	title = 'TIF Open'
	filt = [('TIF', ('TIF','TIFF', 'tif', 'tiff'))]

class SaveFile(fileio.Writer):
	title = 'TIF Save'
	filt = [('TIF', ('TIF','TIFF', 'tif', 'tiff'))]

plgs = [OpenFile, SaveFile]
