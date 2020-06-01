from imagepy.core.util import fileio
from skimage.io import imread, imsave
from sciapp import Source

Source.manager('reader').add(name='png', obj=imread)
Source.manager('writer').add(name='png', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'PNG Open'
	filt = ['PNG']

class SaveFile(fileio.Writer):
	title = 'PNG Save'
	filt = ['PNG']

plgs = [OpenFile, SaveFile]