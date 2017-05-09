# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 14:42:55 2016

@author: yxl
"""

import wx,os
from scipy.misc import imread
from imageplus import ImagePlus
from ui.canvasframe import CanvasFrame
from glob import glob
import IPy
from core.engine import Free

class Plugin(Free):
    title = 'Import Sequence'
    para = {'path':'./', 'start':0, 'end':0, 'step':1, 'title':'sequence'}

    def show(self):
        filt = 'BMP files (*.bmp)|*.bmp|PNG files (*.png)|*.png|JPG \
        files (*.jpg)|*.jpg|GIF files (*.gif)|*.gif|TIF files (*.tif)|*.tif'
        rst = IPy.getpath('Import sequence', filt, 'open', self.para)
        
        files = self.getfiles(self.para['path'])
        nfs = len(files)
        self.para['end'] = nfs-1
        self.view = [(str, 'Title','title',''), 
                     (int, (0, nfs-1), 0, 'Start', 'start', '0~%s'%(nfs-1)),
                     (int, (0, nfs-1), 0, 'End', 'end', '0~%s'%(nfs-1)),
                     (int, (0, nfs-1), 0, 'Step', 'step', '')]
        
        if rst!=wx.ID_OK:return rst
        return IPy.get_para('Import sequence', self.view, self.para)
        
            
    def getfiles(self, name):
        p,f = os.path.split(name)
        s = p+'/*.'+name.split('.')[-1]
        return glob(s)
        
    def readimgs(self, names, shape, dtype):
        imgs = []
        for i in range(len(names)):
            IPy.set_progress(int(round((i+1.0)/len(names)*100)))
            img = imread(names[i])
            if img.shape!=shape or img.dtype!=dtype:
                print('error:', names[i])
                continue
            imgs.append(img)
        IPy.set_progress(0)
        return imgs
    
    #process
    def run(self, para = None):
        try:
            img = imread(para['path'])
        except:
            IPy.alert('unknown img format!')
            return
        files = self.getfiles(para['path'])
        files.sort()
        imgs = self.readimgs(files[para['start']:para['end']+1:para['step']], img.shape, img.dtype)
        IPy.show_img(imgs, para['title'])
        

if __name__ == '__main__':
	print(Plugin.title)
	app = wx.App(False)
	Plugin().run()