from imagepy.core.util import tableio
from pandas import read_csv
from imagepy import IPy
from imagepy.core.manager import ReaderManager, WriterManager, ViewerManager

def show(data, title):
    IPy.show_table(data, title)

ReaderManager.add('csv', read_csv, tag='tab')
ViewerManager.add('tab', show)
#WriterManager.add('jpg', imsave)

class OpenFile(tableio.Reader):
    title = 'CSV Open'
    filt = ['CSV']
'''
class SaveFile(fileio.Writer):
    title = 'JPG Save'
    filt = ['JPG']
'''
plgs = [OpenFile]