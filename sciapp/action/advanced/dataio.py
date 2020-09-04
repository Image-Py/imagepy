import os
from sciapp import Source
from . import Free, Simple, Table
#from .macros import Macros
from ... import Manager
import numpy as np

ReaderManager, WriterManager = Manager(), Manager()

class Reader(Free):
    para = {'path':''}
    tag = None

    def show(self):
        filt = [i.lower() for i in self.filt]
        self.para['path'] = self.app.get_path('Open..', filt, 'open', '')
        return not self.para['path'] is None

    #process
    def run(self, para = None):
        #add_recent(para['path'])
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        readers = ReaderManager.gets(fe[1:].lower(), tag=self.tag)
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
        self.para['path'] = self.app.get_path('Save..', filt, 'save', '')
        return not self.para['path'] is None

    #process
    def run(self, ips, imgs, para = None):
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        writer = WriterManager.gets(fe[1:].lower(), tag=self.tag)
        if len(writer)==1: writer[0][1](para['path'], ips.img if self.tag=='img' else imgs)

class TableWriter(Table):
    tag = 'tab'
    note = ['all']
    para={'path':''}

    def show(self):
        filt = [i.lower() for i in self.filt]
        self.para['path'] = self.app.get_path('Save..', filt, 'save', '')
        return not self.para['path'] is None

    #process
    def run(self, tps, snap, data, para = None):
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)

        writer = WriterManager.gets(fe[1:], tag=self.tag)
        if len(writer)==1: return writer[0][1](para['path'], data)