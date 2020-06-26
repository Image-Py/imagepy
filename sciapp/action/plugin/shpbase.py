from ..tolact import ShapeTool
from sciapp.object import *
from sciapp.util import geom_union
from numpy.linalg import norm
import numpy as np

def mark(shp, types = 'all'):
	pts = []
	if not (types=='all' or shp.dtype in types): return pts
	if shp.dtype == 'point':
		pts.append([shp.body])
	if shp.dtype == 'points':
		pts.append(shp.body)
	if shp.dtype == 'line':
		pts.append(shp.body)
	if shp.dtype == 'lines':
		pts.extend(shp.body)
	if shp.dtype == 'polygon' and len(shp.body)==1:
		pts.append(shp.body[0])
	if shp.dtype == 'polygons':
		for i in shp.body:
			if len(i) != 1: continue
			pts.append(i[0])
	if shp.dtype == 'rectangle':
		l,t,w,h = shp.body
		ps = np.mgrid[l:l+w:3j, t:t+h:3j].T.reshape((-1,2))
		pts.append(ps)
	if shp.dtype == 'rectangles':
		for i in range(len(shp.body)):
			l,t,w,h = shp.body[i]
			ps = np.mgrid[l:l+w:3j, t:t+h:3j].T.reshape((-1,2))
			pts.append(ps)
	if shp.dtype == 'ellipse':
			x0, y0, l1, l2, ang = shp.body
			mat = np.array([[np.cos(-ang),-np.sin(-ang)],
						  [np.sin(-ang),np.cos(-ang)]])
			ps = np.mgrid[-l1:l1:3j, -l2:l2:3j].T.reshape((-1,2))
			pts.append(mat.dot(ps.T).T + (x0, y0))
	if shp.dtype == 'ellipses':
		for i in range(len(shp.body)):
			x0, y0, l1, l2, ang = shp.body[i]
			mat = np.array([[np.cos(-ang),-np.sin(-ang)],
						  [np.sin(-ang),np.cos(-ang)]])
			ps = np.mgrid[-l1:l1:3j, -l2:l2:3j].T.reshape((-1,2))
			pts.append(mat.dot(ps.T).T + (x0, y0))
	if shp.dtype == 'layer':
		minl, obj = 1e8, None
		for i in shp.body:
			pts.extend(mark(i, types))
	return pts

def pick_obj(shp, x, y, lim, types='all'):
	obj, minl = None, lim
	if not (types=='all' or shp.dtype in types): 
		return m, obj, minl
	if shp.dtype == 'layer':
		for i in shp.body:
			o, l = pick_obj(i, x, y, lim, types)
			if l < minl: 
				obj, minl = o, l
	elif shp.dtype in 'polygons':
		b = shp.to_geom().contains(Point([x, y]).to_geom())
		if b : return shp, 0
	else:
		d = shp.to_geom().distance(Point([x, y]).to_geom())
		if d<minl: obj, minl = shp, d
	return obj, minl

