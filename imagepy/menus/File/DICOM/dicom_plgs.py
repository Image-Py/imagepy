from imagepy.core.engine import dataio
import pydicom
from sciapp import Source



def imread(path):
	return pydicom.read_file(path, force=True).pixel_array

Source.manager('reader').add('dcm', imread, 'img')

class OpenFile(dataio.Reader):
	title = 'DCM Open'
	filt = ['DCM']
	tag = 'img'

plgs = [OpenFile]