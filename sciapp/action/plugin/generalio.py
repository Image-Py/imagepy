from ..advanced import dataio
from skimage.io import imread, imsave

for i in ('bmp', 'jpg', 'tif', 'png', 'gif'):
	dataio.ReaderManager.add(i, imread, 'img')
	dataio.WriterManager.add(i, imsave, 'img')

class OpenFile(dataio.Reader):
    title = 'Open'

    def load(self):
        self.filt = [i for i in sorted(dataio.ReaderManager.names())]
        return True

class SaveImage(dataio.ImageWriter):
	title = 'Save Image'

	def load(self, ips):
		self.filt = [i for i in sorted(dataio.WriterManager.names())]
		return True