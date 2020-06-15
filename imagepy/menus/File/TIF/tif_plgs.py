from imagepy.core.util import fileio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add('tif', imread, 'img')
Source.manager('reader').add('tiff', imread, 'img')
Source.manager('writer').add('tif', imsave, 'img')

Source.manager('reader').add('tif', imread, 'imgs')
Source.manager('reader').add('tiff', imread, 'imgs')
Source.manager('writer').add('tif', imsave, 'imgs')

class OpenTIF(fileio.Reader):
	title = 'TIF Open'
	tag = 'img'
	filt = ['TIF', 'TIFF']

class SaveTIF(fileio.ImageWriter):
	title = 'TIF Save'
	tag = 'img'
	filt = ['TIF']

class OpenTIFS(fileio.Reader):
	title = 'TIF 3D Open'
	tag = 'imgs'
	filt = ['TIF', 'TIFF']

class SaveTIFS(fileio.ImageWriter):
	title = 'TIF 3D Save'
	tag = 'imgs'
	filt = ['TIF']
	note = ['all', 'stack3d']

plgs = [OpenTIF, SaveTIF, '-', OpenTIFS, SaveTIFS]