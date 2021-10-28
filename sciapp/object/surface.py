import numpy as np
import scipy.ndimage as ndimg

class Scene:
	def __init__(self, **key):
		self.name = key.get('name', 'scene')
		self.objects = {}
		self._light_dir = (10, 5, -5)
		self._light_color = (0.7, 0.7, 0.7, 0.7)
		self._bg_color = (0.3, 0.3, 0.3, 1.0)
		self._ambient_color = (0.3, 0.3, 0.3, 1.0)
		self.set_style(**key)
		self.dirty = True

	@property
	def title(self): return self.name

	@property
	def surface(self): return self.name

	def apply(self):
		for i in self.objects.values():
			i.light_dir = self.light_dir
			i.light_color = self.light_color
			i.ambient_color = self.ambient_color

	def set_style(self, bg_color=None, light_dir=None, light_color=None, ambient_color=None, **key):
		self._bg_color = bg_color or self._bg_color
		self._light_dir = light_dir or self._light_dir
		self._light_color = light_color or self._light_color
		self._ambient_color = ambient_color or self._ambient_color
		self.dirty = True; self.apply()


	@property
	def bg_color(self): return self._bg_color

	@bg_color.setter
	def bg_color(self, value): 
		return self.set_style(bg_color=value)

	@property
	def light_dir(self): return self._light_dir

	@light_dir.setter
	def light_dir(self, value): 
		return self.set_style(light_dir=value)

	@property
	def light_color(self): return self._light_color

	@light_color.setter
	def light_color(self, value): 
		return self.set_style(light_color=value)

	@property
	def ambient_color(self): return self._ambient_color

	@ambient_color.setter
	def ambient_color(self, value): 
		return self.set_style(ambient_color=value)

	def add_obj(self, name, obj):
		self.objects[name] = obj

	def get_obj(self, name):
		return self.objects[name]

	@property
	def names(self):
		return list(self.objects.keys())

class Mesh:
	def __init__(self, verts=None, faces=None, colors=None, cmap=None, **key):
		if faces is None and not verts is None: 
			faces = np.arange(len(verts), dtype=np.uint32)
		self.verts = verts.astype(np.float32, copy=False) if not verts is None else None
		self.faces = faces.astype(np.uint32, copy=False) if not faces is None else None
		self.colors = colors
		self.mode, self.visible, self.dirty = 'mesh', True, 'geom'
		self.alpha = 1; self.edges = None; self.shiness = 60
		self.high_light = False; self.cmap = 'gray' if cmap is None else cmap
		self.set_data(**key)

	def set_data(self, verts=None, faces=None, colors=None, **key):
		if faces is None and not verts is None: 
			faces = np.arange(len(verts), dtype=np.uint32)
		if not verts is None: self.verts = verts.astype(np.float32, copy=False)
		if not faces is None: self.faces = faces.astype(np.uint32, copy=False)
		if not colors is None: self.colors = colors
		if not faces is None: self.edge = None
		if sum([i is None for i in [verts, faces]])<2: self.dirty = 'geom'
		if not self.faces is None and self.faces.ndim==1: key['mode'] = 'points'
		elif not self.faces is None and self.faces.shape[1]==2: 
			if key.get('mode', self.mode)=='mesh': key['mode'] = 'grid'
		if key.get('mode', self.mode) != self.mode: self.dirty = 'geom'
		self.mode = key.get('mode', self.mode)
		self.visible = key.get('visible', self.visible)
		self.alpha = key.get('alpha', self.alpha)
		self.high_light = key.get('high_light', False)
		self.shiness = key.get('shiness', self.shiness)
		self.cmap = key.get('cmap', self.cmap)
		self.dirty = self.dirty or True

	def get_edges(self):
		if self.faces.ndim==1 or self.faces.shape[1]==2: return self.faces
		if not self.edges is None: return self.edges
		edges = np.vstack([self.faces[:,i] for i in ([0,1],[0,2],[1,2])])
		edges = np.sort(edges, axis=-1).ravel().view(dtype=np.uint64)
		self.edges = np.unique(edges).view(dtype=np.uint32).reshape(-1,2)
		return self.edges

	def update(self, state=True): self.dirty = state

