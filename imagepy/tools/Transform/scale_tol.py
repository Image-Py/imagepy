import wx
import numpy as np
from imagepy.core.engine import Tool, Filter
import scipy.ndimage as nimg

class ScaleTool(Tool):
    def __init__(self, plg):
        self.plg = plg
        self.para = plg.para
        self.moving = False
        
    def snap(self, x, y, lim):
        plg = self.plg
        if abs(x-plg.lt)<lim and abs(y-(plg.tp+plg.bm)/2)<lim:return 'l'
        if abs(x-plg.rt)<lim and abs(y-(plg.tp+plg.bm)/2)<lim:return 'r'
        if abs(x-(plg.lt+plg.rt)/2)<lim and abs(y-plg.tp)<lim:return 't'
        if abs(x-(plg.lt+plg.rt)/2)<lim and abs(y-plg.bm)<lim:return 'b'
        if abs(x-plg.lt)<lim and abs(y-plg.tp)<lim:return 'lt'
        if abs(x-plg.rt)<lim and abs(y-plg.bm)<lim:return 'rb'
        if abs(x-plg.rt)<lim and abs(y-plg.tp)<lim:return 'rt'
        if abs(x-plg.lt)<lim and abs(y-plg.bm)<lim:return 'lb'
        if (x-plg.lt)*(x-plg.rt)<0 and (y-plg.tp)*(y-plg.bm)<0:
            self.ox, self.oy = x, y
            return True
        return False
        
    def mouse_down(self, ips, x, y, btn, **key):  
        lim = 5.0/key['canvas'].get_scale()  
        self.moving = self.snap(x, y, lim)
        print(self.moving)
        
    def mouse_up(self, ips, x, y, btn, **key):
        if self.moving : self.plg.preview(ips, self.para)
        
    def mouse_move(self, ips, x, y, btn, **key):
        lim = 5.0/key['canvas'].get_scale()
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if isinstance(self.snap(x, y, lim), str):
                self.cursor = wx.CURSOR_HAND
        elif self.moving==True:
            self.plg.lt+=x-self.ox
            self.plg.rt+=x-self.ox
            self.plg.bm+=y-self.oy
            self.plg.tp+=y-self.oy
            self.ox, self.oy = x, y
            self.plg.count()
            self.plg.dialog.reset()
            ips.update = True
        elif self.moving != False:
            print("scale_tol.ScaleTool.mouse_move")
            if 'l' in self.moving:self.plg.lt = x
            if 'r' in self.moving:self.plg.rt = x
            if 't' in self.moving:self.plg.tp = y
            if 'b' in self.moving:self.plg.bm = y
            self.plg.count()
            self.plg.dialog.reset()
            ips.update = True

class Plugin(Filter):
    modal = False
    title = 'Scale'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'kx': 1, 'ky':1, 'ox':0, 'oy':0, 'img':True, 'msk':False}
    view = [(float, (-100,100), 3, 'KX', 'kx', ''),
            (float, (-100,100), 3, 'KY', 'ky', ''),
            (int, (-10000,10000), 0, 'OffX', 'ox', 'pix'),
            (int, (-10000,10000), 0, 'OffY', 'oy', 'pix'),
            (bool, 'scale image', 'img'),
            (bool, 'scale mask', 'msk')]

        
    def draw(self, dc, f, **key):
        body = [(self.lt,self.bm),(self.rt,self.bm),
                (self.rt,self.tp),(self.lt,self.tp),(self.lt,self.bm)]
        dc.SetPen(wx.Pen((0,255,0), width=1, style=wx.SOLID))
        dc.DrawLines([f(*i) for i in body])
        for i in body:dc.DrawCircle(f(*i),2)
        dc.DrawCircle(f(self.lt, (self.tp+self.bm)/2),2)
        dc.DrawCircle(f(self.rt, (self.tp+self.bm)/2),2)
        dc.DrawCircle(f((self.lt+self.rt)/2, self.tp),2)
        dc.DrawCircle(f((self.lt+self.rt)/2, self.bm),2)
        
    def load(self, ips):      
        self.bufroi = ips.roi
        self.lt, self.tp, self.rt, self.bm = 0, 0, ips.size[1], ips.size[0]
        
        if ips.roi!=None:
            box = ips.roi.get_box()
            if box[0]!=box[2] and box[1]!=box[3]:
                self.lt, self.tp, self.rt, self.bm = box

        self.orio = ((self.lt+self.rt)/2,(self.tp+self.bm)/2)
        self.oriw, self.orih = self.rt - self.lt, self.tp - self.bm

        self.para['ox'] = (self.lt+self.rt)/2
        self.para['oy'] = (self.tp+self.bm)/2
        self.para['kx'] = self.para['ky'] = 1
        
        ips.mark = self
        ips.update = True
        ips.tool = ScaleTool(self)
        return True
        
    def count(self, dir=True):
        if dir:
            self.para['ox'] = int((self.lt+self.rt)/2)
            self.para['oy'] = int((self.tp+self.bm)/2)
            self.para['kx'] = (self.rt-self.lt)*1.0/self.oriw
            self.para['ky'] = (self.tp-self.bm)*1.0/self.orih
        else:
            self.lt = self.para['ox']-self.oriw*self.para['kx']/2
            self.rt = self.para['ox']+self.oriw*self.para['kx']/2
            self.bm = self.para['oy']-self.orih*self.para['ky']/2
            self.tp = self.para['oy']+self.orih*self.para['ky']/2

    def ok(self, ips, para=None):
        Filter.ok(self, ips, para)
        ips.mark = None
        ips.tool = None
        
    def cancel(self, ips):
        Filter.cancel(self, ips)
        ips.roi = self.bufroi
        ips.mark = None
        ips.tool = None
        ips.update = 'pix'
        
    def run(self, ips, img, buf, para = None):
        if para == None: para = self.para
        self.count(False)
        trans = np.array([[1/self.para['ky'],0],[0,1/self.para['kx']]])
        o = np.array([self.para['oy'], self.para['ox']])
        offset = self.orio[::-1]-trans.dot(o)
        if self.para['img']:
            nimg.affine_transform(img, trans, output=buf, offset=offset)
        trans = np.array([[self.para['kx'],0],[0, self.para['ky']]])
        offset = o[::-1]-trans.dot(self.orio)
        if self.para['msk'] and self.bufroi!=None:ips.roi = self.bufroi.affine(trans, offset)
        if self.para['img'] and not ips.get_msk('out') is None: 
            buf[ips.get_msk('out')] = img[ips.get_msk('out')]
        ips.update = True
