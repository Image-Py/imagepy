import numpy as np
from sciapp.action import Filter
from sciapp.action import ImageTool
from sciapp.util import mark2shp, geom2shp
from shapely.affinity import affine_transform
from sciapp.object import ROI
import scipy.ndimage as nimg

class ScaleTool(ImageTool):
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
        lim = 5.0/key['canvas'].scale  
        self.moving = self.snap(x, y, lim)
        print(self.moving)
        
    def mouse_up(self, ips, x, y, btn, **key):
        if self.moving : 
            print('moving ==========')
            self.plg.preview(ips, self.para)
        
    def mouse_move(self, ips, x, y, btn, **key):
        lim = 5.0/key['canvas'].scale
        if btn==None:
            self.cursor = 'cross'
            if isinstance(self.snap(x, y, lim), str):
                self.cursor = 'hand'
        elif self.moving==True:
            self.plg.lt+=x-self.ox
            self.plg.rt+=x-self.ox
            self.plg.bm+=y-self.oy
            self.plg.tp+=y-self.oy
            self.ox, self.oy = x, y
            self.plg.count()
            self.plg.make_mark()
            ips.update()
        elif self.moving != False:
            if 'l' in self.moving:self.plg.lt = x
            if 'r' in self.moving:self.plg.rt = x
            if 't' in self.moving:self.plg.tp = y
            if 'b' in self.moving:self.plg.bm = y
            self.plg.count()
            self.plg.make_mark()
            ips.update()

class Plugin(Filter):
    modal = False
    title = 'Scale'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'kx': 1, 'ky':1, 'ox':0, 'oy':0, 'img':True, 'msk':False}
    view = [(float, 'kx', (-100,100), 3, 'KX', ''),
            (float, 'ky', (-100,100), 3, 'KY', ''),
            (int, 'ox', (-10000,10000), 0, 'OffX', 'pix'),
            (int, 'oy', (-10000,10000), 0, 'OffY', 'pix'),
            (bool, 'img', 'scale image'),
            (bool, 'msk', 'scale mask')]
        
    def make_mark(self):
        mark = {'type':'layer', 'body':[
            {'type':'rectangle', 'color':(0,255,0), 
            'body':(self.lt, self.tp, self.rt-self.lt, self.bm-self.tp)},
            {'type':'points', 'color':(0,255,0), 'body':[(self.lt, self.tp), 
            (self.lt, self.bm), (self.rt, self.tp), (self.rt, self.bm), 
            (self.lt, (self.tp+self.bm)/2), (self.rt, (self.tp+self.bm)/2),
            ((self.lt+self.rt)/2, self.tp), ((self.lt+self.rt)/2, self.bm)]}
        ]}
        self.ips.mark = mark2shp(mark)

    def load(self, ips):      
        self.bufroi = ips.roi
        self.lt, self.tp, self.rt, self.bm = 0, 0, ips.shape[1], ips.shape[0]
        
        if ips.roi!=None:
            box = ips.roi.box
            if box[0]!=box[2] and box[1]!=box[3]:
                self.lt, self.tp, self.rt, self.bm = box

        self.orio = ((self.lt+self.rt)/2,(self.tp+self.bm)/2)
        self.oriw, self.orih = self.rt - self.lt, self.tp - self.bm

        self.para['ox'] = (self.lt+self.rt)/2
        self.para['oy'] = (self.tp+self.bm)/2
        self.para['kx'] = self.para['ky'] = 1
        
        self.make_mark()
        ips.update()
        ips.tool = ScaleTool(self).start(self.app, 'local')
        return True
        
    def count(self, dir=True):
        if dir:
            self.para['ox'] = (self.lt+self.rt)/2
            self.para['oy'] = (self.tp+self.bm)/2
            self.para['kx'] = (self.rt-self.lt)*1.0/self.oriw
            self.para['ky'] = (self.tp-self.bm)*1.0/self.orih
        else:
            self.lt = self.para['ox']-self.oriw*self.para['kx']/2
            self.rt = self.para['ox']+self.oriw*self.para['kx']/2
            self.bm = self.para['oy']-self.orih*self.para['ky']/2
            self.tp = self.para['oy']+self.orih*self.para['ky']/2

    def ok(self, ips, para=None):
        ips.mark = ips.tool = None
        Filter.ok(self, ips, para)
        
    def cancel(self, ips):
        Filter.cancel(self, ips)
        ips.roi = self.bufroi
        ips.mark = ips.tool = None
        
    def preview(self, ips, para):
        Filter.preview(self, ips, para)
        self.make_mark()

    def run(self, ips, img, buf, para = None):
        if para == None: para = self.para
        self.count(False)
        trans = np.array([[1/self.para['ky'],0],[0,1/self.para['kx']]])
        o = np.array([self.para['oy'], self.para['ox']])
        offset = self.orio[::-1]-trans.dot(o)
        if self.para['img']:
            nimg.affine_transform(img, trans, output=buf, offset=offset)
        trans = np.array([[self.para['kx'],0],[0, self.para['ky']]])
        if self.para['msk'] and self.bufroi!=None:
            m, o = trans, o[::-1]-trans.dot(self.orio)
            mat = [m[0,0], m[0,1], m[1,0], m[1,1], o[0], o[1]]
            ips.roi = ROI(geom2shp(affine_transform(self.bufroi.to_geom(), mat)))
