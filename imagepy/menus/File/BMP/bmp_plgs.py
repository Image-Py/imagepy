from imagepy.core.engine import dataio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add('bmp', imread, 'img')
Source.manager('writer').add('bmp', imsave, 'img')

class OpenFile(dataio.Reader):
	title = 'BMP Open'
	tag = 'img'
	filt = ['BMP']

class SaveFile(dataio.ImageWriter):
	title = 'BMP Save'
	tag = 'img'
	filt = ['BMP']

plgs = [OpenFile, SaveFile]