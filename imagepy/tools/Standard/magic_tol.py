# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
import wx
from sciapp.action import ImageTool, BaseROI, BaseEditor
from sciapp.util import geom_union, geom_flatten, geom2shp
from sciapp.object import ROI
import numpy as np
from skimage.morphology import flood_fill, flood
from skimage.measure import find_contours
from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union


def polygonize(conts, withholes = True):
    for i in conts:i[:,[0,1]] = i[:,[1,0]]
    polygon = Polygon(conts[0]).buffer(0)
    if not withholes:return polygon
    holes = []
    for i in conts[1:]:
        if len(i)<4:continue
        holes.append(Polygon(i).buffer(0))
    hole = cascaded_union(holes)
    return polygon.difference(hole)

def magic_cont(img, x, y, conn, tor):
    img = img.reshape((img.shape+(1,))[:3])
    msk = np.ones(img.shape[:2], dtype='bool')
    for i in range(img.shape[2]):
        msk &= flood(img[:,:,i], (int(y),int(x)), 
            connectivity=conn, tolerance=tor)
    return find_contours(msk, 0, 'high')

def inbase(key, btn):
    status = key['ctrl'], key['alt'], key['shift']
    return status == (1,1,0) or btn in {2,3}

class Plugin(BaseROI):
    title = 'Magic Stick'
    para = {'tor':10, 'con':'8-connect'}
    view = [(int, 'tor', (0,1000), 0, 'torlorance', 'value'),
            (list, 'con', ['4-connect', '8-connect'], str, 'fill', 'pix')]

    
    def __init__(self): 
        BaseROI.__init__(self, BaseEditor)

    def mouse_down(self, ips, x, y, btn, **key):
        if ips.roi is None: ips.roi = ROI()
        else: ips.roi.msk = None
        if inbase(key, btn):
            BaseEditor.mouse_down(self, ips.roi, x, y, btn, **key)
        if key['alt'] and key['ctrl']: return
        if btn==1:
            conts = magic_cont(ips.img, x, y, 
                (self.para['con']=='8-connect')+1, self.para['tor'])
            ips.roi.body.append(geom2shp(polygonize(conts)))
            ips.roi.dirty = True

            if key['alt'] or key['shift']:
                obj = ips.roi.body.pop(-1)
                rst = geom_union(ips.roi.to_geom())
                if key['alt'] and not key['shift']:
                    rst = rst.difference(obj.to_geom())
                if key['shift'] and not key['alt']:
                    rst = rst.union(obj.to_geom())
                if key['shift'] and key['alt']:
                    rst = rst.intersection(obj.to_geom())
                layer = geom2shp(geom_flatten(rst))
                ips.roi.body = layer.body
            ips.roi.dirty = True

    '''

    def __init__(self): 
        BaseEditor.__init__(self)
        self.cur, self.n, self.obj = 0, 0, None

    def mouse_down(self, shp, x, y, btn, **key):
        if inbase(key, btn) and self.obj is None:
            BaseEditor.mouse_down(self, shp, x, y, btn, **key)
        if key['alt'] and key['ctrl']: return
        if btn==1:
            if self.obj is None: 
                self.obj = Line([(x,y)])
                shp.body.append(self.obj)
            else: 
                self.obj.body = np.vstack((self.obj.body, [(x,y)]))
            anchor = Points(mark(self.obj)[0], color=(255,0,0))
            key['canvas'].marks['buffer'] = anchor
        if btn==3 and not self.obj is None :
            body = np.vstack((self.obj.body, [(x,y)]))
            shp.body[-1] = Polygon(body)
            if key['alt'] or key['shift']:
                obj = shp.body.pop(-1)
                rst = geom_union(shp.to_geom())
                if key['alt'] and not key['shift']:
                    rst = rst.difference(obj.to_geom())
                if key['shift'] and not key['alt']:
                    rst = rst.union(obj.to_geom())
                if key['shift'] and key['alt']:
                    rst = rst.intersection(obj.to_geom())
                layer = geom2shp(geom_flatten(rst))
                shp.body = layer.body
            self.obj, shp.dirty = None, True
            del key['canvas'].marks['buffer']
        shp.dirty = True

    '''