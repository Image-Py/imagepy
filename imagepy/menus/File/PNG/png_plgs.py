from sciapp.action import dataio
from skimage.io import imread, imsave
from sciapp import Source

dataio.ReaderManager.add('png', imread, 'img')
dataio.WriterManager.add('png', imsave, 'img')

class OpenFile(dataio.Reader):
	title = 'PNG Open'
	tag = 'img'
	filt = ['PNG']

class SaveFile(dataio.ImageWriter):
	title = 'PNG Save'
	tag = 'img'
	filt = ['PNG']

plgs = [OpenFile, SaveFile]