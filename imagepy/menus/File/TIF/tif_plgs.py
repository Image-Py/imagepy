from sciapp.action import dataio
from skimage.io import imread, imsave

dataio.ReaderManager.add('tif', imread, 'imgs')
dataio.ReaderManager.add('tiff', imread, 'imgs')
dataio.WriterManager.add('tif', imsave, 'imgs')

dataio.ReaderManager.add('tif', imread, 'img')
dataio.ReaderManager.add('tiff', imread, 'img')
dataio.WriterManager.add('tif', imsave, 'img')

class OpenTIF(dataio.Reader):
	title = 'TIF Open'
	tag = 'img'
	filt = ['TIF', 'TIFF']

class SaveTIF(dataio.ImageWriter):
	title = 'TIF Save'
	tag = 'img'
	filt = ['TIF']

class OpenTIFS(dataio.Reader):
	title = 'TIF 3D Open'
	tag = 'imgs'
	filt = ['TIF', 'TIFF']

class SaveTIFS(dataio.ImageWriter):
	title = 'TIF 3D Save'
	tag = 'imgs'
	filt = ['TIF']
	note = ['all', 'stack3d']

plgs = [OpenTIF, SaveTIF, '-', OpenTIFS, SaveTIFS]