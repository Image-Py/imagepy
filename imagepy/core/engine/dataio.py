import os
from sciapp import Source
from imagepy import root_dir
from . import Free, Simple, Table
from .macros import Macros
import numpy as np

# ViewerManager.add('imgs', IPy.show_img)
recent = Source.manager('config').get('recent')
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

    Source.manager('config').add('recent', recent)
    #IPy.curapp.reload_plugins()

class Reader(Free):
    para = {'path':''}
    tag = None

    def show(self):
        filt = [i.lower() for i in self.filt]
        self.para['path'] = self.app.getpath('Open..', filt, 'open', '')
        return not self.para['path'] is None

    #process
    def run(self, para = None):
        add_recent(para['path'])

        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        readers = Source.manager('reader').gets(name=fe[1:], tag=self.tag)
        if len(readers)==0: 
            return self.app.alert('no reader found for %s file'%fe[1:])
        if not self.tag is None:
            self.app.show(self.tag, readers[0][1](para['path']), fn)
        else: self.app.show(readers[0][2], readers[0][1](para['path']), fn)

class ImageWriter(Simple):
    tag = 'img'
    note = ['all']
    para={'path':''}

    def show(self):
        filt = [i.lower() for i in self.filt]
        self.para['path'] = self.app.getpath('Save..', filt, 'save', '')
        return not self.para['path'] is None

    #process
    def run(self, ips, imgs, para = None):
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        writer = Source.manager('writer').gets(name=fe[1:].lower(), tag=self.tag)
        if len(writer)==1: writer[0][1](para['path'], ips.img if self.tag=='img' else imgs)

class TableWriter(Table):
    tag = 'tab'
    note = ['all']
    para={'path':''}

    def show(self):
        filt = [i.lower() for i in self.filt]
        self.para['path'] = self.app.getpath('Save..', filt, 'save', '')
        return not self.para['path'] is None

    #process
    def run(self, tps, snap, data, para = None):
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)

        writer = Source.manager('writer').gets(name=fe[1:], tag=self.tag)
        if len(writer)==1: return writer[0][1](para['path'], data)