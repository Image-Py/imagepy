from .shpbase import pick_obj, pick_point, drag, offset
from .. import ImageTool, ShapeTool
from ...object import Point, Line, Polygon, Layer, Points, Texts
from ...object.roi import *
import numpy as np
from numpy.linalg import norm

def mark(shp, types = 'all'):
    pts = []
    if not (types=='all' or shp.dtype in types): return pts
    if shp.dtype == 'point': pts.append([shp.body])
    if shp.dtype == 'line': pts.append(shp.body)
    if shp.dtype == 'polygon': pts.append(shp.body[0])
    if shp.dtype == 'layer':
        minl, obj = 1e8, None
        for i in shp.body:
            pts.extend(mark(i, types))
    return pts

class BaseEditor(ShapeTool):
    def __init__(self, dtype='all'):
        self.status, self.oldxy, self.p = '', None, None
        self.pick_m, self.pick_obj = None, None

    def mouse_down(self, shp, x, y, btn, **key):
        self.p = x, y
        if btn==2:
            self.status = 'move'
            self.oldxy = key['px'], key['py']
        if btn==1 and self.status=='pick':
            m, obj, l = pick_point(shp, x, y, 5)
            self.pick_m, self.pick_obj = m, obj
        if btn==1 and self.pick_m is None:
            m, l = pick_obj(shp, x, y, 5)
            self.pick_m, self.pick_obj = m, None
        if btn==3:
            obj, l = pick_obj(shp, x, y, 5)
            if key['alt'] and not key['ctrl']:
                if obj is None: del shp.body[:]
                else: shp.body.remove(obj)
                shp.measure_mark()
                shp.dirty = True
            if not (key['shift'] or key['alt'] or key['ctrl']):
                key['canvas'].fit()

    def mouse_up(self, shp, x, y, btn, **key):
        self.status = ''
        if btn==1:
            self.pick_m = self.pick_obj = None
            if not (key['alt'] and key['ctrl']): return
            pts = mark(shp)
            if len(pts)>0: 
                pts = Points(np.vstack(pts), color=(255,0,0))
                key['canvas'].marks['anchor'] = pts
            shp.dirty = True

    def mouse_move(self, shp, x, y, btn, **key):
        self.cursor = 'arrow'
        if self.status == 'move':
            ox, oy = self.oldxy
            up = (1,-1)[key['canvas'].up]
            key['canvas'].move(key['px']-ox, (key['py']-oy)*up)
            self.oldxy = key['px'], key['py']
        if key['alt'] and key['ctrl']:
            self.status = 'pick'
            if not 'anchor' in key['canvas'].marks: 
                pts = mark(shp)
                if len(pts)>0: 
                    pts = Points(np.vstack(pts), color=(255,0,0))
                    key['canvas'].marks['anchor'] = pts
            if 'anchor' in key['canvas'].marks:
                m, obj, l = pick_point(key['canvas'].marks['anchor'], x, y, 5)
                if not m is None: self.cursor = 'hand'
        elif 'anchor' in key['canvas'].marks: 
            self.status = ''
            del key['canvas'].marks['anchor']
            shp.dirty = True
        if not self.pick_obj is None and not self.pick_m is None:
            drag(self.pick_m, self.pick_obj, x, y)
            shp.measure_mark()
            pts = mark(self.pick_m)
            if len(pts)>0:
                pts = np.vstack(pts)
                key['canvas'].marks['anchor'] = Points(pts, color=(255,0,0))
            self.pick_m.dirty = True
            shp.dirty = True
        if self.pick_obj is None and not self.pick_m is None:
            offset(self.pick_m, x-self.p[0], y-self.p[1])
            pts = mark(self.pick_m)
            if len(pts)>0:
                pts = np.vstack(pts)
                key['canvas'].marks['anchor'] = Points(pts, color=(255,0,0))
            shp.measure_mark()
            self.p = x, y
            self.pick_m.dirty = shp.dirty = True

    def mouse_wheel(self, shp, x, y, d, **key):
        if d>0: key['canvas'].zoomout(x, y, coord='data')
        if d<0: key['canvas'].zoomin(x, y, coord='data')

