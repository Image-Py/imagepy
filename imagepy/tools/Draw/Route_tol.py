# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from sciapp.action import Filter
from sciapp.action import ImageTool
import numpy as np
from sciapp.util import mark2shp
from sciapp.action import ImageTool
#from imagepy.core.manager import ColorManager
#from imagepy.core.roi import lineroi
#from imagepy.core.mark import GeometryMark
from skimage.graph import route_through_array
import scipy.ndimage as ndimg

def route_through(ips, snap, poins,para):
    para['max']=True
    para['lcost']=2
    img = snap.astype('float32')
    if para['max']: img *= -1
    np.add(img, para['lcost']-img.min(), casting='unsafe', out=img)
    minv, maxv = ips.range
    routes = []
    for line in poins:
        pts = np.array(list(zip(line[:-1], line[1:])))
        for p0, p1 in pts[:,:,::-1].astype(int):
            indices, weight = route_through_array(img, p0, p1)
            routes.append(indices)
    return routes

class Plugin(ImageTool):
    title = 'Route Toolk'
    note = ['auto_snap','8-bit', '16-bit','int', 'float','2int', 'preview']
    para = {'fully connected':True, 'lcost':0, 'max':False, 'geometric':True, 'type':'ROI'}
    view = [(float, 'lcost', (0, 1e5), 3, 'step', 'cost'),
            (bool, 'max', 'max cost'),
            (bool, 'fully connected', 'fully connected'),
            (bool, 'geometric', 'geometric'),
            (list, 'type', ['white line', 'ROI'], str, 'output', '')]

    def __init__(self):
        self.curobj = None
        self.doing = 'Nothing'
        #初始化线条缓存
        # self.helper = AnchorLine()
        self.odx,self.ody = 0, 0
        self.cursor = 'cross'
        self.buf=[]

    def mouse_down(self, ips, x, y, btn, **key):
        # print(key['canvas'].scale)
        lim = 5.0/key['canvas'].scale 
        if btn==2: 
            if key['ctrl']:
                if len(self.buf)>1:
                    lines=route_through(ips, ips.img,[self.buf],self.para)
                    rs, cs = np.vstack(lines).T
                    minv, maxv = ips.range
                    if self.para['type']=='white line':
                        # ips.img[:,:] = minv
                        ips.img[rs,cs] = maxv
                    elif self.para['type']=='ROI':
                        ips.img[:,:] = minv
                        ips.img[rs,cs] = maxv
                        ndimg.binary_fill_holes(ips.img.copy(), output=ips.img)
                        ips.img[:,:] *=  255
                    self.buf=[]
                    self.draw(ips)
                    return
            else:
                self.oldp = key['canvas'].to_panel_coor(x,y)
                self.do_old=self.doing
                self.doing = 'all_move'
                return 
        #左键按下
        elif btn==1:
            if self.doing=='Nothing':
                if len(self.buf) == 0:
                    self.doing ='draw'
            elif self.doing=='draw' and self.cursor=='hand':
                a=self.in_points(x,y,lim)
                if a!=(-1,-1):
                    # print('doing to move')
                    self.doing='move'
                    #记录第几个点被改变
                    self.p_index=self.buf.index(a)
            elif self.doing=='down':
                #判断是否在点内，如果在，说明在移动
                a=self.in_points(x,y,lim)
                if a!=(-1,-1):
                    self.doing='move'
                    self.p_index=self.buf.index(a)
                    return
                self.buf=[]
                self.doing='Nothing'
                self.draw(ips)
                return
            if self.doing=='draw' and self.cursor=='cross':
                self.addpoint((x,y))
                self.draw(ips)
        elif btn == 3:

            if (self.doing=='draw' or self.doing=='down')and key['ctrl']:
                a=self.in_points(x,y,lim)
                if a!=(-1,-1):self.delete(self.buf.index(a))
                self.draw(ips)
            elif self.doing=='draw':
                self.addpoint((x,y))
                self.addpoint(self.buf[0])
                self.draw(ips)
                self.doing='down'

    def mouse_up(self, ips, x, y, btn, **key):
        if self.doing == 'move' and btn == 1:
            self.doing = 'draw'
        elif self.doing == 'all_move' and  btn ==2:
            self.doing = self.do_old

    def mouse_move(self, ips, x, y, btn, **key):
        if len(self.buf)==0:return
        lim = 5.0/key['canvas'].scale  
        #如果鼠标移动的同时没有按下   
        if btn==1:
            #如果在鼠标是手的时候左键按下，而且在移动，说明在修改点的位置
            if  self.doing=='move':
                self.change(self.p_index,(x,y))
                self.draw(ips)
        elif btn==None:
            #鼠标变成一个十字架
            self.cursor = 'cross'
            a=self.in_points(x,y,lim)
            if a!=(-1,-1):
                self.cursor = 'hand'
        if self.doing == 'all_move':
            x,y = key['canvas'].to_panel_coor(x,y)
            key['canvas'].move(x-self.oldp[0], y-self.oldp[1])
            self.oldp = x, y
            ips.update()
            # print('move')
        self.odx, self.ody = x, y

    def in_points(self,x,y,range):
        for i in self.buf:
            if ((i[0]>x-range) and (i[0]<x+range)) and  ((i[1]>y-range) and (i[1]<y+range)):
                #返回找到的位置
                return i
        #返回没有找到
        return (-1,-1)

    def mouse_wheel(self, ips, x, y, d, **key):pass

    def pop(self):
        a = self.buf
        self.buf = []
        return a

    def change(self,location,val):
        self.buf[location]=val

    def delete(self,location):
        self.buf.pop(location)

    def addpoint(self, p):
        self.buf.append(p)

    def draw(self,ips):
        mark = {'type':'layers', 'body':{}}
        layer = {'type':'layer', 'body':[]}
        layer['body'].append({'type':'points', 'body':self.buf})
        if len(self.buf)>1:
            lines=route_through(ips, ips.img,[self.buf],self.para)
            lst=[]
            for line in lines:lst.append([(j,i) for i,j in line])
            layer['body'].append({'type':'lines', 'body':lst})
        mark['body'][0] = layer
        ips.mark = mark2shp(mark)
        ips.update()     
        
    def mouse_wheel(self, ips, x, y, d, **key):
        if d>0:key['canvas'].zoomout(x, y, 'data')
        if d<0:key['canvas'].zoomin(x, y, 'data')
        ips.update()