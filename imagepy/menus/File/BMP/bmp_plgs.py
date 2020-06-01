from imagepy.core.util import fileio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add(name='bmp', obj=imread)
Source.manager('writer').add(name='bmp', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'BMP Open'
	filt = ['BMP']

class SaveFile(fileio.Writer):
	title = 'BMP Save'
	filt = ['BMP']

plgs = [OpenFile, SaveFile]