def pick_point(shp, x, y, lim, types='all'):
	m, obj, minl = None, None, lim
	if not (types=='all' or shp.dtype in types): 
		return m, obj, minl
	if shp.dtype == 'point':
		l = ((shp.body-(x, y))**2).sum()
		if l < minl: 
			m, obj, minl = shp, shp.body, l
	if shp.dtype == 'points':
		l = norm(shp.body-(x,y), axis=1)
		n = np.argmin(l)
		l = l[n]
		if l < minl: 
			m, obj, minl = shp, shp.body[n], l
	if shp.dtype == 'line':
		l = norm(shp.body-(x,y), axis=1)
		n = np.argmin(l)
		l = l[n]
		if l < minl: 
			m, obj, minl = shp, shp.body[n], l
	if shp.dtype == 'lines':
		for line in shp.body:
			l = norm(line-(x,y), axis=1)
			n = np.argmin(l)
			l = l[n]
			if l < minl: 
				m, obj, minl = shp, line[n], l
	if shp.dtype == 'polygon' and len(shp.body)==1:
		l = norm(shp.body[0]-(x,y), axis=1)
		n = np.argmin(l)
		l = l[n]
		if l < minl: 
			m, obj, minl = shp, shp.body[0][n], l
	if shp.dtype == 'polygons':
		for i in shp.body:
			if len(i) != 1: continue
			l = norm(i[0]-(x,y), axis=1)
			n = np.argmin(l)
			l = l[n]
			if l < minl: 
				m, obj, minl = shp, i[0][n], l
	if shp.dtype == 'rectangle':
		l,t,w,h = shp.body
		pts = np.mgrid[l:l+w:3j, t:t+h:3j].T.reshape((-1,2))
		names = ['lt','t','rt','l','o','r','lb','b','rb']
		l = norm(pts-(x,y), axis=1)
		n = np.argmin(l)
		if l[n] < minl:
			m, obj, minl = shp, names[n], l[n]
	if shp.dtype == 'rectangles':
		for i in range(len(shp.body)):
			l,t,w,h = shp.body[i]
			pts = np.mgrid[l:l+w:3j, t:t+h:3j].T.reshape((-1,2))
			names = ['lt','t','rt','l','o','r','lb','b','rb']
			l = norm(pts-(x,y), axis=1)
			n = np.argmin(l)
			if l[n] < minl:
				m, obj, minl = shp, (names[n], i), l[n]
	if shp.dtype == 'ellipse':
			x0, y0, l1, l2, ang = shp.body
			mat = np.array([[np.cos(-ang),-np.sin(-ang)],
						  [np.sin(-ang),np.cos(-ang)]])
			pts = np.mgrid[-l1:l1:3j, -l2:l2:3j].T.reshape((-1,2))
			pts = mat.dot(pts.T).T + (x0, y0)
			names = ['lt','t','rt','l','o','r','lb','b','rb']
			l = norm(pts-(x,y), axis=1)
			n = np.argmin(l)
			if l[n] < minl:
				m, obj, minl = shp, names[n], l[n]
	if shp.dtype == 'ellipses':
		for i in range(len(shp.body)):
			x0, y0, l1, l2, ang = shp.body[i]
			mat = np.array([[np.cos(-ang),-np.sin(-ang)],
						  [np.sin(-ang),np.cos(-ang)]])
			pts = np.mgrid[-l1:l1:3j, -l2:l2:3j].T.reshape((-1,2))
			pts = mat.dot(pts.T).T + (x0, y0)
			names = ['lt','t','rt','l','o','r','lb','b','rb']
			l = norm(pts-(x,y), axis=1)
			n = np.argmin(l)
			if l[n] < minl:
				m, obj, minl = shp, (names[n], i), l[n]
	if shp.dtype == 'layer':
		# minl, obj = 1e8, None
		for i in shp.body:
			h, o, l = pick_point(i, x, y, lim, types)
			if l < minl: 
				m, obj, minl = h, o, l
	return m, obj, minl

def drag(shp, pt, x, y, types='all'):
	if not (types=='all' or shp.dtype in types): return
	if shp.dtype == 'rectangle':
		body = shp.body
		if pt == 'o':body[:2] = (x, y) - body[2:]/2
		if 'l' in pt:body[[0,2]] = x, body[0]+body[2]-x
		if 'r' in pt:body[2] = x - body[0]
		if 't' in pt:body[[1,3]] = y, body[1]+body[3]-y
		if 'b' in pt:body[3] = y - body[1]
	elif shp.dtype == 'rectangles':
		pt, i = pt
		body = shp.body[i]
		if pt == 'o':body[:2] = (x, y) - body[2:]/2
		if 'l' in pt:body[[0,2]] = x, body[0]+body[2]-x
		if 'r' in pt:body[2] = x - body[0]
		if 't' in pt:body[[1,3]] = y, body[1]+body[3]-y
		if 'b' in pt:body[3] = y - body[1]
	elif shp.dtype == 'ellipse':
		if pt == 'o': 
			shp.body[:2] = x, y
			return
		x0, y0, l1, l2, ang = shp.body
		v1, v2 = (np.array([[np.cos(-ang),-np.sin(-ang)],
			[np.sin(-ang),np.cos(-ang)]]) * (l1, l2)).T
		l, r, t, b = np.array([-v1, v1, -v2, v2]) + (x0, y0)
		if 'l' in pt: l = v1.dot([x-x0, y-y0])*v1/l1**2+(x0, y0)
		if 'r' in pt: r = v1.dot([x-x0, y-y0])*v1/l1**2+(x0, y0)
		if 't' in pt: t = v2.dot([x-x0, y-y0])*v2/l2**2+(x0, y0)
		if 'b' in pt: b = v2.dot([x-x0, y-y0])*v2/l2**2+(x0, y0)
		k = np.linalg.inv(np.array([-v2,v1]).T).dot((l+r-t-b)/2)
		shp.body[:2] = (l+r)/2 + v2*k[0]
		shp.body[2:4] = np.dot(r-l, v1)/l1/2, np.dot(b-t, v2)/l2/2
	elif shp.dtype == 'ellipses':
		pt, i = pt
		body = shp.body[i]
		if pt == 'o': 
			body[:2] = x, y
			return
		x0, y0, l1, l2, ang = body
		v1, v2 = (np.array([[np.cos(-ang),-np.sin(-ang)],
			[np.sin(-ang),np.cos(-ang)]]) * (l1, l2)).T
		l, r, t, b = np.array([-v1, v1, -v2, v2]) + (x0, y0)
		if 'l' in pt: l = v1.dot([x-x0, y-y0])*v1/l1**2+(x0, y0)
		if 'r' in pt: r = v1.dot([x-x0, y-y0])*v1/l1**2+(x0, y0)
		if 't' in pt: t = v2.dot([x-x0, y-y0])*v2/l2**2+(x0, y0)
		if 'b' in pt: b = v2.dot([x-x0, y-y0])*v2/l2**2+(x0, y0)
		k = np.linalg.inv(np.array([-v2,v1]).T).dot((l+r-t-b)/2)
		body[:2] = (l+r)/2 + v2*k[0]
		body[2:4] = np.dot(r-l, v1)/l1/2, np.dot(b-t, v2)/l2/2
	else: pt[:] = x, y

