from imagepy.core.engine import Table
from imagepy.core.manager import ColorManager
from imagepy.core import myvi
import numpy as np
from imagepy import IPy

class Plugin(Table):
	title = 'Table Point Cloud'

	para = {'x':None, 'y':None, 'z':None, 'r':5, 'rs':None, 'c':(0,0,255),
		 'cs':None, 'cm':None, 'cube':False}

	view = [('field', 'x', 'x data', ''),
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

	def load(self, para):
		self.frame = myvi.Frame3D.figure(IPy.curapp, title='3D Canvas')
		return True

	def run(self, tps, snap, data, para = None):
		pts = np.array(data[[para['x'], para['y'], para['z']]])
		rs = data[para['rs']]*para['r'] if para['rs'] != 'None' else [para['r']]*len(pts)
		cm = ColorManager.get_lut(para['cm'])/255.0
		clip = lambda x : (x-x.min())/(x.max()-x.min())*255
		if para['cs'] == 'None': cs = [np.array(para['c'])/255.0]*len(pts)
		else: cs = cm[clip(data[para['cs']]).astype(np.uint8)]
		vts, fs, ns, cs = myvi.build_balls(pts.astype(np.float32), list(rs), cs)
		self.frame.viewer.add_surf_asyn('ball', vts, fs, ns, cs)
		if para['cube']:
			p1 = data[[para['x'], para['y'], para['z']]].min(axis=0)
			p2 = data[[para['x'], para['y'], para['z']]].max(axis=0)
			vts, fs, ns, cs = myvi.build_cube(p1, p2)
			self.frame.viewer.add_surf_asyn('cube', vts, fs, ns, cs, mode='grid')
		self.frame.Raise()
		self.frame = None