from .shape import *
from ..util import draw_shp
import numpy as np
import shapely.geometry as geom

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
