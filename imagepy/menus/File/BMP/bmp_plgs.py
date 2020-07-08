from sciapp.action import dataio
from skimage.io import imread, imsave

dataio.ReaderManager.add('bmp', imread, 'img')
dataio.WriterManager.add('bmp', imsave, 'img')

class OpenFile(dataio.Reader):
	title = 'BMP Open'
	tag = 'img'
	filt = ['BMP']

class SaveFile(dataio.ImageWriter):
	title = 'BMP Save'
	tag = 'img'
	filt = ['BMP']

plgs = [OpenFile, SaveFile]