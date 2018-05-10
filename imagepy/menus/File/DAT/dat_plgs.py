from imagepy.core.util import fileio
import numpy as np
from imagepy.core.manager import ReaderManager, WriterManager



def imread(path):
	# return pydicom.read_file(path, force=True).pixel_array
	return np.loadtxt(path,dtype=float)
ReaderManager.add('dat', imread)

class OpenFile(fileio.Reader):
	title = 'DAT Open'
	filt = ['DAT']

plgs = [OpenFile]