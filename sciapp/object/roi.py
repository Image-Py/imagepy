from .shape import *
import numpy as np
from skimage import draw
import shapely.geometry as geom

def circle(r):
	xs, ys = np.mgrid[-r:r+1, -r:r+1]
	rcs = np.where((xs**2 + ys**2)<r+0.5)
	return np.array(rcs)-r

def thick(rr, cc, r, shp):
	rs, cs = circle(r)
	rr, cc = rr[:,None] + rs, cc[:,None] + cs
	msk = (rr>=0) & (rr<shp[0]) & (cc>=0) & (cc<shp[1])
	return rr[msk], cc[msk]

def draw_line(r1, c1, r2, c2, shp, lw=0):
	rr, cc = draw.line(r1, c1, r2, c2)
	return thick(rr, cc, lw, shp)

def draw_lines(rs, cs, shp, lw):
	rr, cc = [], []
	for r1, c1, r2, c2 in zip(rs[:-1], cs[:-1], rs[1:], cs[1:]):
		r, c = draw.line(r1, c1, r2, c2)
		rr.append(r); cc.append(c)
	rr, cc = np.hstack(rr), np.hstack(cc)
	return thick(rr, cc, lw, shp)

def path(rs, cs, shp, lw):
	rr, cc = draw.polygon_perimeter(rs, cs, shp, True)
	return thick(rr, cc, lw, shp)

def draw_shp(shp, img=None, color=1, lw=1):
	if isinstance(img, tuple):
		img = np.zeros(img, dtype=np.int8)
	if type(shp) in {geom.Point, geom.MultiPoint}:
		arr = np.array(shp).reshape((-1,2)).T
		cc, rr = np.round(arr).astype(np.int32)
		rr, cc = thick(rr, cc, lw, img.shape)
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

class ROI(Layer):
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

if __name__ == '__main__':
	pts = Points([(10,10),(15,20)])
	line = Line([(10,10),(15,20),(20,20)])
	lines = Lines([[(10,10),(15,20),(20,20)]])
	polygon = Polygon([[(1,1),(1,20),(20,20),(20,1)],[(5,5),(5,10),(10,10),(10,5)]])

	im = draw_shp(pts.to_geom(), (30,30), lw=0)
	plt.imshow(im)
	plt.show()
