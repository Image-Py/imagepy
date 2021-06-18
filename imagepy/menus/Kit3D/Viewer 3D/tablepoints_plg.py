from sciapp.action import Table
from imagepy.app import ColorManager
from sciapp.util import meshutil
from sciapp.object import Mesh
import numpy as np

'''
class Plugin(Table):
	title = 'Table Point Cloud'

	para = {'name':'undefined', 'x':None, 'y':None, 'z':None, 'r':5, 'rs':None, 'c':(0,0,255),
		 'cs':None, 'cm':None, 'cube':False}

	view = [(str, 'name', 'name', ''),
			('field', 'x', 'x data', ''),
			('field', 'y', 'y data', ''),
			('field', 'z', 'z data', ''),
			(float, 'r', (0, 1024), 3, 'radius', 'pix'),
			('lab', 'lab', '== if set the radius would becom factor =='),
			('field', 'rs', 'radius', 'column'),
			('color', 'c', 'color', ''),
			('lab', 'lab', '== if set the color upon would disable =='),
			('field', 'cs', 'color', 'column'),
			('cmap', 'cm', 'color map when color column is set'),
			(bool, 'cube', 'draw outline cube')]


	def run(self, tps, snap, data, para = None):
		pts = np.array(data[[para['x'], para['y'], para['z']]])
		rs = data[para['rs']]*para['r'] if para['rs'] != 'None' else np.ones(len(pts))*para['r']
		cm = ColorManager.get(para['cm'])/255.0
		clip = lambda x : (x-x.min())/(x.max()-x.min())*255
		if para['cs'] == 'None': cs = tuple(np.array(para['c'])/255)
		else: cs = data[para['cs']]
		print(pts, rs, cs)
		vts, fs, cs = meshutil.create_balls(pts, rs, cs)
		mesh = Mesh(verts=vts, faces=fs, colors=cs, cmap=cm)
		self.app.show_mesh(mesh, para['name'])
		if para['cube']:
			p1 = data[[para['x'], para['y'], para['z']]].min(axis=0)
			p2 = data[[para['x'], para['y'], para['z']]].max(axis=0)
			vts, fs = meshutil.create_bound(p1, p2)
			self.app.show_mesh(Mesh(verts=vts, faces=fs, colors=(1,1,1), mode='grid'), 'box')
'''

class Plugin(Table):
	title = 'Table Point Cloud'

	para = {'name':'undefined', 'x':None, 'y':None, 'z':None, 'ref':None, 'c':(0,0,255), 'cm':None, 'cube':False}

	view = [(str, 'name', 'name', ''),
			('field', 'x', 'x data', ''),
			('field', 'y', 'y data', ''),
			('field', 'z', 'z data', ''),
			('field', 'ref', 'reflectivity', 'column'),
			('cmap', 'cm', 'color map for reflectivity'),
			('color', 'c', 'color', 'when no ref'),
			(bool, 'cube', 'draw outline cube')]


	def run(self, tps, snap, data, para = None):
		pts = np.array(data[[para['x'], para['y'], para['z']]])
		cm = ColorManager.get(para['cm'])/255.0
		clip = lambda x : (x-x.min())/(x.max()-x.min())*255
		if para['ref'] == 'None': cs = tuple(np.array(para['c'])/255)
		else: cs = data[para['ref']]
		mesh = Mesh(verts=pts, colors=cs, cmap=cm, mode='points')
		self.app.show_mesh(mesh, para['name'])
		if para['cube']:
			p1 = data[[para['x'], para['y'], para['z']]].min(axis=0)
			p2 = data[[para['x'], para['y'], para['z']]].max(axis=0)
			vts, fs = meshutil.create_bound(p1, p2)
			self.app.show_mesh(Mesh(verts=vts, faces=fs, colors=(1,1,1), mode='grid'), 'box')