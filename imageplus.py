import numpy as np
from core.managers import WindowsManager, ColorManager

def get_img_type(imgs):
    if imgs[0].ndim==3:return 'rgb'
    if imgs[0].dtype == np.uint8:return '8-bit'
    if imgs[0].dtype == np.uint16:return '16-bit'
    if imgs[0].dtype == np.float32:return 'float'
        
    
class ImagePlus:
    def __init__(self, imgs, title=None, is3d=False):
        self.set_imgs(imgs)
        self.set_title(title)
        self.snap = None
        self.cur = 0
        self.update = False
        self.scrchanged = False
        self.roi = None
        self.mark = None
        self.msk = None
        self.mskmode = None
        self.lut = ColorManager.get_lut('grey')
        self.tool = None
        
    def set_title(self, title):
        self.title = WindowsManager.name(title)
        
    def set_imgs(self, imgs):
        self.is3d = not isinstance(imgs, list)
        self.scrchanged = True
        self.snap = None
        self.imgs = imgs
        
        self.height, self.width = self.size = self.imgs[0].shape[:2]
        print self.height, self.width
        self.imgtype = get_img_type(self.imgs)
        self.chanels = 1 if self.imgs[0].ndim==2 else self.imgs[0].shape[2]
        self.dtype = self.imgs[0].dtype
        self.range = (0, 255)
        if self.dtype == np.uint16: 
            self.range = (0,imgs[0].max())
        
    def get_imgtype(self):return self.imgtype
        
    def get_nslices(self):return len(self.imgs)
        
    def get_nchannels(self):return self.chanels
        
    def set_cur(self, n):
        if n>=0 and n<len(self.imgs):self.cur=n
    
    def get_nbytes(self):
        return self.imgs[0].nbytes * len(self.imgs)
        
    def get_img(self, cur=None):
        if cur!=None:return self.imgs[cur]
        return self.imgs[self.cur]
        
    def get_msk(self, mode='in'):
        if self.roi==None:return None
        if self.msk == None:
            self.msk = np.zeros(self.size, dtype=np.bool)
        if self.roi.update or mode!=self.mskmode:
            self.msk[:] = 0
            if isinstance(mode, int):
                self.roi.sketch(self.msk, w=mode, color=True)
            else: self.roi.fill(self.msk, color=True)
            if mode=='out':self.msk-=True
            self.roi.update = False
            self.mskmode=mode
        return self.msk
        
    def get_rect(self):
        if self.roi==None:return None
        box = self.roi.get_box()
        l, r = max(0, box[0]), min(self.size[1], box[2])
        t, b = max(0, box[1]), min(self.size[0], box[3])
        return slice(t,b), slice(l,r)
        
    def get_subimg(self, s1=None, s2=None):
        if s1==None:
            s1, s2 = self.get_rect()
        return self.get_img()[s1, s2]
        
    def snapshot(self):
        if self.snap==None:
            self.snap = self.get_img().copy()
        else: self.snap[...] = self.get_img()
        
    def reset(self, msk=False):
        if self.snap!=None:
            if msk and self.get_msk('out')!=None:
                msk = self.get_msk('out')
                self.imgs[self.cur][msk] = self.snap[msk]
            else : self.imgs[self.cur][:] = self.snap
            
    def lookup(self):
        if self.chanels==1 and self.dtype==np.uint8:
            return self.lut[self.get_img()]
        if self.chanels==1 and self.dtype==np.uint16:
            k = 255.0/self.range[1]
            bf = np.multiply(self.get_img(), k, dtype=np.uint8)
            return self.lut[bf]
        if self.chanels==3 and self.dtype==np.uint8:
            return self.get_img()
            
    def swap(self):
        if self.snap==None:return
        self.snap, self.imgs[self.cur] = self.imgs[self.cur], self.snap

if __name__=='__main__':
    from scipy.misc import imread
    img = imread('results.bmp')
    ips = ImagePlus([img, 255-img])
    
    from ui.canvasframe import CanvasFrame
    import wx
    
    app = wx.PySimpleApp()
    frame = CanvasFrame()
    frame.set_ips(ips)
    frame.Show()
    app.MainLoop() 
    
