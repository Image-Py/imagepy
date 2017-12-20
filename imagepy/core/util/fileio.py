import os
from ..manager import ReaderManager, WriterManager, ViewerManager, ConfigManager
from ... import IPy, root_dir
from ..engine import Free, Simple, Macros
import numpy as np

def show(data, title):
    IPy.show_img(data, title)
    
def add_reader(exts, read):
    for i in exts:
        ReaderManager.add(i, read)
        ViewerManager.add(i, show)

def add_writer(exts, save):
    for i in exts:
        WriterManager.add(i, save)

recent = ConfigManager.get('recent')
if recent==None : recent = []

def f(path):
    return Macros(path, ["Open>{'path':%s}"%repr(path)])

rlist = [f(i) for i in recent]

def add_recent(path):
    global recent, rlist
    if path in recent:
        idx = recent.index(path)
        recent.insert(0, recent.pop(idx))
        rlist.insert(0, rlist.pop(idx))
    else: 
        recent.insert(0, path)
        rlist.insert(0, f(path))
    if len(recent)>=5:
        recent.pop(-1)
        rlist.pop(-1)

    ConfigManager.set('recent', recent)
    IPy.curapp.reload_plugins()

class Reader(Free):
    para = {'path':''}

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        return IPy.getpath('Open..', filt, 'open', self.para)

    #process
    def run(self, para = None):
        add_recent(para['path'])

        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        read = ReaderManager.get(fe[1:])
        view = ViewerManager.get(fe[1:])

        group, read = (True, read[0]) if isinstance(read, tuple) else (False, read)
        img = read(para['path'])
        if img.dtype==np.uint8 and img.ndim==3 and img.shape[2]==4:
            img = img[:,:,:3].copy()
        print(img.shape, group)
        if not group: img = [img]
        view(img, fn)

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