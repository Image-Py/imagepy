from imagepy.core.util import fileio
import pydicom
from imagepy.core.manager import ReaderManager, WriterManager



def imread(path):
	return pydicom.read_file(path, force=True).pixel_array

ReaderManager.add('dcm', imread)

class OpenFile(fileio.Reader):
	title = 'DCM Open'
	filt = ['DCM']

plgs = [OpenFile]