def offset(shp, dx, dy):
	if shp.dtype in {'rectangle', 'ellipse', 'circle'}:
		shp.body[:2] += dx, dy
	elif shp.dtype in {'rectangles', 'ellipses', 'circles'}:
		shp.body[:,:2] += dx, dy
	elif isinstance(shp, np.ndarray):
		shp += dx, dy
	elif isinstance(shp.body, list):
		for i in shp.body: offset(i, dx, dy)

class BaseEditor(ShapeTool):
	def __init__(self, dtype='all'):
		self.status, self.oldxy, self.p = '', None, None
		self.pick_m, self.pick_obj = None, None

	def mouse_down(self, shp, x, y, btn, **key):
		self.p = x, y
		if btn==2:
			self.status = 'move'
			self.oldxy = key['px'], key['py']
		if btn==1 and self.status=='pick':
			m, obj, l = pick_point(shp, x, y, 5)
			self.pick_m, self.pick_obj = m, obj
		if btn==1 and self.pick_m is None:
			m, l = pick_obj(shp, x, y, 5)
			self.pick_m, self.pick_obj = m, None
		if btn==3:
			obj, l = pick_obj(shp, x, y, 5)
			if key['alt'] and not key['ctrl']:
				if obj is None: del shp.body[:]
				else: shp.body.remove(obj)
				shp.dirty = True
			if key['shift'] and not key['alt'] and not key['ctrl']:
				layer = geom2shp(geom_union(shp.to_geom()))
				shp.body = layer.body
				shp.dirty = True
			if not (key['shift'] or key['alt'] or key['ctrl']):
				key['canvas'].fit()

	def mouse_up(self, shp, x, y, btn, **key):
		self.status = ''
		if btn==1:
			self.pick_m = self.pick_obj = None
			if not (key['alt'] and key['ctrl']): return
			pts = mark(shp)
			if len(pts)>0: 
				pts = Points(np.vstack(pts), color=(255,0,0))
				key['canvas'].marks['anchor'] = pts
			shp.dirty = True

	def mouse_move(self, shp, x, y, btn, **key):
		self.cursor = 'arrow'
		if self.status == 'move':
			ox, oy = self.oldxy
			up = (1,-1)[key['canvas'].up]
			key['canvas'].move(key['px']-ox, (key['py']-oy)*up)
			self.oldxy = key['px'], key['py']
		if key['alt'] and key['ctrl']:
			self.status = 'pick'
			if not 'anchor' in key['canvas'].marks: 
				pts = mark(shp)
				if len(pts)>0: 
					pts = Points(np.vstack(pts), color=(255,0,0))
					key['canvas'].marks['anchor'] = pts
			if 'anchor' in key['canvas'].marks:
				m, obj, l = pick_point(key['canvas'].marks['anchor'], x, y, 5)
				if not m is None: self.cursor = 'hand'
		elif 'anchor' in key['canvas'].marks: 
			self.status = ''
			del key['canvas'].marks['anchor']
			shp.dirty = True
		if not self.pick_obj is None and not self.pick_m is None:
			drag(self.pick_m, self.pick_obj, x, y)
			pts = mark(self.pick_m)
			if len(pts)>0:
				pts = np.vstack(pts)
				key['canvas'].marks['anchor'] = Points(pts, color=(255,0,0))
			self.pick_m.dirty = True
			shp.dirty = True
		if self.pick_obj is None and not self.pick_m is None:
			offset(self.pick_m, x-self.p[0], y-self.p[1])
			pts = mark(self.pick_m)
			if len(pts)>0:
				pts = np.vstack(pts)
				key['canvas'].marks['anchor'] = Points(pts, color=(255,0,0))
			self.p = x, y
			self.pick_m.dirty =shp.dirty = True

	def mouse_wheel(self, shp, x, y, d, **key):
		if d>0: key['canvas'].zoomout(x, y, coord='data')
		if d<0: key['canvas'].zoomin(x, y, coord='data')