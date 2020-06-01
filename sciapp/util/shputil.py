import numpy as np
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
        geoms.extend(list(obj))
    else: geoms.append(obj)
    if root: return geom.GeometryCollection(geoms)

def geom_union(obj):
    return geom_flatten(unary_union(geom_flatten(obj)))