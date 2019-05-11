# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:03:15 2016
@author: yxl
"""
from __future__ import absolute_import
import numpy as np
from ..draw import polygonfill
from ..manager import ColorManager

def match_color(img, color):
    if hasattr(color, '__iter__') and len(img.shape)==2:
        return np.mean(color)
    return color

class Paint:
    def __init__(self, width=1):
        self.width = 1
        self.curpt = (0,0)

    def set_curpt(self, x,y):
        self.curpt = x,y

    def draw_pixs(self, img, xs, ys, color=None):
        mskx = (xs>=0) * (xs<img.shape[1])
        msky = (ys>=0) * (ys<img.shape[0])
        msk = mskx * msky
        if color == None:color = ColorManager.get_front()
        color = match_color(img, color)
        img[ys[msk], xs[msk]] = color

    def draw_point(self, img, x, y, r=1, color=None):
        shape = img.shape
        x, y = np.round((x,y)).astype(np.int)
        if x<0 or y<0 or x>=shape[1] or y>=shape[0]: return
        if color == None:color = ColorManager.get_front()
        color = match_color(img, color)
        if r==1: img[y,x] = color
        n = int(r)
        xs,ys = np.mgrid[-n:n+1,-n:n+1]
        msk = np.sqrt(xs**2+ys**2)<r
        self.draw_pixs(img, xs[msk]+x, ys[msk]+y, color)

    def draw_line(self, img, x1, y1, x2, y2, w=None, color=None):
        x1, y1, x2, y2 = [int(round(i)) for i in (x1, y1, x2, y2)]
        if w==None:w=self.width
        dx, dy = x2-x1, y2-y1
        n = max(abs(dx), abs(dy)) + 1
        xs = np.linspace(x1, x2, n).round().astype(np.int16)
        ys = np.linspace(y1, y2, n).round().astype(np.int16)
        for x, y in zip(xs, ys):
            self.draw_point(img, x, y, w, color)

    def lineto(self, img, x, y, w=None, color=None):
        self.draw_line(img, self.curpt[0], self.curpt[1], x, y, w, color)
        self.curpt = x, y

    def draw_path(self, img, xs, ys, w=None, color=None):
        self.set_curpt(xs[0], ys[0])
        ## TODO:Fixme! 
        #for x,y in zip(xs,ys)[1:]:
        for x,y in list(zip(xs,ys))[1:]:
            self.lineto(img,x,y,w,color)

    def fill_polygon(self, pg, img, holes=[], color=None):
        if color == None:color = ColorManager.get_front()
        color = match_color(img, color)
        pgs = [pg] + holes
        polygonfill.fill(pgs, img, color)
