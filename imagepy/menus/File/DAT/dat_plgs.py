from imagepy.core.util import fileio
import numpy as np
from imagepy.core.manager import ReaderManager, WriterManager

def imread(path):
	return np.loadtxt(path,dtype=float)
	
def imsave(path,img):
	np.savetxt(path,img)

ReaderManager.add('dat', imread)
WriterManager.add('dat', imsave)

class OpenFile(fileio.Reader):
	title = 'DAT Open'
	filt = ['DAT']

class SaveFile(fileio.Writer):
	title = 'DAT Save'
	filt = ['DAT']

plgs = [OpenFile,SaveFile]