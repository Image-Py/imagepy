import numpy as np
from skimage import draw
from ..object.shape import *

def offset(shp, dx, dy):
	if shp.dtype in {'rectangle', 'ellipse', 'circle'}:
		shp.body[:2] += dx, dy
	elif shp.dtype in {'rectangles', 'ellipses', 'circles'}:
		shp.body[:,:2] += dx, dy
	elif isinstance(shp, np.ndarray):
		shp += dx, dy
	elif isinstance(shp.body, list):
		for i in shp.body: offset(i, dx, dy)

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

def geom_flatten(obj, geoms=None):
    geoms, root = ([], True) if geoms is None else (geoms, False)
    if isinstance(obj, geom.GeometryCollection):
        for i in obj: geom_flatten(i, geoms)
    elif type(obj) in {geom.MultiPolygon, geom.MultiPoint, geom.MultiLineString}: 
        geoms.extend(list(obj.geoms))
    else: geoms.append(obj)
    if root: return geom.GeometryCollection(geoms)

def geom_union(obj):
    return geom_flatten(unary_union(geom_flatten(obj)))


def draw_circle(r):
    xs, ys = np.mgrid[-r:r+1, -r:r+1]
    rcs = np.where((xs**2 + ys**2)<r+0.5)
    return np.array(rcs)-r

def draw_thick(rr, cc, r, shp):
    rs, cs = draw_circle(r)
    rr, cc = rr[:,None] + rs, cc[:,None] + cs
    msk = (rr>=0) & (rr<shp[0]) & (cc>=0) & (cc<shp[1])
    return rr[msk], cc[msk]

def draw_line(r1, c1, r2, c2, shp, lw=0):
    rr, cc = draw.line(r1, c1, r2, c2)
    return draw_thick(rr, cc, lw, shp)

def draw_lines(rs, cs, shp, lw):
    rr, cc = [], []
    for r1, c1, r2, c2 in zip(rs[:-1], cs[:-1], rs[1:], cs[1:]):
        r, c = draw.line(r1, c1, r2, c2)
        rr.append(r); cc.append(c)
    rr, cc = np.hstack(rr), np.hstack(cc)
    return draw_thick(rr, cc, lw, shp)

def draw_path(rs, cs, shp, lw):
    rr, cc = draw.polygon_perimeter(rs, cs, shp, True)
    return draw_thick(rr, cc, lw, shp)

def draw_shp(shp, img=None, color=1, lw=1):
    if isinstance(img, tuple):
        img = np.zeros(img, dtype=np.int8)
    if type(shp) in {geom.Point, geom.MultiPoint}:
        arr = np.array(shp).reshape((-1,2)).T
        cc, rr = np.round(arr).astype(np.int32)
        rr, cc = draw_thick(rr, cc, lw, img.shape)
        img[rr, cc] += color
    if type(shp) is geom.LineString:
        cc, rr = np.round(np.array(shp).T).astype(np.int32)
        rr, cc = draw_lines(rr, cc, img.shape, lw)
        img[rr, cc] += color
    if type(shp) is geom.LinearRing:
        cc, rr = np.round(np.array(shp).T).astype(np.int32)
        if lw>0: rr, cc = draw_lines(rr, cc, img.shape, lw)
        else: rr, cc = draw.polygon(rr, cc, img.shape)
        img[rr, cc] += color
    if type(shp) is geom.MultiLineString:
        for i in shp: draw_shp(i, img, color, lw)
    if type(shp) is geom.Polygon and lw>0:
        draw_shp(shp.exterior, img, color, lw)
        for i in shp.interiors: draw_shp(i, img, color, lw)
    if type(shp) is geom.Polygon and lw==0:
        draw_shp(shp.exterior, img, color, lw)
        for i in shp.interiors: draw_shp(i, img, -color, lw)
    if type(shp) is geom.MultiPolygon:
        for i in shp: draw_shp(i, img, color, lw)
    if type(shp) is geom.GeometryCollection:
        for i in shp: draw_shp(i, img, color, lw)
    return img