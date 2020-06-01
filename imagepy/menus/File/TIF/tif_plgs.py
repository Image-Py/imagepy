from imagepy.core.util import fileio
from skimage.io import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add(name='tif', obj=imread)
ReaderManager.add(name='tiff', obj=imread)
WriterManager.add(name='tif', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'TIF Open'
	filt = ['TIF', 'TIFF']

class SaveFile(fileio.Writer):
	title = 'TIF Save'
	filt = ['TIF']

plgs = [OpenFile, SaveFile]