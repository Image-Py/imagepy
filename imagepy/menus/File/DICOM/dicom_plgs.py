from sciapp.action import dataio
import pydicom

def imread(path):
	return pydicom.read_file(path, force=True).pixel_array

dataio.ReaderManager.add('dcm', imread, 'img')

class OpenFile(dataio.Reader):
	title = 'DCM Open'
	filt = ['DCM']
	tag = 'img'

plgs = [OpenFile]