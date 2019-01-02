from imagepy.core.util import fileio
from imageio import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add('jpg', imread)
WriterManager.add('jpg', imsave)
ReaderManager.add('jpeg', imread)
WriterManager.add('jpeg', imsave)

class OpenFile(fileio.Reader):
	title = 'JPG Open'
	filt = ['JPG','JPEG']

class SaveFile(fileio.Writer):
	title = 'JPG Save'
	filt = ['JPG','JPEG']

plgs = [OpenFile, SaveFile]