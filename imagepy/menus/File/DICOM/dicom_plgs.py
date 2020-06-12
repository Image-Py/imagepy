from imagepy.core.util import fileio
import pydicom
from sciapp import Source



def imread(path):
	return pydicom.read_file(path, force=True).pixel_array

Source.manager('reader').add('dcm', imread)

class OpenFile(fileio.Reader):
	title = 'DCM Open'
	filt = ['DCM']

plgs = [OpenFile]