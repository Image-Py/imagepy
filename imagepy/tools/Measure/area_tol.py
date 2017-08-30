# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 13:31:36 2017

@author: yxl
"""

import wx
from shapely.geometry import Polygon, Point
from imagepy.core.engine import Tool
from .setting import Setting
from imagepy import IPy
    
class Area:
    """Define the area class"""
    dtype = 'area'
    def __init__(self, body=None, unit=None):
        self.body = body if body!=None else []
        self.buf, self.unit = [], unit
        
    def addpoint(self, p):
        self.buf.append(p)
        
    def commit(self):  
        if len(self.buf)<3:return False
        if self.buf[0]!=self.buf[-1]:
            self.buf.append(self.buf[0])
        self.body.append(self.buf)
        self.buf = []
        
    def snap(self, x, y, lim):
        cur, cid, minl = None, None, 1000
        for pg in self.body:
            for i in pg:
                d = (i[0]-x)**2+(i[1]-y)**2
                if d < minl:cur,cid,minl = pg,i,d
        if minl**0.5>lim:return None
        return cur, cur.index(cid)

    def pick(self, x, y, lim):
        rst = self.snap(x, y, lim)
        if rst!=None:return rst
        for i in self.body:
            if Polygon(i).contains(Point(x,y)):
                return True, i
        return None
    
    def draged(self, ox, oy, nx, ny, i):
        self.update, self.infoupdate = True, True
        if i[0]==True:
            for j in range(len(i[1])):
                i[1][j] = (i[1][j][0]+(nx-ox), i[1][j][1]+(ny-oy))
        else:
            i[0][i[1]] = (nx, ny)
            #print('drag,',i,self.body[0][0][i]hasattr(ips.roi, 'topolygon'))
            if i[1]==0:i[0][-1] = (nx,ny)
            if i[1]==len(i[0])-1:
                i[0][0] = (nx, ny)

    def report(self, title):
        rst = []
        titles = ['Area', 'OX', 'OY']
        for pg in self.body:
            plg = Polygon(pg)
            area, xy = plg.area, plg.centroid
            unit = 1 if self.unit==None else self.unit[0]
            axy = [area*unit**2, xy.x*unit, xy.y*unit]
            rst.append([round(i,1) for i in axy])
        IPy.table(title, rst, titles)
            
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen(Setting['color'], width=1, style=wx.SOLID))
        dc.SetTextForeground(Setting['tcolor'])
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        
        dc.SetFont(font)
        dc.DrawLines([f(*i) for i in self.buf])
        for i in self.buf:dc.DrawCircle(f(*i),2)
            
        for pg in self.body:
            plg = Polygon(pg)
            dc.DrawLines([f(*i) for i in pg])
            for i in pg: dc.DrawCircle(f(*i),2)
            area, xy = plg.area, plg.centroid
            if self.unit!=None: 
                area *= self.unit[0]**2
            dc.DrawText('%.1f'%area, f(xy.x, xy.y))

class Plugin(Tool):
    """Define the area class plugin with some events callback fucntions """
    title = 'Area'
    def __init__(self):
        self.curobj = None
        self.doing = False
            
    def mouse_down(self, ips, x, y, btn, **key): 
        if key['ctrl'] and key['alt']:
            if isinstance(ips.mark, Area):
                ips.mark.report(ips.title)
            return

        lim = 5.0/key['canvas'].get_scale() 
        if btn==1:
            if not self.doing:
                if isinstance(ips.mark, Area):
                    self.curobj = ips.mark.pick(x, y, lim)
                if not self.curobj in (None,True):return
                if not isinstance(ips.mark, Area):
                    ips.mark = Area(unit=ips.unit)
                    self.doing = True
                elif isinstance(ips.mark, Area):
                    if key['shift']: self.oper,self.doing = '+',True
                    elif self.curobj: return
                    else: ips.mark=None
            if self.doing:
                ips.mark.addpoint((x,y))
                self.curobj = (ips.mark.buf, -1)
                self.odx, self.ody = x, y
                
        elif btn==3:
            if self.doing:
                ips.mark.addpoint((x,y))
                self.doing = False
                ips.mark.commit()
        ips.update = True
    
    def mouse_move(self, ips, x, y, btn, **key):
        if not isinstance(ips.mark, Area):return
        lim = 5.0/key['canvas'].get_scale()        
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.mark.snap(x, y, lim)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            ips.mark.draged(self.odx, self.ody, x, y, self.curobj)
            ips.update = True
        self.odx, self.ody = x, y

    def mouse_up(self, ips, x, y, btn, **key):
        self.curobj = None
        
    def on_switch(self):
        print('AreaTool_Plugin')