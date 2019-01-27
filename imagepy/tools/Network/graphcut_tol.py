# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016
@author: yxl
"""
from imagepy.core.engine import Tool
import numpy as np
import wx
from numba import jit

@jit
def floodfill(img, x, y):
    buf = np.zeros((131072,2), dtype=np.uint16)
    color = img[int(y), int(x)]
    img[int(y), int(x)] = 0
    buf[0,0] = x; buf[0,1] = y;
    cur = 0; s = 1;

    while True:
        xy = buf[cur]
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                cx = xy[0]+dx; cy = xy[1]+dy
                if cx<0 or cx>=img.shape[1]:continue
                if cy<0 or cy>=img.shape[0]:continue
                if img[cy, cx]!=color:continue
                img[cy, cx] = 0
                buf[s,0] = cx; buf[s,1] = cy
                s+=1
                if s==len(buf):
                    buf[:len(buf)-cur] = buf[cur:]
                    s -= cur; cur=0
        cur += 1
        if cur==s:break

def cut(img, lines):
    if len(lines)<2:return
    lines = np.array(lines).round()
    ox,oy = lines[0]
    for i in lines[1:]:
        cx, cy = i
        dx, dy = cx-ox, cy-oy
        n = max(abs(dx), abs(dy)) + 1
        xs = np.linspace(cx, ox, n).round().astype(np.int16)
        ys = np.linspace(cy, oy, n).round().astype(np.int16)
        for x,y in zip(xs, ys):
            for dxy in [(1,0),(0,1)]:
                xx = x + dxy[0]
                yy = y + dxy[1]
                if xx<0 or xx>img.shape[1]: continue
                if yy<0 or yy>img.shape[0]: continue
                if img[yy,xx] == 0: continue
                floodfill(img, xx, yy)
        ox, oy = i

class Mark():
    def __init__(self, line):
        self.line = line

    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((255,0,0), width=2, style=wx.SOLID))
        dc.DrawLines([f(*i) for i in self.line])

class Plugin(Tool):
    title = 'Graph Cut'
    def __init__(self):
        self.status = 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        if btn==1:
            ips.snapshot()
            self.status = 1
            self.cur = [(x, y)]
            ips.mark = Mark(self.cur)
            ips.update()
    
    def mouse_up(self, ips, x, y, btn, **key):
        ips.mark = None
        self.status = 0
        cut(ips.img, self.cur)
        ips.update()
    
    def mouse_move(self, ips, x, y, btn, **key):
        if self.status==1:
            self.cur.append((x, y))
            ips.update()
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass