from imagepy.core.util import fileio
from imageio import imread, imsave
from sciapp import Source

Source.manager('reader').add('jpg', imread, 'img')
Source.manager('writer').add('jpg', imsave, 'img')
Source.manager('reader').add('jpeg', imread, 'img')
Source.manager('writer').add('jpeg', imsave, 'img')

class OpenFile(fileio.Reader):
	title = 'JPG Open'
	tag = 'img'
	filt = ['JPG','JPEG']

class SaveFile(fileio.ImageWriter):
	title = 'JPG Save'
	tag = 'img'
	filt = ['JPG','JPEG']

plgs = [OpenFile, SaveFile]