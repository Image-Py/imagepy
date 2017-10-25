from time import time
import numpy as np
from math import pi
from .txtmark import lib

def count_ns(vts, fs):
	dv1 = vts[fs[:,1]] - vts[fs[:,2]]
	dv2 = vts[fs[:,1]] - vts[fs[:,0]]
	ns = np.cross(dv1, dv2)
	ass = np.linalg.norm(ns, axis=1)
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

def build_surf2d(img, ds=1, sigma=0, k=0.2):
	from skimage.filters import sobel_h, sobel_v
	from scipy.ndimage import gaussian_filter
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
	from skimage.measure import marching_cubes_lewiner
	vts, fs, ns, cs =  marching_cubes_lewiner(imgs[::ds,::ds,::ds], level, step_size=step)
	vts *= ds
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

def build_mesh(xs, ys, zs, c=(1,0,0)):
	rs, cs, fs = build_grididx(xs.shape[0], xs.shape[1])
	vts = np.array([xs[rs, cs], ys[rs, cs], zs[rs,cs]]).astype(np.float32).T
	ns = count_ns(vts, fs)
	cs = (np.ones((len(vts), 3))*c).astype(np.float32)
	return vts, fs, ns, cs

def build_balls(os, rs, cs=(1,0,0)):
	if isinstance(cs, tuple):
		cs = [cs] * len(os)
	vtss, fss, nss, css = [], [], [], []
	for o,r,c in zip(os, rs, cs):
		vv, ff, nn, cc = build_ball(o, r, c)
		fss.append(ff+len(vtss)*len(vv))
		vtss.append(vv)
		nss.append(nn)
		css.append(cc)
	return np.vstack(vtss), np.vstack(fss), np.vstack(nss), np.vstack(css)

# 0 1 1  2 2 3  3 4 4  5 5 6
def build_line(xs, ys, zs, c):
	vts = np.array([xs, ys, zs], dtype=np.float32).T
	n = (len(xs)-1)*2
	rem = (6 - n % 6)%6
	fs = np.arange(0.1,(n+rem)//2,0.5).round().astype(np.uint32)
	if rem>0: fs[-rem:] = len(xs)-1 
	ns = np.ones((len(vts), 3), dtype=np.float32)
	cs = (np.ones((len(vts), 3))*c).astype(np.float32)
	return vts, fs.reshape((-1,3)), ns, cs

def build_lines(xs, ys, zs, cs):
	if not isinstance(cs, list):
		cs = [cs] * len(xs)
	vtss, fss, nss, css = [], [], [], []
	s = 0
	for x, y, z, c in zip(xs, ys, zs, cs):
		vv, ff, nn, cc = build_line(x, y, z, c)
		fss.append(ff+s)
		s += len(vv)
		vtss.append(vv)
		nss.append(nn)
		css.append(cc)
	return np.vstack(vtss), np.vstack(fss), np.vstack(nss), np.vstack(css)

def build_mark(cont, pos, dz, h, color):
	vts, fss = [], []
	s, sw = 0, 0
	for i in cont:
		xs, ys, w = lib[i]
		vv, ff, nn, cc = build_lines(xs, ys, ys, (0,0,0))
		fss.append(ff+s)
		vts.append(vv+[sw,0,0])
		vts[-1][:,2] = dz
		s += len(vv)
		sw += w+0.3
	sw -= 0.3
	vts = (np.vstack(vts)-[sw/2.0, 0.5, 0])
	return vts, np.vstack(fss), pos, h, color

def build_marks(conts, poss, dz, h, color):
	if not hasattr(dz, '__len__'):
		dz = [dz] * len(conts)
	vtss, fss, pps = [], [], []
	s = 0
	for cont, pos, z in zip(conts, poss, dz):
		vv, ff, pp, hh, cc = build_mark(cont, pos, z, h, color)
		fss.append(ff+s)
		s += len(vv)
		vtss.append(vv)
		pps.append((np.ones((len(vv),3))*pp).astype(np.float32))

	return np.vstack(vtss), np.vstack(fss), np.vstack(pps), h, color

cmp = {'rainbow':[(127, 0, 255), (43, 126, 246), (42, 220, 220), (128, 254, 179), (212, 220, 127), (255, 126, 65), (255, 0, 0)],
	'jet':[(0, 0, 127), (0, 40, 255), (0, 212, 255), (124, 255, 121), (255, 229, 0), (255, 70, 0), (127, 0, 0)],
	'ocean':[(0, 127, 0), (0, 64, 42), (0, 0, 85), (0, 64, 128), (0, 127, 170), (129, 192, 213), (255, 255, 255)],
	'earth':[(0, 0, 0), (27, 77, 122), (54, 135, 111), (93, 160, 75), (169, 179, 91), (206, 171, 132), (253, 250, 250)]}

def linear_color(cs):
	if isinstance(cs, str): cs=cmp[cs]
	cmap = np.zeros((256, 3), dtype=np.uint8)
	idx = np.linspace(0, 256, len(cs)).astype(np.uint16)
	for i in range(1, len(cs)):
		c1, c2 = cs[i-1], cs[i]
		rs, gs, bs = [np.linspace(c1[j], c2[j], idx[i]-idx[i-1]) for j in (0,1,2)]
		cmap[idx[i-1]:idx[i]] = np.array((rs, gs, bs)).T
	return cmap

def auto_lookup(vs, cmap):
	vs = vs - vs.min()
	vs = vs/vs.max()
	vs = (vs*255).astype(np.uint8)
	return cmap[vs]

if __name__ == '__main__':
	from matplotlib import cm
	cmap = linear_color('earth')
	import matplotlib.pyplot as plt
	img = np.zeros((30,256), dtype=np.uint8)
	img[:] = np.arange(256)
	img = cmap[img]
	plt.imshow(img)
	plt.show()