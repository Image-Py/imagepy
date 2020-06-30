from sciapp.action import dataio
from pandas import read_csv, read_excel, read_hdf

def show(data, title):
    IPy.show_table(data, title)
    
# ViewerManager.add('tab', show)

save_csv = lambda path, data:data.to_csv(path)
dataio.ReaderManager.add('csv', read_csv, 'tab')
dataio.WriterManager.add('csv', save_csv, 'tab')

class OpenCSV(dataio.Reader):
    title = 'CSV Open'
    tag = 'tab'
    filt = ['csv']

class SaveCSV(dataio.TableWriter):
    title = 'CSV Save'
    tag = 'tab'
    filt = ['csv']

save_excel = lambda path, data:data.to_excel(path)
dataio.ReaderManager.add('xls', read_excel, 'tab')
dataio.WriterManager.add('xls', save_excel, 'tab')
dataio.ReaderManager.add('xlsx', read_excel, 'tab')
dataio.WriterManager.add('xlsx', save_excel, 'tab')

class OpenExcel(dataio.Reader):
    title = 'Excel Open'
    tag = 'tab'
    filt = ['xls','xlsx']

class SaveExcel(dataio.TableWriter):
    title = 'Excel Save'
    tag = 'tab'
    filt = ['xls', 'xlsx']

plgs = [OpenCSV, SaveCSV, '-', OpenExcel, SaveExcel]