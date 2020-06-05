from imagepy.core.util import fileio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add(name='gif', obj=imread)
Source.manager('writer').add(name='gif', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'GIF Open'
	filt = ['GIF']

class SaveFile(fileio.Writer):
	title = 'GIF Save'
	filt = ['GIF']

plgs = [OpenFile, SaveFile]