from skimage.measure import marching_cubes_lewiner
from skimage.filters import sobel_h, sobel_v
from scipy.ndimage import gaussian_filter
from time import time
import numpy as np
from math import pi

def count_ns(vts, fs):
	dv1 = vts[fs[:,1]] - vts[fs[:,2]]
	dv2 = vts[fs[:,1]] - vts[fs[:,0]]
	ns = np.cross(dv1, dv2)
	
	ass = np.linalg.norm(ns, axis=1)
	print(vts[[3,4,21]])

	ns /= np.linalg.norm(ns, axis=1).reshape((-1,1))
	
	buf = np.zeros_like(vts)
	for i in (0,1,2): np.add.at(buf, fs[:,i], ns)
	buf /= np.linalg.norm(buf, axis=1).reshape((-1,1))
	return buf

def build_grididx(r, c):
	idx = np.arange(r*c, dtype=np.uint32)
	rs, cs = idx//c, idx%c
	idx1 = idx[(rs<r-1)*(cs<c-1)].reshape((-1,1))
	did = np.array([[0, 1, 1+c, 0, 1+c, c]], dtype=np.uint32)
	return rs, cs, (idx1 + did).reshape((-1,3))

def build_surf2d(img, ds=1, sigma=0, k=0.2, lut=None):
	start = time()
	img = img[::-ds, ::ds]
	img = gaussian_filter(img, sigma)
	r, c = img.shape
	rs, cs, fs = build_grididx(r, c)
	vs = img[rs, cs]

	vts = np.array([cs*ds, rs*ds, vs*k], dtype=np.float32).T
	cs = (np.ones((3, r*c))*(vs/255)).astype(np.float32).T
	
	dx, dy = sobel_h(img), sobel_v(img)
	cx, cy = np.zeros((r*c, 3)), np.zeros((r*c, 3))
	cx[:,0], cx[:,2] = 1, dx.ravel()
	cy[:,1], cy[:,2] = 1, dy.ravel()
	ns = np.cross(cx, cy)
	ns = (ns.T/np.linalg.norm(ns, axis=1)).astype(np.float32).T
	
	#ns = count_ns(vts, fs)
	print(time()-start)
	return vts, fs, ns, cs

def build_surf3d(imgs, ds, level, step=1, c=(1,0,0)):
	vts, fs, ns, cs =  marching_cubes_lewiner(imgs[::ds,::ds,::ds], level, step_size=step)
	vts[:,:2] *= ds
	cs = (np.ones((len(vts), 3))*c).astype(np.float32)
	return vts, fs, ns, cs

def build_ball(o, r, c=(1,0,0)):
	ay, ax = np.mgrid[-pi/2:pi/2:9j, 0:pi*2:17j]
	zs = np.sin(ay.ravel())
	xs = np.cos(ax.ravel()) * np.cos(ay.ravel())
	ys = np.sin(ax.ravel()) * np.cos(ay.ravel())
	ns = np.vstack((xs, ys, zs)).astype(np.float32).T
	vts = (ns * r + o).astype(np.float32)
	fs = build_grididx(9, 17)[2]
	cs = (np.ones((len(vts), 3))*c).astype(np.float32)
	#print(ns2)
	return vts, fs, ns, cs

def build_balls(os, rs, cs=(1,0,0)):
	if not isinstance(cs, list):
		cs = [cs] * len(os)
	vtss, fss, nss, css = [], [], [], []
	for o,r,c in zip(os, rs, cs):
		vv, ff, nn, cc = build_ball(o, r, c)
		fss.append(ff+len(vtss)*len(vv))
		vtss.append(vv)
		nss.append(nn)
		css.append(cc)
	return np.vstack(vtss), np.vstack(fss), \
		np.vstack(nss), np.vstack(css)