import numpy as np
from time import time
from collections import Iterable
import shapely.geometry as geom
from shapely.ops import unary_union

def merge(a, b):
    x1, y1 = min(a[0],b[0]), min(a[1],b[1])
    x2, y2 = max(a[2],b[2]), max(a[3],b[3])
    return [x1, y1, x2, y2]

class Shape:
    default = {'color':(255,255,0), 'fcolor':(255,255,255), 
    'fill':False, 'lw':1, 'tcolor':(255,0,0), 'size':8}
    dtype = 'shape'
    def __init__(self, body=None, **key):
        self.name = 'shape'
        self.body = [] if body is None else body
        self.color = key['color'] if 'color' in key else None
        self.fcolor = key.get('fcolor', None)
        self.lstyle = key.get('style', None)
        self.tcolor = key.get('tcolor', None)
        self.lw = key.get('lw', None)
        self.r = key.get('r', None)
        self.fill = key.get('fill', None)
        self._box = None
        self.dirty = True

    @property
    def box(self):
        if self._box is None or self.dirty:
            self._box = self.count_box()
        return self._box

    @property
    def style(self):
        styledic = {'type':self.dtype}
        if not self.color is None: styledic['color']=self.color
        if not self.fcolor is None: styledic['fcolor']=self.fcolor
        if not self.lstyle is None: styledic['lstyle']=self.lstyle
        if not self.lw is None: styledic['lw']=self.lw
        if not self.fill is None: styledic['fill']=self.fill
        return styledic
        
    def count_box(self, body=None, box=None):
        if body is None:
            box = [1e10, 1e10,-1e10,-1e10]
            self.count_box(self.body, box)
            return box
        if isinstance(body, np.ndarray):
            body = body.reshape((-1,2))
            minx, miny = body.min(axis=0)
            maxx, maxy = body.max(axis=0)
            newbox = [minx, miny, maxx, maxy]
            box.extend(merge(box, newbox))
            del box[:4]
        else:
            for i in body: self.count_box(i, box)

    @property
    def info(self):
        minx, miny, maxx, maxy = self.box
        return 'Type:%s   minX:%.3f maxX:%.3f, minY:%.3f maxY%.3f'%(
            self.dtype, minx, maxx, miny, maxy)

    def to_mark(self, body):
        mark = self.style
        mark['body'] = body
        return mark

    def to_json(self):
        return geom.mapping(self.to_geom())

    def to_geom(self): pass

    def __str__(self):
        return str(self.to_mark())
    
class Point(Shape):
    dtype = 'point'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def to_mark(self):
        return Shape.to_mark(self, tuple(self.body.tolist()))

    def to_geom(self):
        return geom.Point(self.body)

class Points(Shape):
    dtype = 'points'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def to_mark(self):
        return Shape.to_mark(self, [tuple(i.tolist()) for i in self.body])

    def to_geom(self):
        return geom.MultiPoint(self.body)

class Line(Shape):
    dtype = 'line'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def to_mark(self):
        return Shape.to_mark(self, [tuple(i.tolist()) for i in self.body])

    def to_geom(self):
        return geom.LineString(self.body)

class Lines(Shape):
    dtype = 'lines'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = [np.array(i, dtype=np.float32) for i in body]

    def to_mark(self):
        return Shape.to_mark(self, [[tuple(i.tolist()) for i in j] for j in self.body])

    def to_geom(self):
        return geom.MultiLineString(self.body)
    
class Polygon(Shape):
    dtype = 'polygon'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        if len(body)>0 and not isinstance(body[0][0], Iterable): body = [body]
        self.body = [np.array(i, dtype=np.float32) for i in body]

    def to_mark(self):
        return Shape.to_mark(self, [[tuple(i.tolist()) for i in j] for j in self.body])

    def to_geom(self):
        return geom.Polygon(self.body[0], self.body[1:])

