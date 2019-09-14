import sys, wx
from scipy.misc import imread
import scipy.ndimage as ndimg
sys.path.append('..')
import numpy as np
from glob import glob
import myvi

def dem():
	img = imread('data/dem.jpg')
	vts, fs, ns, cs = myvi.util.build_surf2d(img, ds=1, k=0.3, sigma=2)

	manager = myvi.Manager()
	manager.add_surf('dem', vts, fs, ns, cs)
	manager.show('DEM Demo')
	
def volume():
	fs = glob('data/vessel*.png')
	imgs = np.array([imread(i, True) for i in fs])
	print()
	imgs = ndimg.gaussian_filter(imgs, 1)
	vts, fs, ns, vs = myvi.util.build_surf3d(imgs, 1, 80)

	manager = myvi.Manager()
	manager.add_surf('vessel', vts, fs, ns, (1,0,0))
	manager.show('Vessel Demo')

def ball():
	vts, fs, ns, cs = myvi.build_ball((100,100,100),50, (1,0,0))
	manager = myvi.Manager()
	manager.add_surf('balls', vts, fs, ns, cs)
	manager.show('Ball Demo')

def random_balls():
	os = np.random.rand(30).reshape((-1,3))
	rs = np.random.rand(10)/5
	cs = (np.random.rand(10)*255).astype(np.uint8)
	cs = myvi.linear_color('jet')[cs]/255

	vts, fs, ns, cs = myvi.build_balls(os, rs, cs)
	manager = myvi.Manager()
	manager.add_surf('balls', vts, fs, ns, cs)
	manager.show('Random Balls Demo')

def line():
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

	vts, fs, ns, cs = myvi.build_line(x, y, z, (1, 0, 0))
	cs[:] = myvi.auto_lookup(vts[:,2], myvi.linear_color('jet'))/255

	manager = myvi.Manager()
	obj = manager.add_surf('line', vts, fs, ns, cs)
	obj.set_style(mode='grid')
	manager.show('Line Rings')

def mesh():
	dphi, dtheta = np.pi/80.0, np.pi/80.0  
	[phi,theta] = np.mgrid[0:np.pi+dphi*1.5:dphi,0:2*np.pi+dtheta*1.5:dtheta]  
	m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;  
	r = np.sin(m0*phi)**m1 + np.cos(m2*phi)**m3 + np.sin(m4*theta)**m5 + np.cos(m6*theta)**m7  
	x = r*np.sin(phi)*np.cos(theta)  
	y = r*np.cos(phi)  
	z = r*np.sin(phi)*np.sin(theta)  
	vts, fs, ns, cs = myvi.build_mesh(x, y, z)
	cs[:] = myvi.util.auto_lookup(vts[:,2], myvi.util.linear_color('jet'))/255

	manager = myvi.Manager()
	obj = manager.add_surf('mesh', vts, fs, ns, cs)
	obj.set_style(mode='grid')
	manager.show('Mesh Demo')

def ball_ring_box():
	os = np.random.rand(30).reshape((-1,3))
	rs = np.random.rand(10)/7
	cs = (np.random.rand(10)*255).astype(np.uint8)
	cs = myvi.linear_color('jet')[cs]/255

	vts_b, fs_b, ns_b, cs_b = myvi.build_balls(list(os), list(rs), list(cs))
	vts_l, fs_l, ns_l, cs_l = myvi.build_line(os[:,0], os[:,1], os[:,2], list(cs))
	vts_c, fs_c, ns_c, cs_c = myvi.build_cube((0,0,0), (1,1,1))
	manager = myvi.Manager()
	manager.add_surf('balls', vts_b, fs_b, ns_b, cs_b)
	line = manager.add_surf('line', vts_l, fs_l, ns_l, cs_l)
	line.set_style(mode='grid')
	box = manager.add_surf('box', vts_c, fs_c, ns_c, cs_c)
	box.set_style(mode='grid')
	manager.show('Balls Ring Demo')

def balls_with_mark():
	os = np.random.rand(30).reshape((-1,3))
	rs = np.random.rand(10)/7
	cs = (np.random.rand(10)*255).astype(np.uint8)
	cs = myvi.linear_color('jet')[cs]/255

	vts_b, fs_b, ns_b, cs_b = myvi.build_balls(os, rs, cs)
	cont = ['ID:%s'%i for i in range(10)]
	vtss, fss, pps, h, color = myvi.build_marks(cont, os, rs, 0.05, (1,1,1))
	manager = myvi.Manager()
	manager.add_surf('balls', vts_b, fs_b, ns_b, cs_b)
	line = manager.add_mark('line', vtss, fss, pps, h, color)
	line.set_style(mode='grid')
	manager.show('Balls Mark Demo')

def frame_demo():
	app = wx.App(False)
	frm = myvi.Frame3D(None, 'Frame')
	img = imread('data/dem.jpg')
	vts, fs, ns, cs = myvi.util.build_surf2d(img, ds=1, k=0.3, sigma=2)
	frm.viewer.add_surf_ansy('dem', vts, fs, ns, cs)
	frm.Show()
	app.MainLoop()

def surface2d():
	x, y = np.ogrid[-2:2:20j, -2:2:20j]  
	z = x * np.exp( - x**2 - y**2)
	vts, fs, ns, cs = myvi.util.build_surf2d(z, ds=1, k=20, sigma=2)
	cs[:] = myvi.util.auto_lookup(vts[:,2], myvi.util.linear_color('jet'))/255
	manager = myvi.Manager()
	manager.add_surf('dem', vts, fs, ns, cs)
	manager.show('DEM Demo') 

def arrow():
	v1, v2 = np.array([[[0,0,0],[5,5,5]],[[0,15,5],[2,8,3]]], dtype=np.float32)
	vts, fs, ns, c = myvi.util.build_arrows(v1, v2, 1, 1, 1, 1, (1,0,0))
	manager = myvi.Manager()
	manager.add_surf('dem', vts, fs, ns, c)
	manager.show('DEM Demo') 

def cube():
	vts, fs, ns, cs = myvi.build_cube((0,0,0), (1,1,1))
	manager = myvi.Manager()
	obj = manager.add_surf('cube', vts, fs, ns, cs)
	obj.set_style(mode='grid')
	manager.show('Cube Demo') 

def cube_surf():
	from skimage.data import camera
	lut = np.zeros((256,3), dtype=np.uint8)
	lut[:,0] = np.arange(256)
	imgs = np.array([camera()[:300,::]]*256)
	vts, fs, ns, cs = myvi.build_img_cube(imgs)
	manager = myvi.Manager()
	obj = manager.add_surf('cube', vts, fs, ns, cs)
	vts, fs, ns, cs = myvi.build_img_box(imgs)
	obj = manager.add_surf('box', vts, fs, ns, cs)
	obj.set_style(mode='grid')
	manager.show('Cube Demo') 


if __name__ == '__main__':

	cube_surf()
	'''
	volume()
	surface2d()
	dem()
	volume()
	ball()
	random_balls()
	line()
	mesh()
	ball_ring_box()
	balls_with_mark()
	arrow()
	'''