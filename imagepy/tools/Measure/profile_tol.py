# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 22:21:32 2017

@author: yxl
"""

import wx
#from imagepy import IPy
from sciapp.action import ImageTool
import numpy as np
import pandas as pd
from numpy.linalg import norm
from math import ceil

class Profile:
    """Define the profile class"""
    dtype = 'distance'
    def __init__(self, body=None, unit=None):
        self.body = body if body!=None else []
        self.buf, self.unit = [], unit

    def addline(self):
        line = self.buf
        if len(line)!=2 or line[0] !=line[-1]:
            self.body.append(line)
        self.buf = []

    def snap(self, x, y, lim):
        minl, idx = 1000, None
        for i in self.body:
            for j in i:
                d = (j[0]-x)**2+(j[1]-y)**2
                if d < minl:minl,idx = d,(i, i.index(j))
        return idx if minl**0.5<lim else None

    def pick(self, x, y, lim):
        return self.snap(x, y, lim)

    def draged(self, ox, oy, nx, ny, i):
        i[0][i[1]] = (nx, ny)

    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen(Setting['color'], width=1, style=wx.SOLID))
        dc.SetTextForeground(Setting['tcolor'])
        linefont = wx.Font(10, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dc.SetFont(linefont)
        if len(self.buf)>1:
            dc.DrawLines([f(*i) for i in self.buf])
        for i in self.buf:dc.DrawCircle(f(*i),2)
        for line in self.body:
            dc.DrawLines([f(*i) for i in line])
            for i in line:dc.DrawCircle(f(*i),2)
            pts = np.array(line)
            mid = (pts[:-1]+pts[1:])/2

            dxy = (pts[:-1]-pts[1:])
            dis = norm(dxy, axis=1)
            unit = 1 if self.unit is None else self.unit[0]
            for i,j in zip(dis, mid):
                dc.DrawText('%.2f'%(i*unit), f(*j))

    def report(self, title):
        rst, titles = [], ['K']
        for line in self.body:
            pts = np.array(line)
            mid = (pts[:-1]+pts[1:])/2

            dxy = (pts[:-1]-pts[1:])
            dxy[:,1][dxy[:,1]==0] = 1
            l = norm(dxy, axis=1)*-np.sign(dxy[:,1])
            rst.append(np.round(np.arccos(dxy[:,0]/l)/np.pi*180,1))
        IPy.show_table(pd.DataFrame(rst, columns=titles), title)

class Plugin(ImageTool):
    """Define the profile class plugin with the event callback functions"""
    title = 'Profile'
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.odx,self.ody = 0, 0

    def mouse_down(self, ips, x, y, btn, **key):
        if key['ctrl'] and key['alt']:
            if isinstance(ips.mark, Profile):
                ips.mark.report(ips.title)
            return
        lim = 5.0/key['canvas'].scale
        if btn==1:
            if not self.doing:
                if isinstance(ips.mark, Profile):
                    self.curobj = ips.mark.pick(x, y, lim)
                if self.curobj!=None:return

                if not isinstance(ips.mark, Profile):
                    ips.mark = Profile(unit=ips.unit)
                    self.doing = True
                else: ips.mark = None
            if self.doing:
                ips.mark.buf.append((x,y))
                ips.mark.buf.append((x,y))
                self.curobj = (ips.mark.buf, -1)
                self.odx, self.ody = x,y
        ips.update()

    def mouse_up(self, ips, x, y, btn, **key):
        self.curobj = None
        if self.doing:
            ips.mark.addline()
        self.doing = False
        if ips.mark!=None and len(ips.mark.body)==1:
            self.profile(ips.mark.body, ips.img)
        ips.update()

    def mouse_move(self, ips, x, y, btn, **key):
        if not isinstance(ips.mark, Profile):return
        lim = 5.0/key['canvas'].scale      
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.mark.snap(x, y, lim)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            ips.mark.draged(self.odx, self.ody, x, y, self.curobj)
            ips.update()
            #PlotFrame.plot(np.random.rand(100))
        self.odx, self.ody = x, y

    def profile(self, body, img):
        (x1, y1), (x2, y2) = body[0]
        dx, dy = x2-x1, y2-y1
        n = max(abs(dx), abs(dy)) + 1
        xs = np.linspace(x1, x2, n).round().astype(np.int16)
        ys = np.linspace(y1, y2, n).round().astype(np.int16)
        msk = (xs>=0) * (xs<img.shape[1])
        msk*= (ys>=0) * (ys<img.shape[0])
        ix = np.arange(len(xs))

        frame = IPy.plot('Profile', 'Profile - Line', 'pixels coordinate', 'value of pixcels')
        frame.clear()
        if len(img.shape) == 3:
            vs = np.zeros((3,len(xs)), dtype=np.int16)
            vs[:,msk] = img[ys[msk], xs[msk]].T
            frame.add_data(ix, vs[0], (255,0,0), 1)
            frame.add_data(ix, vs[1], (0,255,0), 1)
            frame.add_data(ix, vs[2], (0,0,255), 1)
        else: 
            vs = np.zeros(len(xs), dtype=np.int16)
            vs[msk] = img[ys[msk], xs[msk]]
            frame.add_data(ix, vs, (0,0,0), 1)
        frame.draw()

    def mouse_wheel(self, ips, x, y, d, **key):
        pass

if __name__ == '__main__':
    app = wx.App(False)
    frame = PlotFrame(None)
    frame.Show()
    app.MainLoop()