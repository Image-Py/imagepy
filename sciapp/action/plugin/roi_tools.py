from .shp_tools import *
from .shpbase import BaseEditor
from ..tolact import ImageTool
from ...object import ROI

class BaseROI(ImageTool):
	def __init__(self, base): 
		base.__init__(self)
		self.base = base

	def mouse_down(self, img, x, y, btn, **key):
		if img.roi is None: img.roi = ROI()
		else: img.roi.msk = None
		self.base.mouse_down(self, img.roi, x, y, btn, **key)

	def mouse_up(self, img, x, y, btn, **key):
		self.base.mouse_up(self, img.roi, x, y, btn, **key)
		if not img.roi is None:
			if len(img.roi.body)==0: img.roi = None
			else: img.roi.msk = None

	def mouse_move(self, img, x, y, btn, **key):
		self.base.mouse_move(self, img.roi, x, y, btn, **key)

	def mouse_wheel(self, img, x, y, d, **key):
		self.base.mouse_wheel(self, img.roi, x, y, d, **key)

class PolygonROI(BaseROI):
	title = 'Polygon ROI'
	def __init__(self): 
		BaseROI.__init__(self, PolygonEditor)

class LineROI(BaseROI):
	title = 'Line ROI'
	def __init__(self): 
		BaseROI.__init__(self, LineEditor)

class PointROI(BaseROI):
	title = 'Point ROI'
	def __init__(self): 
		BaseROI.__init__(self, PointEditor)

class RectangleROI(BaseROI):
	title = 'Rectangle ROI'
	def __init__(self): 
		BaseROI.__init__(self, RectangleEditor)

class EllipseROI(BaseROI):
	title = 'Ellipse ROI'
	def __init__(self): 
		BaseROI.__init__(self, EllipseEditor)

class FreeLineROI(BaseROI):
	title = 'Free Line ROI'
	def __init__(self): 
		BaseROI.__init__(self, FreeLineEditor)

class FreePolygonROI(BaseROI):
	title = 'Free Polygon ROI'
	def __init__(self): 
		BaseROI.__init__(self, FreePolygonEditor)