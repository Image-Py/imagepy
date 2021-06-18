from sciapp.action import Free
from sciapp.object import Mesh
from sciapp.util import  meshutil
import numpy as np

class Decoration(Free):
	title = 'Decoration Demo'

	def run(self, para=None):
		dphi, dtheta = np.pi/20.0, np.pi/20.0  
		[phi,theta] = np.mgrid[0:np.pi+dphi*1.5:dphi,0:2*np.pi+dtheta*1.5:dtheta]  
		m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;  
		r = np.sin(m0*phi)**m1 + np.cos(m2*phi)**m3 + np.sin(m4*theta)**m5 + np.cos(m6*theta)**m7  
		x = r*np.sin(phi)*np.cos(theta)  
		y = r*np.cos(phi)  
		z = r*np.sin(phi)*np.sin(theta)
		vts, fs = meshutil.create_grid_mesh(x, y, z)
		mesh = Mesh(vts, fs.astype(np.uint32), vts[:,2], mode='grid', cmap='jet')
		self.app.show_mesh(mesh, 'decoration')

class Lines(Free):
	title = 'Lines Demo'

	def run(self, para=None):
		n_mer, n_long = 6, 11
		pi = np.pi
		dphi = pi / 1000.0
		phi = np.arange(0.0, 2 * pi + 0.5 * dphi, dphi)
		mu = phi * n_mer
		x = np.cos(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
		y = np.sin(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
		z = np.sin(n_long * mu / n_mer) * 0.5

		vts = np.array([x, y, z]).T.astype(np.float32)
		fs = np.arange(len(vts), dtype=np.uint32)
		fs = np.array([fs[:-1], fs[1:]]).T
		mesh = Mesh(vts, fs, vts[:,2], cmap='jet', mode='grid')
		self.app.show_mesh(mesh, 'line')

class Balls(Free):
	title = 'Random Balls Demo'

	def run(self, para=None):
		os = np.random.rand(30).reshape((-1,3))
		rs = np.random.rand(10)/7+0.05
		cs = np.random.rand(10)
		vts_b, fs_b, cs_b = meshutil.create_balls(os, rs, cs)
		mesh = Mesh(verts=vts_b, faces=fs_b, colors=cs_b, cmap='jet')
		self.app.show_mesh(mesh, 'balls')

plgs = [Lines, Balls, Decoration]