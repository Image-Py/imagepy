import wx, weakref
import numpy as np
from vispy import app, scene, gloo
import platform, os.path as osp
from vispy.visuals.transforms import STTransform
from vispy.color import Colormap
from sciapp.object import Mesh, TextSet, Volume3d, Scene
from sciapp.action import MeshTool

# verts, faces, colors, mode, alpha, visible
# light_dir, light, ambiass, background

class MeshVisual(scene.visuals.Mesh):
    def __init__(self, *p, **key):
        scene.visuals.Mesh.__init__(self, *p, **key)
        self.unfreeze()
        self._light_color = (0.7,0.7,0.7, 1.0)
        self.freeze()

    @property
    def light_color(self):
        return self._light_color

    @light_color.setter
    def light_color(self, light):
        self._light_color = light
        self.mesh_data_changed()
    
    def _update_data(self):
        rst = scene.visuals.Mesh._update_data(self)
        if self.shading is not None:
            self.shared_program.vert['light_color'] = self._light_color
        return rst

class VolumeVisual(scene.visuals.Volume):
    def set_data(self, vol, clim=None, copy=True):
        scene.visuals.Volume.set_data(self, vol.transpose(2,1,0), clim, copy)

    def _compute_bounds(self, axis, view):
        return 0, self._vol_shape[::-1][axis]

def viewmesh(mesh, view):
    if mesh.dirty == 'geom':
        faces = mesh.faces
        if mesh.mode == 'grid': faces = mesh.get_edges()
        if mesh.mode == 'points': faces = np.arange(len(mesh.verts))
        shading = 'smooth' if mesh.mode == 'mesh' else None
        if view is None or view.shading!=shading: 
            if not view is None: view.parent = None
            view = MeshVisual(shading=shading)
        dic = {'mesh':'triangles', 'grid':'lines', 'points':'points'}
        view._draw_mode = dic[mesh.mode]
        key = {'vertices':mesh.verts, 'faces':faces}
        if isinstance(mesh.colors, tuple): colorkey = 'color'
        elif mesh.colors.ndim == 2: colorkey = 'vertex_colors'
        elif mesh.colors.ndim == 1: colorkey = 'vertex_values'

        key[colorkey] = mesh.colors
        view.set_data(**key)

    view.interactive = True
    view.shininess = 0
    if isinstance(mesh.cmap, str): cmap = mesh.cmap
    elif mesh.cmap.max()>1+1e-5: cmap = Colormap(mesh.cmap/255)
    else: cmap = Colormap(mesh.cmap)
    view.cmap = cmap
    view.visible = mesh.visible
    view.opacity = mesh.alpha
    if mesh.high_light is False:
        view._picking_filter.enabled = False
        view._picking_filter.id = view._id
    else:
        view._picking_filter.enabled = True
        view._picking_filter.id = mesh.high_light
    # view.shading = 'flat'
    mesh.dirty = False
    return view

def viewtext(text, view):
    if text.dirty=='geom':
        if view is None: 
            view = scene.visuals.Text()

        view.text = text.texts
        view.pos = text.verts
        view.color = text.colors
        view.font_size = text.size

    view.interactive = True
    view.visible = text.visible
    view.opacity = text.alpha
    if text.high_light is False:
        view._picking_filter.enabled = False
        view._picking_filter.id = view._id
    else:
        view._picking_filter.enabled = True
        view._picking_filter.id = mesh.high_light
    # view.shading = 'flat'
    text.dirty = False
    return view

def viewvolume(vol, view):
    if isinstance(vol.cmap, str): cmap = vol.cmap
    elif vol.cmap.max()>1+1e-5: cmap = Colormap(vol.cmap/255)
    else: cmap = Colormap(vol.cmap)
    if vol.dirty=='geom':
        if view is None: 
            view = VolumeVisual(vol.imgs, emulate_texture=False, cmap=cmap)
        view.relative_step_size = vol.step
        view.threshold = vol.level
    
    view.interactive = True
    view.visible = vol.visible
    view.opacity = vol.alpha
    if vol.high_light is False:
        view._picking_filter.enabled = False
        view._picking_filter.id = view._id
    else:
        view._picking_filter.enabled = True
        view._picking_filter.id = mesh.high_light
    # view.shading = 'flat'
    vol.dirty = False
    return view


def viewobj(obj, view):
    if isinstance(obj, Mesh): return viewmesh(obj, view)
    if isinstance(obj, TextSet): return viewtext(obj, view)
    if isinstance(obj, Volume3d): return viewvolume(obj, view)

