import struct
import numpy as np
import ModernGL
from time import time

from scipy.misc import imread
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

	def on_ctx(self, ctx, prog):
		vts, ids, ns, cs = self.vts, self.ids, self.ns, self.cs;
		buf = self.buf = np.zeros((len(vts), 9), dtype=np.float32)
		buf[:,0:3], buf[:,3:6], buf[:,6:9] = vts, ns, cs
		self.vbo = ctx.buffer(buf.tobytes())
		ibo = ctx.buffer(ids.tobytes())
		ctx.line_width = 1
		content = [(self.vbo, '3f3f3f', ['v_vert', 'v_norm', 'v_color'])]
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

	def draw(self, mvp):
		if not self.visible: return
		self.prog.uniforms['Mvp'].write(mvp.astype(np.float32).tobytes())
		self.prog.uniforms['blend'].value = self.blend

		self.vao.render({'mesh':ModernGL.TRIANGLES, 'grid':ModernGL.LINES}[self.mode])

class Manager:
	def __init__(self):
		self.h, self.v, self.r = 1.5, 0, 300
		self.ratio, self.dial = 1.0, 1.0
		self.pers, self.center = True, (0,0,0)
		self.background = 0.4, 0.4, 0.4
		self.objs = {}
		self.ctx = None

	def on_ctx(self):
		self.ctx = ModernGL.create_context()
		self.prog_suf = self.ctx.program([
			self.ctx.vertex_shader('''
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
            '''),
            self.ctx.fragment_shader('''
                #version 330
                uniform vec3 light = vec3(1,1,0.8);
                uniform float blend = 1;
                in vec3 f_norm;
                in vec3 f_color;
                out vec4 color;
                void main() {
                    float d = clamp((dot(light, f_norm)+1)*0.5, 0, 1);
           			color = vec4(f_color*d, blend);
                }
			'''),
		])
		for i in self.objs.values():
			i.on_ctx(self.ctx, self.prog_suf)

	def add_obj(self, name, vts, ids, ns=None, cs=(0,0,1)):
		surf = Surface(vts, ids, ns, cs)
		if not self.ctx is None:
			surf.on_ctx(self.ctx, self.prog_suf)
		self.objs[name] = surf
		self.count_box()
		return surf

	def get_obj(self, key):
		if not key in self.objs: return None
		return self.objs[key]

	def draw(self):
		self.ctx.clear(*self.background)
		self.ctx.enable(ModernGL.DEPTH_TEST)
		#self.ctx.enable(ModernGL.CULL_FACE)
		self.ctx.enable(ModernGL.BLEND)
		for i in self.objs.values(): i.draw(self.mvp)

	def count_box(self):
		minb = np.array([i.box[0] for i in self.objs.values()]).min(axis=0)
		maxb = np.array([i.box[1] for i in self.objs.values()]).max(axis=0)
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
		self.mvp = np.dot(lookat, proj)
		
	def set_viewport(self, x, y, width, height):
		self.ctx.viewport = (x, y, width, height)
		self.ratio = width*1.0/height

	def set_background(self, rgb):
		self.background = rgb

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
		Frame3D(None, title, self).Show()
		app.MainLoop()

if __name__ == '__main__':
	img = imread('gis.png')
	build_surf2d(img)