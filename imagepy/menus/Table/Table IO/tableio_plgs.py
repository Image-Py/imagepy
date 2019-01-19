from imagepy.core.util import tableio
from pandas import read_csv, read_excel, read_hdf
from imagepy import IPy
from imagepy.core.manager import ReaderManager, WriterManager, ViewerManager

def show(data, title):
    IPy.show_table(data, title)
    
ViewerManager.add('tab', show)

save_csv = lambda path, data:data.to_csv(path)
ReaderManager.add('csv', read_csv, tag='tab')
WriterManager.add('csv', save_csv, tag='tab')

class OpenCSV(tableio.Reader):
    title = 'CSV Open'
    filt = ['csv']

class SaveCSV(tableio.Writer):
    title = 'CSV Save'
    filt = ['csv']

save_excel = lambda path, data:data.to_excel(path)
ReaderManager.add(['xls','xlsx'], read_excel, tag='tab')
WriterManager.add(['xls','xlsx'], save_excel, tag='tab')

class OpenExcel(tableio.Reader):
    title = 'Excel Open'
    filt = ['xls','xlsx']

class SaveExcel(tableio.Writer):
    title = 'Excel Save'
    filt = ['xls', 'xlsx']

plgs = [OpenCSV, SaveCSV, '-', OpenExcel, SaveExcel]