class Canvas3D(scene.SceneCanvas):
    def __new__(cls, parent, scene3d=None):
        self = super().__new__(cls)
        scene.SceneCanvas.__init__(self, app="wx", parent=parent, keys='interactive', show=True, dpi=150)
        canvas = parent.GetChildren()[-1]
        self.unfreeze()
        self.canvas = weakref.ref(canvas)
        self.view = self.central_widget.add_view()
        self.set_scene(scene3d or Scene())
        self.visuals = {}
        self.curobj = None
        self.freeze()
        canvas.Bind(wx.EVT_IDLE, self.on_idle)
        canvas.tool = None
        canvas.camera = scene.cameras.TurntableCamera(parent=self.view.scene, fov=45, name='Turntable')
        canvas.set_camera = self.set_camera
        canvas.fit = lambda : self.set_camera(auto=True)
        canvas.at = self.at
        self.view.camera = canvas.camera
        return canvas

    def __init__(self, **kwargs): pass

    def set_scene(self, scene):
        self.scene3d = scene
        self.canvas().scene3d = self.scene3d
        self.canvas().add_obj = self.scene3d.add_obj

    def on_idle(self, event):
        need = 'ignore'
        if self.scene3d.dirty:
            need = 'update'
            self.bgcolor = self.scene3d.bg_color
            for i in self.visuals:
                self.visuals[i].ambient_light_color = self.scene3d.ambient_color
                self.visuals[i].light_color = self.scene3d.light_color
                self.visuals[i].light_dir = self.scene3d.light_dir
            self.scene3d.dirty = False
        for i in self.scene3d.names:
            obj = self.scene3d.objects[i]
            if not i in self.visuals:
                self.visuals[i] = viewobj(obj, None)
                need = 'add'
            vis = self.visuals[i]
            if obj.dirty != False:
                self.visuals[i] = viewobj(obj, vis)
                if need=='ignore': need = 'update'
            self.visuals[i].parent = self.view.scene
        if need == 'add': self.canvas().fit()
        if need != 'ignore': 
            print('need')
            self.update()

    def set_camera(self, azimuth=None, elevation=None, dist=None, fov=None, auto=False):
        if not azimuth is None: self.canvas().camera.azimuth = azimuth
        if not elevation is None: self.canvas().camera.elevation = elevation
        if not fov is None: self.canvas().camera.fov = fov
        if auto: self.canvas().camera.set_range()
    
    def at(self, x, y):
        self.view.interactive = False
        vis = self.visual_at((x, y))
        self.view.interactive = True
        for k in self.visuals:
            if self.visuals[k] is vis:
                    return self.scene3d.objects[k]
        return None

    def _process_mouse_event(self, event):
        # self.measure_fps()
        # return scene.SceneCanvas._process_mouse_event(self, event)
        px, py = x, y = tuple(event.pos)
        canvas, tool, btn = self.canvas(), self.canvas().tool or MeshTool.default, event._button
        btn = {2:3, 3:2}.get(btn, btn)
        ld, rd, md = [i in event.buttons for i in (1,2,3)]
        sta = [i in [j.name for j in event.modifiers] for i in ('Alt', 'Control', 'Shift')]
        others = {'alt':sta[0], 'ctrl':sta[1],
            'shift':sta[2], 'px':px, 'py':py, 'canvas':canvas}
        
        if event.type == 'mouse_press':
            canvas.SetFocus()
            tool.mouse_down(canvas.scene3d, x, y, btn, **others)
        if event.type == 'mouse_release':
            tool.mouse_up(canvas.scene3d, x, y, btn, **others)
        if event.type == 'mouse_move':
            tool.mouse_move(canvas.scene3d, x, y, None, **others)
        
        wheel = np.sign(event.delta[1])
        #if me.Dragging():
        #    tool.mouse_move(canvas.scene3d, x, y, btn, **others)
        if wheel!=0:
            tool.mouse_wheel(canvas.scene3d, x, y, wheel, **others)
        ckey = {'arrow':1,'cross':5,'hand':6}
        cursor = ckey[tool.cursor] if tool.cursor in ckey else 1
        canvas.SetCursor(wx.Cursor(cursor))
        event.handled = True

    def __del__(self):
        # self.img = self.back = None
        print('========== canvas del')

def make_bitmap(bmp):
    img = bmp.ConvertToImage()
    img.Resize((20, 20), (2, 2))
    return img.ConvertToBitmap()
