from ..advanced import dataio
from skimage.io import imread, imsave

for i in ('bmp', 'jpg', 'jpeg', 'tif', 'png', 'gif'):
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

from pandas import read_csv, read_excel
read_csv2 = lambda p:read_csv(p, index_col=0)
read_excel2 = lambda p:read_excel(p, index_col=0)

save_csv = lambda path, data:data.to_csv(path)
dataio.ReaderManager.add('csv', read_csv2, 'tab')
dataio.WriterManager.add('csv', save_csv, 'tab')


save_excel = lambda path, data:data.to_excel(path)
dataio.ReaderManager.add('xls', read_excel2, 'tab')
dataio.WriterManager.add('xls', save_excel, 'tab')
dataio.ReaderManager.add('xlsx', read_excel2, 'tab')
dataio.WriterManager.add('xlsx', save_excel, 'tab')

class OpenTable(dataio.Reader):
    title = 'Excel Open'
    tag = 'tab'
    filt = ['csv', 'xls','xlsx']

class SaveTable(dataio.TableWriter):
    title = 'Excel Save'
    tag = 'tab'
    filt = ['csv', 'xls', 'xlsx']