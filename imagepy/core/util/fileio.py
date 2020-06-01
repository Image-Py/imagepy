import os
from ..manager import ConfigManager
from ..manager import ReaderManager, WriterManager
from ... import root_dir
from ..engine import Free, Simple, Macros
import numpy as np

def show_img(img, title):
    if isinstance(img, list):
        return IPy.show_img(img, title)
    if img.ndim>2 and img.shape[2]!=3:
        return IPy.show_img(img, title)
    if img.dtype==np.uint8 and img.ndim==3 and img.shape[2]==4:
        img = img[:,:,:3].copy()
    IPy.show_img([img], title)

# ViewerManager.add('imgs', IPy.show_img)
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
    #IPy.curapp.reload_plugins()

class Reader(Free):
    para = {'path':''}
    tag, note = None, None

    def show(self):
        self.para['path'] = self.app.getpath('Open..', self.filt, 'open', '')
        return not self.para['path'] is None

    #process
    def run(self, para = None):
        add_recent(para['path'])

        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        reader = ReaderManager.gets(name=fe[1:], tag=self.tag, note=self.note)
        print(fe, self.tag, self.note, reader)
        '''
        if len(reader) == 0:
            a, b = os.path.splitext(fn)
            fn, fe = a, b+fe
            reader = ReaderManager.gets(name=fe[1:], tag=self.tag, note=self.note)
        if len(reader) is None: 
            return self.app.alert('No reader found for %s'%fe[1:])
        # ext, read, tag, note = reader
        '''
        self.app.show(self.tag, reader[0](para['path']))

class Writer(Simple):
    note = ['all']
    para={'path':''}

    def show(self):
        self.para['path'] = self.app.getpath('Save..', self.filt, 'save', '')
        return not self.para['path'] is None

    #process
    def run(self, ips, imgs, para = None):
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        writer = WriterManager.get(ext=fe[1:], tag='img')
        if len(writer)==1: return writer[0][1](para['path'], ips.img)
        writer = WriterManager.get(fe[1:], 'imgs')
        if len(writer)==1: return writer[0][1](para['path'], imgs)