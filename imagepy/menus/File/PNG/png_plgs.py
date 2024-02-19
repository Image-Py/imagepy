from sciapp.action import dataio
from skimage.io import imread, imsave

def read_png(path):
	img = imread(path)
	if img.ndim==3 and img.shape[-1]==4:
		msk = img[:,:,3]
		img = img[:,:,:3].copy()
		img[msk==0] = 255
	return img

dataio.ReaderManager.add('png', read_png, 'img')
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