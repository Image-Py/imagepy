from imagepy.core.util import fileio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add('png', imread, 'img')
Source.manager('writer').add('png', imsave, 'img')

class OpenFile(fileio.Reader):
	title = 'PNG Open'
	tag = 'img'
	filt = ['PNG']

class SaveFile(fileio.ImageWriter):
	title = 'PNG Save'
	tag = 'img'
	filt = ['PNG']

plgs = [OpenFile, SaveFile]