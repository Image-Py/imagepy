import wx
import numpy as np
from imagepy.core.engine import Tool, Filter
import scipy.ndimage as nimg

class RotateTool(Tool):
    """RotateTool class derived from imagepy.core.engine.Tool"""
    def __init__(self, plg):
        self.plg = plg
        self.para = plg.para
        self.moving = False
        
    def mouse_down(self, ips, x, y, btn, **key):  
        lim = 5.0/key['canvas'].get_scale() 
        if abs(x-self.para['ox'])<lim and abs(y-self.para['oy'])<lim:
            self.moving = True
        
    def mouse_up(self, ips, x, y, btn, **key):
        if self.moving : self.moving = False
        else : self.plg.preview(ips, self.para)
        
    def mouse_move(self, ips, x, y, btn, **key):
        lim = 5.0/key['canvas'].get_scale()
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if abs(x-self.para['ox'])<lim and abs(y-self.para['oy']<lim):
                self.cursor = wx.CURSOR_HAND
        elif self.moving:
            self.para['ox'], self.para['oy'] = x, y
            self.plg.dialog.reset()
            ips.update = True
        else:
            dx, dy = x-self.para['ox'], y-self.para['oy']
            ang = np.arccos(dx/np.sqrt(dx**2+dy**2))
            if dy<0: ang = np.pi*2-ang
            ang = int(ang/np.pi*180)
            self.para['ang'] = ang
            self.plg.dialog.reset()
            ips.update = True

class Plugin(Filter):
    """RotateTool class plugin derived from imagepy.core.engine.Filter"""
    modal = False
    title = 'Rotate'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'ang':0, 'ox':0, 'oy':0, 'img':True, 'msk':False}
    view = [(int, (0,360), 0, 'angle', 'ang', 'degree'),
            (int, (0,5000), 0, 'OX', 'ox', 'pix'),
            (int, (0,5000), 0, 'OY', 'oy', 'pix'),
            (bool, 'rotate image', 'img'),
            (bool, 'rotate mask', 'msk')]
        
    def load(self, ips):
        self.bufroi = ips.roi
        self.para['oy'], self.para['ox'] = np.array(ips.size)/2
        if ips.roi!=None:
            box = ips.roi.get_box()
            if box[0]!=box[2] and box[1]!=box[3]:
                self.para['oy'] = int((box[1]+box[3])/2)
                self.para['ox'] = int((box[0]+box[2])/2)
        ips.mark = self
        ips.update = True
        ips.tool = RotateTool(self)
        return True
        
    def cancel(self, ips):
        Filter.cancel(self, ips)
        ips.roi = self.bufroi
        ips.mark = None
        ips.tool = None
        ips.update = 'pix'
        
    def ok(self, ips, para=None):
        Filter.ok(self, ips, para)
        ips.mark = None
        ips.tool = None
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((0,255,0), width=1, style=wx.SOLID))
        sox, soy = f(self.para['ox'], self.para['oy'])
        dc.DrawCircle((sox, soy), 5)
        a = np.linspace(0, 2*np.pi, 20)
        dc.DrawLines(list(zip(sox+np.cos(a)*40, soy+np.sin(a)*40)))
        a = self.para['ang']*np.pi/180
        dc.DrawCircle((sox+np.cos(a)*40, soy+np.sin(a)*40), 3)
        
    def run(self, ips, img, buf, para = None):
        if para == None: para = self.para
        a = para['ang']/180.0*np.pi
        trans = np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
        o = np.array([self.para['oy'], self.para['ox']])
        offset = o-trans.dot(o)
        if self.para['img']:
            nimg.affine_transform(img, trans, output=buf, offset=offset)
        if self.para['msk'] and self.bufroi!=None:
            ips.roi = self.bufroi.affine(trans, o[::-1]-trans.dot(o[::-1]))