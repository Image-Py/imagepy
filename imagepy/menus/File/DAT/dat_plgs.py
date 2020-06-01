from imagepy.core.util import fileio
import numpy as np
from sciapp import Source

def imread(path):
	return np.loadtxt(path,dtype=float)
	
def imsave(path,img):
	np.savetxt(path,img)

Source.manager('reader').add(name='dat', obj=imread)
Source.manager('writer').add(name='dat', obj=imsave)

class OpenFile(fileio.Reader):
	title = 'DAT Open'
	filt = ['DAT']

class SaveFile(fileio.Writer):
	title = 'DAT Save'
	filt = ['DAT']

plgs = [OpenFile,SaveFile]