class Polygons(Shape):
    dtype = 'polygons'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        for i in range(len(body)):
            if not isinstance(body[i][0][0], Iterable): body[i] = [body[i]]
        self.body = [[np.array(i, dtype=np.float32) for i in j] for j in body]

    def to_mark(self):
        mark = self.style
        f = lambda x:[[tuple(i.tolist()) for i in j] for j in x]
        return Shape.to_mark(self, [[[tuple(i.tolist()) for i in j] for j in k] for k in self.body])

    def to_geom(self):
        return geom.MultiPolygon([[i[0], i[1:]] for i in self.body])

class Circle(Shape):
    dtype = 'circle'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def count_box(self):
        pts = self.body
        return [pts[0]-pts[2], pts[1]-pts[2], pts[0]+pts[2], pts[1]+pts[2]]
    
    def to_mark(self):
        return Shape.to_mark(self, tuple(self.body.tolist()))

    def to_geom(self):
        return geom.Point(self.body[:2]).buffer(self.body[2])

class Circles(Shape):
    dtype = 'circles'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def count_box(self):
        pts = self.body.T
        return [(pts[0]-pts[2]).min(), (pts[1]-pts[2]).min(), (pts[0]+pts[2]).max(), (pts[1]+pts[2]).max()]
    
    def to_mark(self):
        return Shape.to_mark(self, [tuple(i.tolist()) for i in self.body])

    def to_geom(self):
        return geom.MultiPolygon([geom.Point(i[:2]).buffer(i[2]) for i in self.body])

class Rectangle(Shape):
    dtype = 'rectangle'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def count_box(self):
        return [self.body[0], self.body[1], self.body[0]+self.body[2], self.body[1]+self.body[3]]
    
    def to_mark(self):
        return Shape.to_mark(self, tuple(self.body.tolist()))

    def to_geom(self):
        f = lambda x:[(x[0],x[1]),(x[0],x[1]+x[3]),(x[0]+x[2],x[1]+x[3]),(x[0]+x[2],x[1])]
        return geom.Polygon(f(self.body))

class Rectangles(Shape):
    dtype = 'rectangles'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def count_box(self, body=None, box=None):
        self.body[:,2:] += self.body[:,:2]
        minx, miny = self.body.reshape((-1,2)).min(axis=0)
        maxx, maxy = self.body.reshape((-1,2)).max(axis=0)
        self.body[:,2:] -= self.body[:,:2]
        return [minx, miny, maxx, maxy]
    
    def to_mark(self):
        return Shape.to_mark(self, [tuple(i.tolist()) for i in self.body])

    def to_geom(self):
        f = lambda x:[(x[0],x[1]),(x[0],x[1]+x[3]),(x[0]+x[2],x[1]+x[3]),(x[0]+x[2],x[1])]
        return geom.MultiPolygon([[f(i),[]] for i in self.body])

def make_ellipse(x0, y0, l1, l2, ang):
    m = np.array([[l1*np.cos(-ang),-l2*np.sin(-ang)],
                  [l1*np.sin(-ang),l2*np.cos(-ang)]])
    a = np.linspace(0, np.pi*2, 36)
    xys = np.array((np.cos(a), np.sin(a)))
    return np.dot(m, xys).T + (x0, y0)

class Ellipse(Shape):
    dtype = 'ellipse'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def count_box(self):
        xy = make_ellipse(*self.body)
        (minx, miny), (maxx, maxy) = xy.min(axis=0), xy.max(axis=0)
        return [minx, miny, maxx, maxy]
    
    def to_mark(self):
        return Shape.to_mark(self, tuple(self.body.tolist()))

    def to_geom(self):
        return geom.Polygon(make_ellipse(*self.body))

class Ellipses(Shape):
    dtype = 'ellipses'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body, dtype=np.float32)

    def count_box(self):
        xy = np.vstack([make_ellipse(*i) for i in self.body])
        (minx, miny), (maxx, maxy) = xy.min(axis=0), xy.max(axis=0)
        return [minx, miny, maxx, maxy]
    
    def to_mark(self):
        return Shape.to_mark(self, [tuple(i.tolist()) for i in self.body])

    def to_geom(self):
        return geom.MultiPolygon([[make_ellipse(*i),[]] for i in self.body])

