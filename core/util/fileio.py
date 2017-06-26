import os
from ..manager import ReaderManager, WriterManager, ViewerManager
from ... import IPy, root_dir
from ..engine import Free, Simple

def show(data, title):
    IPy.show_img(data, title)
    
def add_reader(exts, read):
    for i in exts:
        ReaderManager.add(i, read)
        ViewerManager.add(i, show)

def add_writer(exts, save):
    for i in exts:
        WriterManager.add(i, save)

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
        view = ViewerManager.get(fe[1:])
        img = read(para['path'])
        if img.ndim==3 and img.shape[2]==4:
            img = img[:,:,:3].copy()
        view([img], fn)

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
        write(para['path'], ips.img)