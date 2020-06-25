from imagepy.core.engine import dataio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add('png', imread, 'img')
Source.manager('writer').add('png', imsave, 'img')

class OpenFile(dataio.Reader):
	title = 'PNG Open'
	tag = 'img'
	filt = ['PNG']

class SaveFile(dataio.ImageWriter):
	title = 'PNG Save'
	tag = 'img'
	filt = ['PNG']

plgs = [OpenFile, SaveFile]