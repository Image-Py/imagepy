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
from core.engines import Free

class Plugin(Free):
    title = 'Import Sequence'
    
    para = {'path':'./', 'start':0, 'step':1}

    def show(self):
        filt = 'BMP files (*.bmp)|*.bmp|PNG files (*.png)|*.png|JPG files (*.jpg)|*.jpg|GIF files (*.gif)|*.gif'
        rst = IPy.getpath('Import sequence', filt, self.para)
        
        files = self.getfiles(self.para['path'])
        nfs = len(files)
        self.view = [(int, (0, nfs-1), 0, 'Start', 'start', '0~%s'%(nfs-1)),
            (int, (0, nfs-1), 0, 'Step', 'step', '')]
        
        if rst!=wx.ID_OK:return rst
        return IPy.getpara('Import sequence', self.view, self.para)
        
            
    def getfiles(self, name):
        p,f = os.path.split(name)
        s = p+'/*.'+name.split('.')[-1]
        return glob(s)
        
    def readimgs(self, names, shape, dtype):
        imgs = []
        for i in range(len(names)):
            IPy.curapp.set_progress(int(round((i+1.0)/len(names)*100)))
            IPy.curapp.pro_bar.Refresh()
            img = imread(names[i])
            if img.shape!=shape or img.dtype!=dtype:
                print 'error:', names[i]
                continue
            imgs.append(img)
        IPy.curapp.set_progress(0)
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
        imgs = self.readimgs(files[para['start']::para['step']], img.shape, img.dtype)
        
        img = imread(para['path'])
        ips = ImagePlus(imgs)
        frame = CanvasFrame()
        frame.set_ips(ips)
        frame.Show()
        

if __name__ == '__main__':
	print Plugin.title
	app = wx.App(False)
	Plugin().run()