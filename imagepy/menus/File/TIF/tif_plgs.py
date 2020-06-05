from imagepy.core.util import fileio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add(name='tif', obj=imread)
Source.manager('reader').add(name='tiff', obj=imread)
Source.manager('writer').add(name='tif', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'TIF Open'
	filt = ['TIF', 'TIFF']

class SaveFile(fileio.Writer):
	title = 'TIF Save'
	filt = ['TIF']

plgs = [OpenFile, SaveFile]