from sciapp.action import dataio
from imageio import imread, imsave

dataio.ReaderManager.add('jpg', imread, 'img')
dataio.WriterManager.add('jpg', imsave, 'img')
dataio.ReaderManager.add('jpeg', imread, 'img')
dataio.WriterManager.add('jpeg', imsave, 'img')

class OpenFile(dataio.Reader):
	title = 'JPG Open'
	tag = 'img'
	filt = ['JPG','JPEG']

class SaveFile(dataio.ImageWriter):
	title = 'JPG Save'
	tag = 'img'
	filt = ['JPG','JPEG']

plgs = [OpenFile, SaveFile]