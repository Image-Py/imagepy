import struct
import numpy as np
import moderngl
from time import time

from skimage.io import imread
import numpy as np
from math import sin, cos, tan, pi
import scipy.ndimage as nimg

def look_at(eye, target, up, dtype=None):
    forward = (target - eye)/np.linalg.norm(target - eye)
    side = (np.cross(forward, up))/np.linalg.norm(np.cross(forward, up))
    up = (np.cross(side, forward)/np.linalg.norm(np.cross(side, forward)))

    return np.array((
            (side[0], up[0], -forward[0], 0.),
            (side[1], up[1], -forward[1], 0.),
            (side[2], up[2], -forward[2], 0.),
            (-np.dot(side, eye), -np.dot(up, eye), np.dot(forward, eye), 1.0)
        ), dtype=np.float32)

def perspective(xmax, ymax, near, far):
	left, right = -xmax, xmax
	bottom, top = -ymax, ymax

	A = (right + left) / (right - left)
	B = (top + bottom) / (top - bottom)
	C = -(far + near) / (far - near)
	D = -2. * far * near / (far - near)
	E = 2. * near / (right - left)
	F = 2. * near / (top - bottom)
	return np.array((
		(  E, 0., 0., 0.),
		( 0.,  F, 0., 0.),
		(  A,  B,  C,-1.),
		( 0., 0.,  D, 0.),
	), dtype=np.float32)

def orthogonal(xmax, ymax, near, far):
    rml = xmax * 2
    tmb = ymax * 2
    fmn = far - near

    A = 2. / rml
    B = 2. / tmb
    C = -2. / fmn
    Tx = 0
    Ty = 0
    Tz = -(far + near) / fmn

    return np.array((
        ( A, 0., 0., 0.),
        (0.,  B, 0., 0.),
        (0., 0.,  C, 0.),
        (Tx, Ty, Tz, 1.),
    ), dtype=np.float32)

class Surface:
	def __init__(self, vts, ids, ns, cs=(0,0,1)):
		self.vts, self.ids, self.ns, self.cs = vts, ids, ns, cs
		self.box = np.vstack((vts.min(axis=0), vts.max(axis=0)))
		self.mode, self.blend, self.visible = 'mesh', 1.0, True
		self.color = cs if isinstance(cs, tuple) else (0,0,0)
		self.width = 1

	def on_ctx(self, ctx, prog):
		self.ctx = ctx
		vts, ids, ns, cs = self.vts, self.ids, self.ns, self.cs;
		buf = self.buf = np.zeros((len(vts), 9), dtype=np.float32)
		buf[:,0:3], buf[:,3:6], buf[:,6:9] = vts, ns, cs
		self.vbo = ctx.buffer(buf.tobytes())
		ibo = ctx.buffer(ids.tobytes())
		
		content = [(self.vbo, '3f 3f 3f', 'v_vert', 'v_norm', 'v_color')]
		self.vao = ctx.vertex_array(prog, content, ibo)
		self.prog = prog

	def set_style(self, mode=None, blend=None, color=None, visible=None):
		if not mode is None: self.mode = mode
		if not blend is None: self.blend=blend
		if not visible is None: self.visible=visible
		if not color is None:
			self.buf[:,6:9] = color
			self.vbo.write(self.buf.tobytes())
			self.color = color if isinstance(color, tuple) else (0,0,0)

	def draw(self, mvp, light, bright, scatter):
		if not self.visible: return
		self.ctx.line_width = self.width
		mvp = np.dot(*mvp)
		self.prog['Mvp'].write(mvp.astype(np.float32).tobytes())
		self.prog['blend'].value = self.blend
		self.prog['scatter'].value = scatter
		self.prog['light'].value = tuple(light)
		self.prog['bright'].value = bright
		self.vao.render({'mesh':moderngl.TRIANGLES, 'grid':moderngl.LINES}[self.mode])

class MarkText:
	def __init__(self, vts, ids, os, h, color):
		self.vts, self.ids, self.color, self.os, self.h = vts, ids, color, os, h
		self.blend, self.box, self.visible, self.mode = 1, None, True, 'grid'

	def on_ctx(self, ctx, prog):
		self.ctx = ctx
		vts, ids, os = self.vts, self.ids, self.os
		buf = self.buf = np.zeros((len(vts), 6), dtype=np.float32)
		buf[:,0:3], buf[:,3:6] = vts, os
		self.vbo = ctx.buffer(buf.tobytes())
		ibo = ctx.buffer(ids.tobytes())
		content = [(self.vbo, '3f 3f', 'v_vert', 'v_pos')]
		self.vao = ctx.vertex_array(prog, content, ibo)
		self.prog = prog

	def set_style(self, mode=None, blend=None, color=None, visible=None):
		if not visible is None: self.visible = visible
		if not color is None: self.color = color

	def draw(self, mvp, light, bright, scatter):
		if not self.visible: return
		self.ctx.line_width = 2
		self.prog['mv'].write(mvp[0].astype(np.float32).tobytes())
		self.prog['proj'].write(mvp[1].astype(np.float32).tobytes())
		self.prog['f_color'].write(np.array(self.color).astype(np.float32).tobytes())
		self.prog['h'].value = self.h
		self.vao.render(moderngl.LINES)

