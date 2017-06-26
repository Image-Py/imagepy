# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 14:42:55 2016
@author: yxl
"""

from imagepy.core.util import fileio
from scipy.misc import imread
from imagepy.core.manager import ReaderManager, ViewerManager
from imagepy.core.engine import Free
from imagepy import IPy
from glob import glob
import wx, os

class Plugin(Free):
    title = 'Import Sequence'
    para = {'path':'', 'start':0, 'end':0, 'step':1, 'title':'sequence'}

    def load(self):
        self.filt = sorted(ReaderManager.all())
        return True

    def show(self):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        rst = IPy.getpath('Import sequence', filt, 'open', self.para)
        if rst!=wx.ID_OK:return rst

        files = self.getfiles(self.para['path'])
        nfs = len(files)
        self.para['end'] = nfs-1
        self.view = [(str, 'Title','title',''), 
                     (int, (0, nfs-1), 0, 'Start', 'start', '0~{}'.format(nfs-1)),
                     (int, (0, nfs-1), 0, 'End', 'end', '0~{}'.format(nfs-1)),
                     (int, (0, nfs-1), 0, 'Step', 'step', '')]
        return IPy.get_para('Import sequence', self.view, self.para)

    def getfiles(self, name):
        p,f = os.path.split(name)
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
        fp, fn = os.path.split(para['path'])
        fn, fe = os.path.splitext(fn)
        read = ReaderManager.get(fe[1:])
        view = ViewerManager.get(fe[1:])
        
        try:
            img = read(para['path'])
        except:
            IPy.alert('unknown img format!')
            return
        
        files = self.getfiles(para['path'])
        files.sort()
        imgs = self.readimgs(files[para['start']:para['end']+1:para['step']], 
                             read, img.shape, img.dtype)
        view(imgs, para['title'])

if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()