class TextSet:
	def __init__(self, texts=None, verts=None, colors=(1,1,1), size=12, **key):
		self.texts, self.verts, self.size, self.colors = texts, verts, size, colors
		self.visible, self.dirty = True, 'geom'
		self.alpha = 1; self.edges = None
		self.high_light = False; self.shiness = 0
		self.set_data(**key)

	def set_data(self, texts=None, verts=None, colors=None, size=None, **key):
		if not texts is None: self.texts = texts
		if not verts is None: self.verts = verts
		if not colors is None: self.colors = colors
		if not size is None: self.size = size
		if sum([i is None for i in [texts, verts, colors, size]])<4: self.dirty = 'geom'
		self.visible = key.get('visible', self.visible)
		self.alpha = key.get('alpha', self.alpha)
		self.high_light = key.get('high_light', False)
		self.shiness = key.get('shiness', self.shiness)
		self.dirty = self.dirty or True

class Surface2d(Mesh):
	def __init__(self, img=None, sample=1, sigma=0, k=0.3, **key):
		self.img, self.sample, self.sigma, self.k = img, sample, sigma, k
		Mesh.__init__(self, **key)
		self.set_data(img, sample, sigma, k)

	def set_data(self, img=None, sample=None, sigma=None, k=None, **key):
		if not img is None: self.img = img
		if not sample is None: self.sample = sample
		if not sigma is None: self.sigma = sigma
		if not k is None: self.k = k
		if sum([not i is None for i in (img, sample, sigma, k)])>0:
			from ..util import meshutil
			vert, fs = meshutil.create_surface2d(self.img, self.sample, self.sigma, self.k)
			Mesh.set_data(self, verts=vert, faces=fs.astype(np.uint32), colors=vert[:,2], **key)
		else: Mesh.set_data(self, **key)

class Surface3d(Mesh):
	def __init__(self, imgs=None, level=0, sample=1, sigma=0, step=1, **key):
		self.imgs, self.sample, self.sigma, self.step = imgs, sample, sigma, step
		self.level, self.step = level, step
		Mesh.__init__(self, **key)
		self.set_data(imgs, level, sample, sigma, step)

	def set_data(self, imgs=None, level=None, sample=None, sigma=None, step=None, **key):
		if not imgs is None: self.imgs = imgs
		if not level is None: self.level = level
		if not sample is None: self.sample = sample
		if not sigma is None: self.sigma = sigma
		if not step is None: self.step = step
		if sum([not i is None for i in (imgs, level, sample, sigma, step)])>0:
			from ..util import meshutil
			vert, fs = meshutil.create_surface3d(self.imgs, self.level, self.sample, self.sigma, self.step)
			Mesh.set_data(self, verts=vert, faces=fs.astype(np.uint32), **key)
		else: Mesh.set_data(self, **key)

class Volume3d:
	def __init__(self, imgs=None, level=0.25, sample=1, step=1, cmap=None, **key):
		self.imgs, self.level, self.sample, self.step = imgs, level, sample, step
		self.visible, self.dirty = True, 'geom'
		self.cmap = 'gray' if cmap is None else cmap
		self.alpha = 1; self.shiness = 0
		self.high_light = False;
		self.set_data(**key)

	def set_data(self, imgs=None, level=None, step=None, **key):
		if not imgs is None: self.imgs = imgs
		if not level is None: self.level = level
		if not step is None: self.step = step
		if sum([not i is None for i in (imgs, level, step)])>0:
			self.dirty = 'geom'
		self.visible = key.get('visible', self.visible)
		self.alpha = key.get('alpha', self.alpha)
		self.high_light = key.get('high_light', False)
		self.shiness = key.get('shiness', self.shiness)
		self.cmap = key.get('cmap', self.cmap)
		self.dirty = self.dirty or True
