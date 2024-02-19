from time import time
import numpy as np
from math import pi

lib = {'0':([(0,0.5,0.5,0,0)],[(1,1,0,0,1)],0.5),
	'1':([(0.25,0.25)], [(0,1)], 0.5),
	'2':([(0,0.5,0.5,0,0,0.5)], [(1,1,0.5,0.5,0,0)], 0.5),
	'3':([(0,0.5,0.5,0),(0,0.5)],[(1,1,0,0),(0.5,0.5)], 0.5),
	'4':([(0,0,0.5),(0.5,0.5)],[(1,0.5,0.5),(1,0)],0.5),
	'5':([(0.5,0,0,0.5,0.5,0)], [(1,1,0.5,0.5,0,0)], 0.5),
	'6':([(0.5,0,0,0.5,0.5,0,0)], [(1,1,0.5,0.5,0,0,0.5)], 0.5),
	'7':([(0,0.5,0.5)], [(1,1,0)], 0.5),
	'8':([(0.5,0.5,0,0,0.5,0.5,0,0)], [(0.5,1,1,0.5,0.5,0,0,0.5)], 0.5),
	'9':([(0.5,0.5,0,0,0.5,0.5,0)], [(0.5,1,1,0.5,0.5,0,0)], 0.5),
	'I':([(0,0.5),(0.25,0.25),(0,0.5)],[(1,1),(1,0),(0,0)],0.5),
	'D':([(0,0.25,0.4,0.5,0.5,0.4,0.25,0),(0.1,0.1)],[(1,1,0.9,0.75,0.25,0.1,0,0),(0,1)],0.5),
	':':([(0.2,0.3),(0.2,0.3)],[(0.75,0.75),(0.25,0.25)],0.5)}

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

def build_twringidx(n, offset=0):
	idx = np.array([[0,1,n+1],[n+1,n+2,1]])
	idx = idx[np.arange(n*2)%2].T + np.arange(n*2)//2
	return (idx.T+offset).astype(np.uint32)

def build_pringidx(p, n, offset=0):
	ridx = np.array([[0,0,1]]*n, dtype=np.uint32)
	ridx += np.arange(n, dtype=np.uint32).reshape((-1,1))+offset
	ridx[:,0] = p
	return ridx

def build_grididx(r, c):
	idx = np.arange(r*c, dtype=np.uint32)
	rs, cs = idx//c, idx%c
	idx1 = idx[(rs<r-1)*(cs<c-1)].reshape((-1,1))
	did = np.array([[0, 1, 1+c, 0, 1+c, c]], dtype=np.uint32)
	return rs, cs, (idx1 + did).reshape((-1,3))

def build_surf2d(img, ds=1, sigma=0, k=0.2):
	from skimage.filters import sobel_h, sobel_v
	from scipy.ndimage import gaussian_filter
	#start = time()
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

def build_arrow(v1, v2, rs, re, ts, te, c):
	v = (v2-v1)/np.linalg.norm(v2-v1)
	ss, ee = v1 + v*rs*ts, v2 - v*re*te
	vx = np.cross(v, np.random.rand(3))
	vx /= np.linalg.norm(vx)
	vy = np.cross(vx, v)
	angs = np.linspace(0, np.pi*2, 17)
	vas = np.array([np.cos(angs), np.sin(angs)])
	vxy = np.dot(vas.T, np.array([vx, vy]))
	vts = np.vstack((v1, ss + rs * vxy, ee + re * vxy, v2))
	fs1 = build_pringidx(0, 16, 1)
	fs = build_twringidx(16, 1)
	fs2 = build_pringidx(35, 16, 18)
	face = np.vstack((fs1, fs, fs2))
	ns = np.vstack((-v, vxy, vxy, v)).astype(np.float32)
	cs = (np.ones((len(vts), 3))*c).astype(np.float32)
	return vts.astype(np.float32), face, ns, cs

def build_arrows(v1s, v2s, rss, res, tss, tes, cs):
	if not isinstance(cs, list): cs = [cs] * len(v1s)
	if not isinstance(tss, list): tss = [tss] * len(v1s)
	if not isinstance(tes, list): tes = [tes] * len(v1s)
	if not isinstance(rss, list): rss = [rss] * len(v1s)
	if not isinstance(res, list): res = [res] * len(v1s)
	vtss, fss, nss, css = [], [], [], []
	s = 0
	for v1, v2, rs, re, ts, te, c in zip(v1s, v2s, rss, res, tss, tes, cs):
		if np.linalg.norm(v1-v2) < 0.1: continue
		vv, ff, nn, cc = build_arrow(v1, v2, rs, re, ts, te, c)
		fss.append(ff+s)
		s += len(vv)
		vtss.append(vv)
		nss.append(nn)
		css.append(cc)
	print(np.vstack(vtss).shape, np.vstack(fss).shape, np.vstack(nss).shape, np.vstack(css).shape)
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

def build_cube(p1, p2, color=(1,1,1)):
	(x1,y1,z1),(x2,y2,z2) = p1, p2
	xs = (x1,x2,x2,x1,x1,x1,x1,x1,x1,x2,x2,x1,x2,x2,x2,x2)
	ys = (y1,y1,y1,y1,y1,y2,y2,y1,y2,y2,y2,y2,y2,y1,y1,y2)
	zs = (z1,z1,z2,z2,z1,z1,z2,z2,z2,z2,z1,z1,z1,z1,z2,z2)
	return build_line(xs, ys, zs, color)

def build_img_cube(imgs, ds=1):
	imgs = imgs[::ds,::ds,::ds]
	(h, r, c), total = imgs.shape[:3], 0
	print(h, r, c)
	vtss, fss, nss, css = [], [], [], []
	shp = [(h,r,c,h*r), (h,c,r,h*c), (r,c,h,r*c)]
	nn = [[(0,0,-1),(0,0,1)], [(0,1,0),(0,-1,0)], [(1,0,0),(-1,0,0)]]
	for i in (0,1,2):
		rs, cs, fs12 = build_grididx(*shp[i][:2])
		idx1, idx2 = [rs*ds, cs*ds], [rs*ds, cs*ds]
		rcs1, rcs2 = [rs, cs], [rs, cs]
		rcs1.insert(2-i, 0); rcs2.insert(2-i, -1)
		vs1, vs2 = imgs[tuple(rcs1)]/255, imgs[tuple(rcs2)]/255
		idx1.insert(2-i, rs*0); idx2.insert(2-i, cs*0+shp[i][2]*ds-1)
		vtss.append(np.array(idx1, dtype=np.float32).T)
		vtss.append(np.array(idx2, dtype=np.float32).T)
		css.append((np.ones((1, 3))*vs1.reshape((len(vs1),-1))).astype(np.float32))
		css.append((np.ones((1, 3))*vs2.reshape((len(vs1),-1))).astype(np.float32))
		nss.append((np.ones((shp[i][3],1))*[nn[i][0]]).astype(np.float32))
		nss.append((np.ones((shp[i][3],1))*[nn[i][1]]).astype(np.float32))
		fss.extend([fs12+total, fs12+(total+shp[i][0]*shp[i][1])])
		total += shp[i][3] * 2
	return np.vstack(vtss), np.vstack(fss), np.vstack(nss), np.vstack(css)
	
def build_img_box(imgs, color=(1,1,1)):
	return build_cube((-1,-1,-1), imgs.shape[:3], color)

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