class Text(Shape):
    dtype = 'text'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        self.body = np.array(body[:2], dtype=np.float32)
        self.txt = body[2]

    def to_mark(self):
        return Shape.to_mark(self, tuple(self.body.tolist())+(self.txt,))

    def to_geom(self):
        return geom.Point(self.body)

class Texts(Shape):
    dtype = 'texts'
    def __init__(self, body=[], **key):
        Shape.__init__(self, body, **key)
        body = np.array(body, dtype=object)
        self.body = body[:,:2].astype(np.float32)
        self.txt = body[:,2]

    def to_mark(self):
        return Shape.to_mark(self, [(i,j,t) for (i,j), t in zip(self.body.tolist(), self.txt.tolist())])

    def to_geom(self):
        return geom.MultiPoint(self.body)
    
class Layer(Shape):
    dtype = 'layer'
    def __init__(self, body=None, **key):
        Shape.__init__(self, body, **key)

    @property
    def box(self):
        if len(self.body)==0: return None
        boxs = np.array([i.box for i in self.body]).T
        return [boxs[0].min(), boxs[1].min(), boxs[2].max(), boxs[3].max()]

    def to_mark(self):
        return Shape.to_mark(self, [i.to_mark() for i in self.body])

    def to_geom(self):
        return geom.GeometryCollection([i.to_geom() for i in self.body])

class Layers(Shape):
    dtype = 'layers'
    def __init__(self, body=None, **key):
        Shape.__init__(self, body, **key)
        
    @property
    def box(self):
        if len(self.body)==0: return None
        boxs = np.array([i.box for i in self.body.values()]).T
        return [boxs[0].min(), boxs[1].min(), boxs[2].max(), boxs[3].max()]

    def to_mark(self):
        body = dict(zip(self.body.keys(), [i.to_mark() for i in self.body.values()]))
        return Shape.to_mark(self, body)

def mark2shp(mark):
    style = mark.copy()
    style.pop('body')
    keys = {'point':Point, 'points':Points, 'line':Line, 'lines':Lines,
            'polygon':Polygon, 'polygons':Polygons, 'circle':Circle,
            'circles':Circles, 'rectangle':Rectangle, 'rectangles':Rectangles,
            'ellipse':Ellipse, 'ellipses':Ellipses, 'text':Text, 'texts':Texts}
    if mark['type'] in keys: return keys[mark['type']](mark['body'], **style)
    if mark['type']=='layer':
        return Layer([mark2shp(i) for i in mark['body']], **style)
    if mark['type']=='layers':
        return Layers(dict(zip(mark['body'].keys(),
            [mark2shp(i) for i in mark['body'].values()])), **style)

def json2shp(obj):
    if obj['type']=='Point':
        return Point(obj['coordinates'])
    if obj['type']=='MultiPoint':
        return Points(obj['coordinates'])
    if obj['type']=='LineString':
        return Line(obj['coordinates'])
    if obj['type']=='MultiLineString':
        return Lines(obj['coordinates'])
    if obj['type']=='Polygon':
        return Polygon(obj['coordinates'])
    if obj['type']=='MultiPolygon':
        return Polygons(obj['coordinates'])
    if obj['type']=='GeometryCollection':
        return Layer([json2shp(i) for i in obj['geometries']])

def geom2shp(obj): return json2shp(geom.mapping(obj))

if __name__ == '__main__':
    import json

    layer = {'type': 'layer', 'body': [{'type': 'circle', 'body': (256, 256, 5)}, {'type': 'circle', 'body': (256, 256, 50)}, {'type': 'circle', 'body': (306.0, 256.0, 3)}]}
    layers = {'type':'layers', 'body':{1:{'type':'layer', 'body':[]}}}
    a = mark2shp(layers)
    print(a)
    #import geonumpy.io as gio
    #shp = gio.read_shp('C:/Users/54631/Documents/projects/huangqu/demo/shape/province.shp')
    #feas = json.loads(shp.to_json())['features']
