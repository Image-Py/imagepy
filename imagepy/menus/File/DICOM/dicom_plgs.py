from imagepy.core.util import fileio
import dicom

def imread(path):
	return dicom.read_file(path, force=True).pixel_array

fileio.add_reader(['dcm'], imread)

class OpenFile(fileio.Reader):
	title = 'DCM Open'
	filt = ['DCM']

plgs = [OpenFile]