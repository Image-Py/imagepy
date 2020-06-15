from imagepy.core.util import fileio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add('bmp', imread, 'img')
Source.manager('writer').add('bmp', imsave, 'img')

class OpenFile(fileio.Reader):
	title = 'BMP Open'
	tag = 'img'
	filt = ['BMP']

class SaveFile(fileio.ImageWriter):
	title = 'BMP Save'
	tag = 'img'
	filt = ['BMP']

plgs = [OpenFile, SaveFile]