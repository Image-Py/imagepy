from .shpbase import *
from ...util import geom_flatten

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
			shp.body.append(Point([x,y]))
			shp.dirty = True

class LineEditor(BaseEditor):
	title = 'Line Tool'
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
			self.obj.body = np.vstack((self.obj.body, [(x,y)]))
			self.obj.dirty, shp.dirty, self.obj = True, True, None
			del key['canvas'].marks['buffer']
		shp.dirty = True

class PolygonEditor(BaseEditor):
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

class RectangleEditor(BaseEditor):
	title = 'Rectangle Tool'
	def __init__(self): 
		BaseEditor.__init__(self)
		self.obj, self.p = None, None

	def mouse_down(self, shp, x, y, btn, **key):
		if inbase(key, btn):
			BaseEditor.mouse_down(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if btn==1:
			self.obj = Rectangle([x, y, 0, 0])
			self.p = x, y
			shp.body.append(self.obj)

	def mouse_up(self, shp, x, y, btn, **key): 
		if inbase(key, btn):
			BaseEditor.mouse_up(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if self.p == (x, y) and not self.obj is None:
			self.obj = self.p = None
			return shp.body.pop(-1)
		if (key['alt'] or key['shift']) and not self.obj is None:
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
		if 'buffer' in key['canvas'].marks:
			del key['canvas'].marks['buffer']

	def mouse_move(self, shp, x, y, btn, **key): 
		BaseEditor.mouse_move(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if not self.obj is None:
			self.obj.body[2:] = (x, y) - self.obj.body[:2]
			anchor = Points(mark(self.obj)[0], color=(255,0,0))
			key['canvas'].marks['buffer'] = anchor
			self.obj.dirty = shp.dirty = True

class EllipseEditor(BaseEditor):
	title = 'Ellipse Tool'
	def __init__(self): 
		BaseEditor.__init__(self)
		self.obj, self.p = None, None

	def mouse_down(self, shp, x, y, btn, **key):
		if inbase(key, btn):
			BaseEditor.mouse_down(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if btn==1:
			self.p = (x, y)
			self.obj = Ellipse([x, y, 0, 0, 0])
			shp.body.append(self.obj)

	def mouse_up(self, shp, x, y, btn, **key): 
		if inbase(key, btn):
			BaseEditor.mouse_up(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if self.p == (x, y) and not self.obj is None:
			self.obj = self.p = None
			return shp.body.pop(-1)
		if (key['alt'] or key['shift']) and not self.obj is None:
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
		if 'buffer' in key['canvas'].marks:
			del key['canvas'].marks['buffer']

	def mouse_move(self, shp, x, y, btn, **key): 
		BaseEditor.mouse_move(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if not self.obj is None:
			ox, oy = self.p
			self.obj.body[:] = [(x+ox)/2, (y+oy)/2, (x-ox)/2, (y-oy)/2, 0]
			anchor = Points(mark(self.obj)[0], color=(255,0,0))
			key['canvas'].marks['buffer'] = anchor
			shp.dirty = self.obj.dirty = True

class FreeLineEditor(BaseEditor):
	title = 'Free Line Tool'
	def __init__(self): 
		BaseEditor.__init__(self)
		self.cur, self.n, self.obj = 0, 0, None

	def mouse_down(self, shp, x, y, btn, **key):
		if inbase(key, btn):
			BaseEditor.mouse_down(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if btn==1 and self.obj is None: 
			self.obj = Line([(x,y)])
			shp.body.append(self.obj)
			shp.dirty = True

	def mouse_up(self, shp, x, y, btn, **key): 
		if inbase(key, btn):
			BaseEditor.mouse_up(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		self.obj = None

	def mouse_move(self, shp, x, y, btn, **key): 
		BaseEditor.mouse_move(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if not self.obj is None:
			self.obj.body = np.vstack((self.obj.body, [(x,y)]))
			self.obj.dirty = shp.dirty = True

class FreePolygonEditor(BaseEditor):
	title = 'Free Polygon Tool'
	def __init__(self): 
		BaseEditor.__init__(self)
		self.cur, self.n, self.obj = 0, 0, None

	def mouse_down(self, shp, x, y, btn, **key):
		if inbase(key, btn):
			BaseEditor.mouse_down(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if btn==1 and self.obj is None: 
			self.obj = Line([(x,y)])
			shp.body.append(self.obj)
			shp.dirty = True

	def mouse_up(self, shp, x, y, btn, **key): 
		if inbase(key, btn):
			BaseEditor.mouse_up(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if btn==1 and not self.obj is None:
			body = np.vstack((self.obj.body, self.obj.body[0]))
			shp.body[-1] = Polygon(body)
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

	def mouse_move(self, shp, x, y, btn, **key): 
		BaseEditor.mouse_move(self, shp, x, y, btn, **key)
		if key['alt'] and key['ctrl']: return
		if not self.obj is None:
			self.obj.body = np.vstack((self.obj.body, [(x,y)]))
			self.obj.dirty = shp.dirty = True