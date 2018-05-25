import os
from ..manager import ViewerManager, ReaderManager, WriterManager
from ... import IPy, root_dir
from ..engine import Free, Simple, Macros
import numpy as np

def show(data, title):
    IPy.table(data, title)

class Reader(Free):
    para = {'path':''}

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        return IPy.getpath('Open..', filt, 'open', self.para)

    #process
    def run(self, para = None):

        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        read = ReaderManager.get(fe[1:])

        table = read(para['path'])
        ViewerManager.get(fe[1:])(table, fn)

class Writer(Simple):
    note = ['all']
    para={'path':root_dir}

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        return IPy.getpath('Save..', filt, 'save', self.para)

    #process
    def run(self, ips, imgs, para = None):
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        write = WriterManager.get(fe[1:])
        group, write = (True, write[0]) if isinstance(write, tuple) else (False, write)
        write(para['path'], imgs if group else ips.img)