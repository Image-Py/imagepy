# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 14:42:55 2016
@author: yxl
"""

from sciapp.action import dataio
from skimage.io import imread
from sciapp.action import Free
from glob import glob
import os.path as osp
    
class Plugin(Free):
    title = 'Import Sequence'
    para = {'path':'', 'start':0, 'end':0, 'step':1, 'title':'sequence'}

    def load(self):
        self.filt = dataio.ReaderManager.names()
        return True

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        rst = self.app.get_path('Import sequence', self.filt, 'open')
        if rst is None: return rst
        self.para['path'] = rst
        files = self.getfiles(self.para['path'])
        nfs = len(files)
        self.para['end'] = nfs-1
        self.view = [(str, 'title', 'Title',''), 
                     (int, 'start', (0, nfs-1), 0, 'Start', '0~{}'.format(nfs-1)),
                     (int, 'end',   (0, nfs-1), 0, 'End', '0~{}'.format(nfs-1)),
                     (int, 'step',  (0, nfs-1), 0, 'Step', '')]
        return self.app.show_para('Import sequence', self.para, self.view)

    def getfiles(self, name):
        p,f = osp.split(name)
        s = p+'/*.'+name.split('.')[-1]
        return glob(s)

    def readimgs(self, names, read, shape, dtype):
        imgs = []
        for i in range(len(names)):
            self.progress(i, len(names))
            img = read(names[i])
            if img.shape!=shape or img.dtype!=dtype:
                print('error:', names[i])
                continue
            imgs.append(img)
        return imgs

    #process
    def run(self, para = None):
        fp, fn = osp.split(para['path'])
        fn, fe = osp.splitext(fn)
        read = dataio.ReaderManager.get(name=fe[1:])
        try: img = read(para['path'])
        except: return self.app.alert('unknown img format!')
        files = self.getfiles(para['path'])
        files.sort()
        imgs = self.readimgs(files[para['start']:para['end']+1:para['step']], 
                             read, img.shape, img.dtype)
        self.app.show('imgs', imgs, para['title'])

if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()