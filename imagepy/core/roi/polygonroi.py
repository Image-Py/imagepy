# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:10:33 2016
@author: yxl
"""
import wx
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import cascaded_union
from shapely.ops import polygonize
from ..draw import paint
from .roi import ROI
from ..manager import RoiManager
from imagepy import IPy

def parse_poly(geom):
    out = list(geom.exterior.coords)
    inn = [list(i.coords) for i in list(geom.interiors)]
    return [out, inn]

def parse_mpoly(geom):
    if geom.geom_type == 'Polygon': 
        return[i for i in [parse_poly(geom)] if i != None]
    return [parse_poly(i) for i in list(geom)]
    
def to_segment(pg):
    p = Polygon(pg) if len(pg)>2 else Polygon(*pg)
    if p.is_valid: return [p]
    if len(pg)<3: pg = pg[0]
    line = LineString(pg)
    return polygonize([line.intersection(line)])
    
class PolygonRoi(ROI):
    dtype = 'polygon'
    def __init__(self, body=None):
        self.body = body if body!=None else []
        self.dirty = body!=None
        self.infoupdate = body!=None
        self.box = [1000,1000,-1000,-1000]
        
    def update(self): self.dirty = True

    def addpoint(self, p):
        self.buf[0].append(p)
        
    def commit(self, buf, oper):     
        pgs = []
        if len(buf[0])==0:return False
        if buf[0][0]!=buf[0][-1]:
            buf[0].append(buf[0][0])
        if len(self.body)==0:
            self.body.append(buf)
            buf = [[],[]]
            self.update, self.infoupdate = True, True
            return True
        for i in self.body:
            pgs.extend(to_segment(i))
        unin = cascaded_union(pgs)
        cur = cascaded_union(list(to_segment(buf)))
        if oper=='+':rst = unin.union(cur)
        if oper=='-':rst = unin.difference(cur)
        self.body = parse_mpoly(rst)
        self.update, self.infoupdate = True, True
        
    def snap(self, x, y, z, lim):
        if not self.issimple():return None
        cur, minl = None, 1e8
        for i in self.body[0][0]:
            d = (i[0]-x)**2+(i[1]-y)**2
            if d < minl:cur,minl = i,d
        if minl**0.5>lim:return None
        return self.body[0][0], self.body[0][0].index(cur)

    def pick(self, x, y, z, lim):
        rst = self.snap(x, y, z, lim)
        if rst!=None:return rst
                
        pgs = []
        for i in self.body:
            pgs.extend(to_segment(i))
        unin = cascaded_union(pgs)
        if unin.contains(Point(x,y)):
            return True
        return None
    
    def draged(self, ox, oy, nx, ny, nz, i):
        self.update, self.infoupdate = True, True
        if i==True:
            for pg in self.body:
                pg[0] = [(p[0]+(nx-ox), p[1]+(ny-oy)) for p in pg[0]]
                for i in range(len(pg[1])):
                    pg[1][i] = [(p[0]+(nx-ox), p[1]+(ny-oy)) for p in pg[1][i]]
        else:
            i[0][i[1]] = (nx, ny)
            #print 'drag,',i,self.body[0][0][i]
            if i[1]==0:i[0][-1] = (nx,ny)
            if i[1]==len(i[0])-1:
                i[0][0] = (nx, ny)
            
    def info(self, ips, cur):
        if cur==None:return
        IPy.set_info('Polygon: %.0f fragments'%len(self.body))

    def countbox(self):
        self.box = [1000,1000,-1000,-1000]
        for i in self.body:
            for x,y in i[0]:
                if x<self.box[0]:self.box[0]=x
                if x>self.box[2]:self.box[2]=x
                if y<self.box[1]:self.box[1]=y
                if y>self.box[3]:self.box[3]=y
        
    def get_box(self):
        if self.infoupdate:
            self.countbox()
            self.infoupdate=False
        return self.box
            
    def issimple(self):
        if len(self.body)==1 and len(self.body[0][1])==0:
            return True
        
    def topolygon(self):return self
     
    '''   
    def affine(self, m, o):
        plg = PolygonRoi()
        plg.body = affine(self.body, m, o)
        plg.update()
        plg.infoupdate()
        return plg
    '''
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen(RoiManager.get_color(), width=RoiManager.get_lw(), style=wx.SOLID))
        for pg in self.body:
            dc.DrawLines([f(*i) for i in pg[0]])
            if self.issimple():
                for i in pg[0]: dc.DrawCircle(f(*i),2)
            for hole in pg[1]:
                dc.DrawLines([f(*i) for i in hole])
            
    def sketch(self, img, w=1, color=None):
        pen = paint.Paint()
        for i in self.body:
            xs, ys = [x[0] for x in i[0]], [x[1] for x in i[0]]
            pen.draw_path(img, xs, ys, w)
            for j in i[1]:
                xs, ys = [x[0] for x in j], [x[1] for x in j]
                pen.draw_path(img, xs, ys, w, color) 
               
    def fill(self, img, color=None):
        pen = paint.Paint()
        for i in self.body:
            pen.fill_polygon(i[0], img, i[1], color)