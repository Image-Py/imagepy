import wx
import numpy as np
from sciapp.action import ImageTool
from sciapp.util import mark2shp, geom2shp
from sciapp.object import ROI
from sciapp.action import Filter
from shapely.affinity import affine_transform
import scipy.ndimage as nimg

class RotateTool(ImageTool):
    """RotateTool class derived from sciapp.action.Tool"""
    def __init__(self, plg):
        self.plg = plg
        self.para = plg.para
        self.moving = False
        
    def mouse_down(self, ips, x, y, btn, **key):  
        lim = 5.0/key['canvas'].scale 
        if abs(x-self.para['ox'])<lim and abs(y-self.para['oy'])<lim:
            self.moving = True
        
    def mouse_up(self, ips, x, y, btn, **key):
        if self.moving : self.moving = False
        else : self.plg.preview(ips, self.para)
        
    def mouse_move(self, ips, x, y, btn, **key):
        lim = 5.0/key['canvas'].scale
        if btn==None:
            self.cursor = 'cross'
            if abs(x-self.para['ox'])<lim and abs(y-self.para['oy']<lim):
                self.cursor = wx.CURSOR_HAND
        elif self.moving:
            self.para['ox'], self.para['oy'] = x, y
            # self.plg.dialog.reset()
            self.plg.make_mark()
            ips.update()
        else:
            dx, dy = x-self.para['ox'], y-self.para['oy']
            ang = np.arccos(dx/np.sqrt(dx**2+dy**2))
            if dy<0: ang = np.pi*2-ang
            ang = int(ang/np.pi*180)
            self.para['ang'] = ang
            #self.plg.dialog.reset()
            self.plg.make_mark()
            ips.update()

class Plugin(Filter):
    """RotateTool class plugin derived from sciapp.action.Filter"""
    modal = False
    title = 'Rotate'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'ang':0, 'ox':0, 'oy':0, 'img':True, 'msk':False}
    view = [(int, 'ang', (0,360), 0, 'angle', 'degree'),
            (int, 'ox',  (0,5000), 0, 'OX', 'pix'),
            (int, 'oy',  (0,5000), 0, 'OY', 'pix'),
            (bool, 'img', 'rotate image'),
            (bool, 'msk', 'rotate mask')]
        
    def load(self, ips):
        self.bufroi = ips.roi
        self.para['oy'], self.para['ox'] = np.array(ips.shape)/2
        if ips.roi!=None:
            box = ips.roi.box
            if box[0]!=box[2] and box[1]!=box[3]:
                self.para['oy'] = int((box[1]+box[3])/2)
                self.para['ox'] = int((box[0]+box[2])/2)
        self.make_mark()
        ips.update()
        ips.tool = RotateTool(self).start(self.app, 'local')
        return True
        
    def cancel(self, ips):
        Filter.cancel(self, ips)
        ips.roi = self.bufroi
        ips.mark = ips.tool = None
        
    def ok(self, ips, para=None):
        ips.mark = ips.tool = None
        Filter.ok(self, ips, para)
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((0,255,0), width=1, style=wx.SOLID))
        sox, soy = f(self.para['ox'], self.para['oy'])
        dc.DrawCircle((sox, soy), 5)
        a = np.linspace(0, 2*np.pi, 20)
        dc.DrawLines(list(zip(sox+np.cos(a)*40, soy+np.sin(a)*40)))
        a = self.para['ang']*np.pi/180
        dc.DrawCircle((sox+np.cos(a)*40, soy+np.sin(a)*40), 3)
        
    def make_mark(self):
        a = self.para['ang']/180.0*np.pi
        mark = {'type':'layer', 'color':(0,255,0), 'body':[
            {'type':'circle', 'fcolor':(255,255,255), 'fill':True, 'body':(self.para['ox'], self.para['oy'], 5)},
            {'type':'circle', 'body':(self.para['ox'], self.para['oy'], 50)},
            {'type':'circle', 'fcolor':(255,255,255), 'fill':True, 'body':(self.para['ox']+np.cos(a)*50, 
                self.para['oy']+np.sin(a)*50, 3)}]}
        self.ips.mark = mark2shp(mark)

    def preview(self, ips, para):
        Filter.preview(self, ips, para)
        self.make_mark()

    def run(self, ips, img, buf, para = None):
        if para == None: para = self.para
        a = para['ang']/180.0*np.pi
        trans = np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
        o = np.array([self.para['oy'], self.para['ox']])
        offset = o-trans.dot(o)
        if self.para['img']:
            nimg.affine_transform(img, trans, output=buf, offset=offset)
        if self.para['msk'] and self.bufroi!=None:
            m, o = trans, o[::-1]-trans.dot(o[::-1])
            mat = [m[0,0], m[0,1], m[1,0], m[1,1], o[0], o[1]]
            ips.roi = ROI(geom2shp(affine_transform(self.bufroi.to_geom(), mat)))