class Manager:
	def __init__(self):
		self.h, self.v, self.r = 1.5, 0, 300
		self.ratio, self.dial = 1.0, 1.0
		self.pers, self.center = True, (0,0,0)
		self.background = 0.4, 0.4, 0.4
		self.light = (1,0,0)
		self.bright, self.scatter = 0.66, 0.66
		self.objs = {}
		self.ctx = None

	def on_ctx(self):
		self.ctx = moderngl.create_context()
		self.prog_suf = self.ctx.program(
			vertex_shader='''
                #version 330
                uniform mat4 Mvp;
                in vec3 v_vert;
                in vec3 v_norm;
                in vec3 v_color;
                out vec3 f_norm;
                out vec3 f_color;
                void main() {
                    gl_Position = Mvp * vec4(v_vert, 1);
                    f_norm = v_norm;
                    f_color = v_color;
                }
            ''',
            fragment_shader='''
                #version 330
                uniform vec3 light;
                uniform float blend;
                uniform float scatter;
                uniform float bright;
                in vec3 f_norm;
                in vec3 f_color;
                out vec4 color;
                void main() {
                    float d = clamp(dot(light, f_norm)*bright+scatter, 0, 1);
           			color = vec4(f_color*d, blend);
                }
			'''
		)

		self.prog_txt = self.ctx.program(
			vertex_shader='''
                #version 330
                uniform mat4 mv;
                uniform mat4 proj;
                uniform float h;
                in vec3 v_vert;
                in vec3 v_pos;
                void main() {
                    vec4 o = mv * vec4(v_pos, 1);
                    gl_Position = proj *(o + vec4(v_vert.x*h, v_vert.y*h, v_vert.z, 0));
                }
            ''',
            fragment_shader='''
                #version 330
                uniform vec3 f_color;
                out vec4 color;
                void main() {
           			color = vec4(f_color, 1);
                }
			''')

		for i in self.objs.values():
			if isinstance(i, Surface): i.on_ctx(self.ctx, self.prog_suf)
			if isinstance(i, MarkText): i.on_ctx(self.ctx, self.prog_txt)

	def add_surf(self, name, vts, ids, ns=None, cs=(0,0,1), real=True):
		surf = Surface(vts, ids, ns, cs)
		if not real: surf.box = None
		if not self.ctx is None:
			surf.on_ctx(self.ctx, self.prog_suf)
		self.objs[name] = surf
		self.count_box()
		return surf

	def add_mark(self, name, vts, ids, o, h, cs=(0,0,1)):
		mark = MarkText(vts, ids, o, h, cs)
		if not self.ctx is None:
			mark.on_ctx(self.ctx, self.prog_txt)
		self.objs[name] = mark
		return mark


	def get_obj(self, key):
		if not key in self.objs: return None
		return self.objs[key]

	def draw(self):
		self.ctx.clear(*self.background)
		self.ctx.enable(moderngl.DEPTH_TEST)
		#self.ctx.enable(ModernGL.CULL_FACE)
		self.ctx.enable(moderngl.BLEND)
		for i in self.objs.values():
                    i.draw(self.mvp, self.light, self.bright, self.scatter)

	def count_box(self):
		minb = np.array([i.box[0] for i in self.objs.values() if not i.box is None]).min(axis=0)
		maxb = np.array([i.box[1] for i in self.objs.values() if not i.box is None]).max(axis=0)
		self.box = np.vstack((minb, maxb))
		#print(self.box)
		self.center = self.box.mean(axis=0)
		self.dial = np.linalg.norm(self.box[1]-self.box[0])

	def count_mvp(self):
		#print('mvp')
		ymax = (1.0 if self.pers else self.l) * np.tan(self.fovy * np.pi / 360.0)
		xmax = ymax * self.ratio
		proj = (perspective if self.pers else orthogonal)(xmax, ymax, 1.0, 100000)
		lookat = look_at(self.eye, self.center, (0.0,0.0,1.0))
		self.mvp = (lookat, proj)
		
	def set_viewport(self, x, y, width, height):
		self.ctx.viewport = (x, y, width, height)
		self.ratio = width*1.0/height

	def set_background(self, rgb): self.background = rgb

	def set_light(self, light): self.light = light

	def set_bright_scatter(self, bright=None, scatter=None):
		if not bright is None: self.bright = bright
		if not scatter is None: self.scatter = scatter

	def reset(self, fovy=45, angx=0, angy=0):
		self.fovy, self.angx, self.angy = fovy, angx, angy
		self.l = self.dial/2/(tan(fovy*pi/360))
		v = np.array([cos(angy)*cos(angx), cos(angy)*sin(angx), sin(angy)])
		self.eye = self.center + v*self.l*1
		self.count_mvp()
		#print('reset', self.eye, self.center)

	def set_pers(self, fovy=None, angx=None, angy=None, l=None, pers=None):
		if not pers is None: self.pers = pers
		if not fovy is None: self.fovy = fovy
		if not angx is None: self.angx = angx
		if not angy is None: self.angy = angy
		self.angx %= 2*pi
		self.angy = max(min(pi/2-1e-4, self.angy), -pi/2+1e-4)
		if not l is None: self.l = l
		v = np.array([cos(self.angy)*cos(self.angx), 
			cos(self.angy)*sin(self.angx), sin(self.angy)])
		
		self.eye = self.center + v*self.l*1
		self.count_mvp()

	def show(self, title='Myvi'):
		import wx
		from .frame3d import Frame3D
		app = wx.App(False)
		self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
		Frame3D(None, title, self).Show()
		app.MainLoop()

if __name__ == '__main__':
	img = imread('gis.png')
	build_surf2d(img)
