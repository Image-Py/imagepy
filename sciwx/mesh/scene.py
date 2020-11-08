import numpy as np
import moderngl
from .matutil import *
import numpy as np
from math import sin, cos, tan, pi
from sciapp.object import Surface, MarkText, MeshSet

class Scene:
	def __init__(self):
		self.title = 'Scene'
		self.h, self.v, self.r = 1.5, 0, 300
		self.ratio, self.dial = 1.0, 1.0
		self.pers, self.center = True, (0,0,0)
		self.angx = self.angy = 0
		self.fovy = self.l = 1
		self.background = 0.4, 0.4, 0.4
		self.light = (1,0,0)
		self.bright, self.scatter = 0.66, 0.66
		self.meshset = MeshSet()
		self.vabo = {}
		self.ctx = None

	def set_mesh(self, mesh): 
		self.meshset = mesh
		self.vabo = {}
		for i in self.objs:
			self.add_surf(i, self.objs[i])

	def on_ctx(self, ctx):
		self.ctx = ctx
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
		for i in self.objs:
			if isinstance(self.objs[i], MarkText): 
				self.ctx_txt(self.ctx, self.prog_txt, self.objs[i], i)
			elif isinstance(self.objs[i], Surface): 
				self.ctx_obj(self.ctx, self.prog_suf, self.objs[i], i)

	@property
	def objs(self): return self.meshset.objs

	def ctx_obj(self, ctx, prog, obj, name):
		vts, ids, ns, cs = obj.vts, obj.ids, obj.ns, obj.cs
		buf = np.zeros((len(vts), 9), dtype=np.float32)
		buf[:,0:3], buf[:,3:6], buf[:,6:9] = vts, ns, cs
		vbo = ctx.buffer(buf.tobytes())
		ibo = ctx.buffer(ids.tobytes())
		content = [(vbo, '3f 3f 3f', 'v_vert', 'v_norm', 'v_color')]
		vao = ctx.vertex_array(prog, content, ibo)
		self.vabo[name] = [buf, vao, vbo]

	def ctx_txt(self, ctx, prog, obj, name):
		vts, ids, os, cs = obj.vts, obj.ids, obj.os, obj.cs
		buf = self.buf = np.zeros((len(vts), 6), dtype=np.float32)
		buf[:,0:3], buf[:,3:6] = vts, os
		vbo = ctx.buffer(buf.tobytes())
		ibo = ctx.buffer(ids.tobytes())
		content = [(vbo, '3f 3f', 'v_vert', 'v_pos')]
		vao = ctx.vertex_array(prog, content, ibo)
		self.vabo[name] = [buf, vao, vbo]

	def add_surf(self, name, obj):
		if isinstance(obj, tuple):
			if isinstance(obj[3], (int, float)):
				obj = MarkText(*obj)
			else: obj = Surface(*obj)
		if not self.ctx is None:
			if isinstance(obj, MarkText):
				self.ctx_txt(self.ctx, self.prog_txt, obj, name)
			elif isinstance(obj, Surface):
				self.ctx_obj(self.ctx, self.prog_suf, obj, name)

		self.objs[name] = obj
		self.count_box()

	def get_obj(self, key): return self.meshset.get_obj(key)

	def draw_obj(self, name, obj, ctx, prog, mvp, light, bright, scatter):
		if not obj.visible: return
		ctx.line_width = obj.width
		mvp = np.dot(*mvp)
		prog['Mvp'].write(mvp.astype(np.float32).tobytes())
		prog['blend'].value = obj.alpha
		prog['scatter'].value = scatter
		prog['light'].value = tuple(light)
		prog['bright'].value = bright
		mode = {'mesh':moderngl.TRIANGLES, 'grid':moderngl.LINES}[obj.mode]
		if obj.update:
			self.vabo[name][0][:,6:9] = obj.cs
			self.vabo[name][0][:,:3] = obj.vts
			self.vabo[name][2].write(self.vabo[name][0].tobytes())
			obj.update = False
		self.vabo[name][1].render(mode)

	def draw_txt(self, name, obj, ctx, prog, mvp, light, bright, scatter):
		if not obj.visible: return
		ctx.line_width = obj.width
		prog['mv'].write(mvp[0].astype(np.float32).tobytes())
		prog['proj'].write(mvp[1].astype(np.float32).tobytes())
		prog['f_color'].write(np.array(obj.cs).astype(np.float32).tobytes())
		prog['h'].value = obj.h
		self.vabo[name][1].render(moderngl.LINES)

	def draw(self):
		self.ctx.clear(*self.background)
		self.ctx.enable(moderngl.DEPTH_TEST)
		#self.ctx.enable(ModernGL.CULL_FACE)
		self.ctx.enable(moderngl.BLEND)
		for i in self.objs: 
			prog = self.prog_txt if isinstance(self.objs[i], MarkText) else self.prog_suf
			draw = self.draw_txt if isinstance(self.objs[i], MarkText) else self.draw_obj
			draw(i, self.objs[i], self.ctx, prog, self.mvp, self.light, self.bright, self.scatter)

	def count_box(self):
		minb = [i.box[0] for i in self.objs.values() if not i.box is None]
		minb = np.array(minb).min(axis=0)
		maxb = [i.box[1] for i in self.objs.values() if not i.box is None]
		maxb = np.array(maxb).max(axis=0)
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