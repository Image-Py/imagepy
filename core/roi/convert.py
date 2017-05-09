# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 03:05:20 2016
@author: yxl
"""
from __future__ import absolute_import
from shapely.geometry import *

def r2s_point(mp):
    return MultiPoint(mp.body)

def s2r_points(mp):  
    from .pointroi import PointRoi
    body = list(LineString(mp).coords)
    return PointRoi(body)
    
def s2r_point(p):
    from .pointroi import PointRoi
    return PointRoi(list(p.coords))
    
def r2s_line(ml):
    return MultiLineString(ml.body)
    
def s2r_lines(ml):
    from .lineroi import LineRoi
    body = [list(i.coords for i in ml)]
    return LineRoi(body)
    
def s2r_line(ml):
    from .lineroi import LineRoi
    return LineRoi([list(ml.coords)])
    
def r2s_polygon(pg):
    pgs = []
    for i in pg.body:
        pgs.append(Polygon(i[0], i[1]))
    return MultiPolygon(pgs)

def s2r_polygon(pg):
    from .polygonroi import PolygonRoi
    if pg.exterior == None:return None
    out = list(pg.exterior.coords)
    inn = [list(i.coords) for i in list(pg.interiors)]
    return PolygonRoi([[out, inn]])
    
def s2r_polygons(pg):
    from .polygonroi import PolygonRoi
    body = []
    for p in pg:
        if p.exterior == None: continue
        out = list(p.exterior.coords)
        inn = [list(i.coords) for i in list(p.interiors)]
        body.append([out, inn])
    if len(body)==0:return None
    return PolygonRoi(body)
    
def roi2shape(roi):
    from .lineroi import LineRoi
    from .polygonroi import PolygonRoi
    from .pointroi import PointRoi
    from .rectangleroi import RectangleRoi
    from .ovalroi import OvalRoi
    
    if isinstance(roi, PointRoi):
        return r2s_point(roi)
    if isinstance(roi, LineRoi):
        return r2s_line(roi)
    if isinstance(roi, PolygonRoi):
        return r2s_polygon(roi)
    if isinstance(roi, RectangleRoi):
        return r2s_polygon(roi.topolygon())
    if isinstance(roi, OvalRoi):
        return r2s_polygon(roi.topolygon())
    
def shape2roi(shape):
    if isinstance(shape, Point):
        return s2r_point(shape)
    if isinstance(shape, MultiPoint):
        return s2r_points(shape)
    if isinstance(shape, LineString):
        return s2r_line(shape)
    if isinstance(shape, MultiLineString):
        return s2r_lines(shape)
    if isinstance(shape, Polygon):
        return s2r_polygon(shape)
    if isinstance(shape, MultiPolygon):
        return s2r_polygons(shape)
        
if __name__ == '__main__':
    import sys
    sys.path.append('../../')
    from .rectangleroi import RectangleRoi
    from .ovalroi import OvalRoi
    r = RectangleRoi(0,0,101,101)
    o = OvalRoi(40,40,60,60)
    sr = roi2shape(r)
    so = roi2shape(o)