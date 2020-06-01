from imagepy.core.util import fileio
from imageio import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager

ReaderManager.add(name='jpg', obj=imread)
WriterManager.add(name='jpg', obj=imsave)
ReaderManager.add(name='jpeg', obj=imread)
WriterManager.add(name='jpeg', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'JPG Open'
	filt = ['JPG','JPEG']

class SaveFile(fileio.Writer):
	title = 'JPG Save'
	filt = ['JPG','JPEG']

plgs = [OpenFile, SaveFile]