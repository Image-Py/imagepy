import numpy as np
import moderngl
import numpy as np
from math import sin, cos, tan, pi

class Surface:
	def __init__(self, vts, ids, ns, cs=(0,0,1), **key):
		self.vts = vts
		self.ids = ids
		self.ns = ns
		self.cs = cs
		self.box = np.vstack(
			(vts.min(axis=0), 
			 vts.max(axis=0)))
		self.mode = 'mesh'
		self.alpha = 1
		self.visible = True
		self.width = 1
		self.update = False
		self.color = (0,0,0)
		self.set_style(**key)

	def set_style(self, **key):
		if 'mode' in key: self.mode = key['mode']
		if 'alpha' in key: self.alpha = key['alpha']
		if 'visible' in key: self.visible = key['visible']
		if 'color' in key:
			self.cs = key['color']
			self.update = True	

class MarkText(Surface):
	def __init__(self, vts, ids, os, h, color):
		self.vts = vts
		self.ids = ids
		self.cs = color
		self.os = os
		self.h = h
		self.box = None
		self.alpha = 1
		self.visible = True
		self.width = 1
		self.mode = 'grid'
		self.update = False
		self.color = (0,0,0)

class MeshSet:
	def __init__(self, name='meshset', objs=None):
		self.name = name
		self.objs = objs or {}

	@property
	def box(self):
		minb = [i.box[0] for i in self.objs.values() if not i.box is None]
		maxb = [i.box[1] for i in self.objs.values() if not i.box is None]
		minb, maxb = np.array(minb).min(axis=0), np.array(maxb).max(axis=0)
		return np.vstack((minb, maxb))

	@property
	def center(self): return self.box.mean(axis=0)

	@property
	def dial(self): return np.linalg.norm(self.box[1]-self.box[0])

	def add_surf(self, name, obj):
		self.objs[name] = obj

	def get_obj(self, key):
		if not key in self.objs: return None
		return self.objs[key]


