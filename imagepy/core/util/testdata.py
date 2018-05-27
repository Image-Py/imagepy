from imagepy import IPy
from imagepy.core.engine import Free
from imagepy.core.manager import ReaderManager, WriterManager, ViewerManager
from skimage.io import imread
import os.path as osp, os
import numpy as np

class TestData(Free):
	def __init__(self, path, name):
		self.name = name
		self.path = path
		self.title = name.split('.')[0].replace('\\', '/').split('/')[-1]

	def run(self, para = None):
		root_dir = osp.abspath(osp.dirname(self.path))
		print(root_dir)
		path = osp.join(root_dir, self.name)
		if osp.isfile(path):
			fp, fn = osp.split(path)
			fn, fe = osp.splitext(fn)
			read = ReaderManager.get(fe[1:])
			view = ViewerManager.get(fe[1:])

			group, read = (True, read[0]) if isinstance(read, tuple) else (False, read)
			img = read(path)
			if img.dtype==np.uint8 and img.ndim==3 and img.shape[2]==4:
			    img = img[:,:,:3].copy()
			if not group: img = [img]
		else:
			names = [i for i in os.listdir(path) if '.' in i]
			read = ReaderManager.get(names[0].split('.')[1])
			view = ViewerManager.get(names[0].split('.')[1])
			imgs = []
			for i in range(len(names)):
				self.progress(i, len(names))
				imgs.append(read(osp.join(path,names[i])))
			img = imgs
		view(img, self.title)

	def __call__(self):
		return self