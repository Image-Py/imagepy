from imagepy.core.util import fileio
from imageio import imread, imsave
from sciapp import Source

Source.manager('reader').add(name='jpg', obj=imread)
Source.manager('writer').add(name='jpg', obj=imsave)
Source.manager('reader').add(name='jpeg', obj=imread)
Source.manager('writer').add(name='jpeg', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'JPG Open'
	filt = ['JPG','JPEG']

class SaveFile(fileio.Writer):
	title = 'JPG Save'
	filt = ['JPG','JPEG']

plgs = [OpenFile, SaveFile]