# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 03:19:34 2017
@author: yxl
"""

import wx
# from imagepy.core import ImagePlus
from sciapp.action import ImageTool
from sciapp.action import  Simple

class Cross:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x, self.y = -1, -1
        
    def set_xy(self, x, y):
        if x!=None:self.x=x
        if y!=None:self.y=y
        
    def draw(self, dc, f):
        print(self.x, self.y)
        dc.SetPen(wx.Pen((255,255,0), width=1, style=wx.SOLID))
        dc.DrawLines([f(0,self.y),f(self.w,self.y)])
        dc.DrawLines([f(self.x,0),f(self.x,self.h)])
        
class Orthogonal(ImageTool):        
    title = 'Orthogonal View'
    def __init__(self):
        self.view1, self.view2 = None, None
        self.ips1, self.ips2 = None, None
        self.ips = None
        
    def getimgs(self, img, x, y):
        return img[:, :, int(x)].transpose((1,0,2)[:len(img.shape)-1]).copy(), \
            img[:, int(y), :].copy()
        
    def mouse_down(self, ips, x, y, btn, **key):
        if ips==self.ips1:
            self.ips1.mark.set_xy(x, y)
            self.ips.mark.set_xy(None, y)
            self.ips.cur = int(x)
            self.ips1.update()
            self.ips.update()
        elif ips==self.ips2:
            self.ips2.mark.set_xy(x, y)
            self.ips.mark.set_xy(x, None)
            self.ips.cur = int(y)
            self.ips2.update()
            self.ips.update()
        elif ips.get_nslices()==1 or not ips.is3d:
            IPy.alert('stack required!')
            return
        elif self.view1==None:
            img1, img2 = self.getimgs(ips.imgs, x, y)
            self.ips1 = ImagePlus([img1])
            self.ips2 = ImagePlus([img2])
            self.view1 = CanvasFrame(IPy.curapp)
            self.view2 = CanvasFrame(IPy.curapp)
            
            self.ips = ips
            self.view1.set_ips(self.ips1)
            self.view2.set_ips(self.ips2)
            canvas1, canvas2 = self.view1.canvas, self.view2.canvas
            canvas = IPy.get_window().canvas
            canvas1.scaleidx = canvas2.scaleidx = canvas.scaleidx
            canvas1.zoom(canvas.scales[canvas.scaleidx], 0, 0)
            canvas2.zoom(canvas.scales[canvas.scaleidx], 0, 0)
            self.view1.Show()
            self.view2.Show()
            ips.mark = Cross(*ips.size[::-1])
            ips.mark.set_xy(x, y)
            self.ips1.mark = Cross(*self.ips1.size[::-1])
            self.ips2.mark = Cross(*self.ips2.size[::-1])
            self.ips1.mark.set_xy(x, ips.cur)
            self.ips2.mark.set_xy(ips.cur, y)
            ips.update()
            
        else:
            img1, img2 = self.getimgs(ips.imgs, x, y)
            self.ips1.set_imgs([img1])
            self.ips2.set_imgs([img2])
            '''
            canvas1, canvas2 = self.view1.canvas, self.view2.canvas
            canvas = IPy.curwindow.canvas
            canvas1.scaleidx = canvas2.scaleidx = canvas.scaleidx
            canvas1.zoom(canvas.scales[canvas.scaleidx], 0, 0)
            canvas2.zoom(canvas.scales[canvas.scaleidx], 0, 0)
            '''
            self.ips1.mark.set_xy(ips.cur, y)
            self.ips2.mark.set_xy(x, ips.cur)
            self.ips1.update()
            self.ips2.update()
            ips.mark.set_xy(x, y)
            ips.update()
            
        
    def mouse_up(self, ips, x, y, btn, **key):
        pass
    
    def mouse_move(self, ips, x, y, btn, **key):
        if btn==1:
            img1, img2 = self.getimgs(ips.imgs, x, y)
            self.ips1.set_imgs([img1])
            self.ips2.set_imgs([img2])
            self.ips1.update()
            self.ips2.update()
            ips.update()
            ips.mark.set_xy(x, y)
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass
    
class Plugin(Simple):
    title = 'Orthogonal view'
    note = ['all', 'stack3d']

    #process
    def run(self, ips, imgs, para = None):
        ips.tool = Orthogonal()