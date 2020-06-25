from .shape import *
import numpy as np
from numpy.linalg import norm
import shapely.geometry as geom

class ROI(Layer):
	default = {'color':(255,255,0), 'fcolor':(255,255,255), 
    'fill':False, 'lw':1, 'tcolor':(255,0,0), 'size':8}

	def __init__(self, body=None, **key):
		if isinstance(body, Layer):  body = body.body
		if not body is None and not isinstance(body, list):
			body = [body]
		Layer.__init__(self, body, **key)
		self.fill = False
		self.msk = None

	@property
	def roitype(self):
		roitype = ''
		for i in self.body:
			if roitype == '': roitype = i.dtype
			if roitype != i.dtype: return 'multi'
		return roitype

	def to_mask(self, msk, mode):
		from ..util import draw_shp
		if isinstance(msk, tuple):
			msk = np.zeros(msk, dtype=np.int8)
		else: msk[:] = 0
		msk.dtype = np.int8
		if mode=='in':
			draw_shp(self.to_geom(), msk, 1, 0)
			np.clip(msk, 0, 1, out=msk)
		if mode=='out':
			draw_shp(self.to_geom(), msk, 1, 0)
			np.clip(msk, 0, 1, out=msk)
			msk -= 1
		if isinstance(mode, int):
			draw_shp(self.to_geom(), msk, 1, mode)
			np.clip(msk, 0, 1, out=msk)
		msk.dtype, self.msk = np.bool, mode
		return msk

class Measure(Layer): 
	default = {'color':(255,255,0), 'fcolor':(255,255,255), 
	'fill':False, 'lw':1, 'tcolor':(255,0,0), 'size':8}

	def measure(self, shp):
		txt = []
		if shp.dtype == 'layer':
			for i in shp.body:
				txt.extend(self.measure(i))
		if not hasattr(shp, 'mtype'): return txt
		if shp.mtype=='coordinate':
			txt.append(tuple(shp.body)+('%.2f,%.2f'%tuple(shp.body),))
		if shp.mtype=='distance':
			for s,e in zip(shp.body[:-1], shp.body[1:]):
				p = ((s[0]+e[0])/2, (s[1]+e[1])/2)
				l = ((s[0]-e[0])**2+(s[1]-e[1])**2)**0.5
				txt.append(p+('%.2f'%l,))
		if shp.mtype=='angle':
			pts = np.array(shp.body)
			v1 = pts[:-2]-pts[1:-1]
			v2 = pts[2:]-pts[1:-1]
			a = np.sum(v1*v2, axis=1)*1.0
			a/=norm(v1,axis=1)*norm(v2,axis=1)
			ang = np.arccos(a)/np.pi*180
			for v, p in zip(ang, shp.body[1:-1]):
				txt.append(tuple(p[:2])+('%.2f'%v,))
		if shp.mtype=='slope':
			pts = np.array(shp.body)
			mid = (pts[:-1]+pts[1:])/2

			dxy = (pts[:-1]-pts[1:])
			dxy[:,1][dxy[:,1]==0] = 1
			l = norm(dxy, axis=1)*-np.sign(dxy[:,1])
			ang = np.arccos(dxy[:,0]/l)/np.pi*180
			for v, p in zip(ang, mid):
				txt.append(tuple(p[:2])+('%.2f'%v,))
		if shp.mtype=='area':
			geom = shp.to_geom()
			o = geom.centroid
			txt.append((o.x, o.y)+('%.2f'%geom.area,))
		return txt

	def measure_mark(self):
		txt = self.measure(self)
		if len(txt)>0:
			rms = [i for i in self.body if isinstance(i, Texts)]
			for i in rms: self.body.remove(i)
			self.body.append(Texts(txt))

class Coordinate(Point): mtype = 'coordinate'

class Distance(Line): mtype = 'distance'

class Area(Polygon): mtype = 'area'

class Angle(Line): mtype = 'angle'

class Slope(Line): mtype = 'slope'

if __name__ == '__main__':
	pts = Points([(10,10),(15,20)])
	line = Line([(10,10),(15,20),(20,20)])
	lines = Lines([[(10,10),(15,20),(20,20)]])
	polygon = Polygon([[(1,1),(1,20),(20,20),(20,1)],[(5,5),(5,10),(10,10),(10,5)]])

	im = draw_shp(pts.to_geom(), (30,30), lw=0)
	plt.imshow(im)
	plt.show()
