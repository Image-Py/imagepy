from sciapp.action import dataio
import numpy as np
from sciapp import Source

def imread(path):
	return np.loadtxt(path,dtype=float)
	
def imsave(path,img):
	np.savetxt(path,img)

dataio.ReaderManager.add('dat', imread, 'img')
dataio.WriterManager.add('dat', imsave, 'img')

class OpenFile(dataio.Reader):
	title = 'DAT Open'
	tag = 'img'
	filt = ['DAT']

class SaveFile(dataio.ImageWriter):
	title = 'DAT Save'
	tag = 'img'
	filt = ['DAT']

plgs = [OpenFile,SaveFile]