class BaseMeasure(ImageTool):
    def __init__(self, base): 
        base.__init__(self)
        self.base = base

    def mouse_down(self, img, x, y, btn, **key):
        if img.mark is None: img.mark = Measure()
        self.base.mouse_down(self, img.mark, x, y, btn, **key)

    def mouse_up(self, img, x, y, btn, **key):
        self.base.mouse_up(self, img.mark, x, y, btn, **key)
        if not img.mark is None:
            if len(img.mark.body)==0: img.mark = None

    def mouse_move(self, img, x, y, btn, **key):
        self.base.mouse_move(self, img.mark, x, y, btn, **key)

    def mouse_wheel(self, img, x, y, d, **key):
        self.base.mouse_wheel(self, img.mark, x, y, d, **key)

def inbase(key, btn):
    status = key['ctrl'], key['alt'], key['shift']
    return status == (1,1,0) or btn in {2,3}

class PointEditor(BaseEditor):
    title = 'Point Tool'
    def __init__(self): 
        BaseEditor.__init__(self)

    def mouse_down(self, shp, x, y, btn, **key):
        if inbase(key, btn):
            BaseEditor.mouse_down(self, shp, x, y, btn, **key)
        if btn==1 and not key['alt'] and not key['ctrl']:
            shp.body.append(Coordinate([x,y]))
            shp.measure_mark()
            shp.dirty = True

class LineEditor(BaseEditor):
    title = 'Line Tool'
    def __init__(self, tp): 
        BaseEditor.__init__(self)
        self.cur, self.n, self.obj, self.tp = 0, 0, None, tp

    def mouse_down(self, shp, x, y, btn, **key):
        if inbase(key, btn) and self.obj is None:
            BaseEditor.mouse_down(self, shp, x, y, btn, **key)
        if key['alt'] and key['ctrl']: return
        if btn==1:
            if self.obj is None: 
                self.obj = self.tp([(x,y)])
                shp.body.append(self.obj)
            else: 
                self.obj.body = np.vstack((self.obj.body, [(x,y)]))
            anchor = Points(mark(self.obj)[0], color=(255,0,0))
            key['canvas'].marks['buffer'] = anchor
        if btn==3 and not self.obj is None :
            self.obj.body = np.vstack((self.obj.body, [(x,y)]))
            self.obj.dirty, shp.dirty, self.obj = True, True, None
            del key['canvas'].marks['buffer']
        shp.measure_mark()
        shp.dirty = True

class AreaEditor(BaseEditor):
    title = 'Polygon Tool'
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
            shp.body[-1] = Area(body)
            shp.measure_mark()
            self.obj, shp.dirty = None, True
            del key['canvas'].marks['buffer']
        shp.dirty = True

class DistanceEditor(LineEditor):
    def __init__(self): LineEditor.__init__(self, Distance)

class AngleEditor(LineEditor):
    def __init__(self): LineEditor.__init__(self, Angle)

class SlopEditor(LineEditor):
    def __init__(self): LineEditor.__init__(self, Slope)

class CoordinateTool(BaseMeasure):
    title = 'Coordinate Tool'
    def __init__(self): 
        BaseMeasure.__init__(self, PointEditor)

class DistanceTool(BaseMeasure):
    title = 'Distance Tool'
    def __init__(self): 
        BaseMeasure.__init__(self, DistanceEditor)

class AngleTool(BaseMeasure):
    title = 'Angle Tool'
    def __init__(self): 
        BaseMeasure.__init__(self, AngleEditor)

class SlopeTool(BaseMeasure):
    title = 'Slop Tool'
    def __init__(self): 
        BaseMeasure.__init__(self, SlopEditor)

class AreaTool(BaseMeasure):
    title = 'Area Tool'
    def __init__(self):
        BaseMeasure.__init__(self, AreaEditor)