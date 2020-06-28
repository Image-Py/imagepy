from sciapp.action import Free
from sciapp.object import Surface, MarkText
from sciapp.util import surfutil
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
		vts, fs, ns, cs = surfutil.build_mesh(x, y, z)
		cs[:] = surfutil.auto_lookup(vts[:,2], surfutil.linear_color('jet'))/255
		self.app.show_mesh(Surface(vts, fs, ns, cs), 'decoration')

class Lines(Free):
	title = 'Lines Demo'

	def run(self, para=None):
		vts = np.array([(0,0,0),(1,1,0),(2,1,0),(1,0,0)], dtype=np.float32)
		fs = np.array([(0,1,2),(1,2,3)], dtype=np.uint32)
		ns = np.ones((4,3), dtype=np.float32)

		n_mer, n_long = 6, 11
		pi = np.pi
		dphi = pi / 1000.0
		phi = np.arange(0.0, 2 * pi + 0.5 * dphi, dphi)
		mu = phi * n_mer
		x = np.cos(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
		y = np.sin(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
		z = np.sin(n_long * mu / n_mer) * 0.5

		vts, fs, ns, cs = surfutil.build_line(x, y, z, (1, 0, 0))
		cs[:] = surfutil.auto_lookup(vts[:,2], surfutil.linear_color('jet'))/255
		self.app.show_mesh(Surface(vts, fs, ns, cs, mode='grid'), 'line')

class Balls(Free):
	title = 'Random Balls Demo'

	def run(self, para=None):
		os = np.random.rand(30).reshape((-1,3))
		rs = np.random.rand(10)/5
		cs = (np.random.rand(10)*255).astype(np.uint8)
		cs = surfutil.linear_color('jet')[cs]/255

		vts, fs, ns, cs = surfutil.build_balls(os, rs, cs)
		self.app.show_mesh(Surface(vts, fs, ns, cs), 'balls')

plgs = [Lines, Balls, Decoration]