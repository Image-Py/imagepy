import wx
from sciapp.action import ImageTool
#from imagepy.core import myvi
#from imagepy import IPy
import numpy as np

class Plugin(ImageTool):
    title = 'Cursor 3D'
    para = {'r':1, 'color':(255,0,0)}
    view = [(int, 'r', (0,100), 0,  'radius', 'pix'),
            ('color', 'color', 'color', '')]

    def __init__(self):
        self.pressed = False
        self.cursor = wx.CURSOR_CROSS
            
    def set_cursor(self, x, y, z):
        if not self.pressed: return
        frame = myvi.Frame3D.figure(IPy.curapp, title='3D Canvas')
        manager = frame.viewer.canvas.manager
        obj = manager.get_obj('cursor')
        color = tuple(np.array(self.para['color'])/255.0)
        vts, fs, ns, cs = myvi.build_ball((y, x, z), self.para['r'], color)
        obj.set_style(visible=True)
        obj.buf[:,0:3], obj.buf[:,3:6], obj.buf[:,6:9] = vts, ns, cs
        obj.vbo.write(obj.buf.tobytes())
        frame.viewer.Refresh(False)

    def mouse_down(self, ips, x, y, btn, **key):
        z = ips.cur
        frame = myvi.Frame3D.figure(IPy.curapp, title='3D Canvas')
        manager = frame.viewer.canvas.manager
        obj = manager.get_obj('cursor')
        color = tuple(np.array(self.para['color'])/255.0)
        vts, fs, ns, cs = myvi.build_ball((y, z, x), self.para['r'], color)
        if obj==None:
            obj = manager.add_surf('cursor', vts, fs, ns, cs, real=False)
        self.set_cursor(y, z, x)
        self.pressed = True
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.pressed = False
        frame = myvi.Frame3D.figure(IPy.curapp, title='3D Canvas')
        manager = frame.viewer.canvas.manager
        obj = manager.get_obj('cursor')
        if obj!=None: obj.set_style(visible=False)
        frame.viewer.canvas.Refresh(False)
    
    def mouse_move(self, ips, x, y, btn, **key):
        if not self.pressed: return
        self.set_cursor(y, ips.cur, x)
        
    def mouse_wheel(self, ips, x, y, d, **key):
        if d>0:
            if ips.cur<ips.get_nslices()-1:
                ips.cur+=1
        if d<0:
            if ips.cur>0:ips.cur-=1
        ips.update()
        if not self.pressed: return
        self.set_cursor(y, ips.cur, x)