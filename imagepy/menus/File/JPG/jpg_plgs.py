from imagepy.core.engine import dataio
from imageio import imread, imsave
from sciapp import Source

Source.manager('reader').add('jpg', imread, 'img')
Source.manager('writer').add('jpg', imsave, 'img')
Source.manager('reader').add('jpeg', imread, 'img')
Source.manager('writer').add('jpeg', imsave, 'img')

class OpenFile(dataio.Reader):
	title = 'JPG Open'
	tag = 'img'
	filt = ['JPG','JPEG']

class SaveFile(dataio.ImageWriter):
	title = 'JPG Save'
	tag = 'img'
	filt = ['JPG','JPEG']

plgs = [OpenFile, SaveFile]