import numpy as np
from time import time
from ..manager import ImageManager, ColorManager

def get_img_type(imgs):
    if imgs[0].ndim==3 and imgs[0].dtype==np.uint8:return 'rgb'
    if imgs[0].dtype == np.uint8:return '8-bit'
    if imgs[0].dtype == np.uint16:return '16-bit'
    if imgs[0].dtype == np.int32:return '32-int'
    if imgs[0].dtype == np.float32:return '32-float'
    if imgs[0].dtype == np.float64:return '64-float'
    if imgs[0].dtype == np.complex128:return '128-complex'
    if imgs[0].dtype == np.complex64:return '64-complex'

def get_updown(imgs, slices='all', chans='all', step=1):
    c = chans if isinstance(chans, int) else slice(None)
    if isinstance(slices, int): imgs = [imgs[slices]]
    if step<=1: step = int(1/step+0.5)
    else: step = int(min(imgs[0].shape[:2])/step+0.5)
    s = slice(None, None, max(step,1))
    s = (s,s,c)[:imgs[0].ndim]
    mins = [i[s].min(axis=(0,1)) for i in imgs]
    maxs = [i[s].max(axis=(0,1)) for i in imgs]
    mins = np.array(mins).reshape((len(mins),-1))
    maxs = np.array(maxs).reshape((len(maxs),-1))
    mins, maxs = mins.min(axis=0), maxs.max(axis=0)
    if np.iscomplexobj(mins):
        mins, maxs = np.zeros(mins.shape), np.abs(maxs)
    if chans!='all': return mins.min(), maxs.max()
    return [(i,j) for i,j in zip(mins, maxs)]

def histogram(imgs, rg=(0,256), slices='all', chans='all', step=1):
    c = chans if isinstance(chans, int) else slice(None)
    if isinstance(slices, int): imgs = [imgs[slices]]
    if step<=1: step = int(1/step+0.5)
    else: step = int(min(imgs[0].shape[:2])/step+0.5)
    s = slice(None, None, max(step,1))
    s = (s,s,c)[:imgs[0].ndim]
    rg = np.linspace(rg[0], rg[1], 257)
    hist = [np.histogram(i[s], rg)[0] for i in imgs]
    return np.sum(hist, axis=0)

class ImagePlus:
    """ImagePlus: a class to make operation more flexible """
    def __init__(self, imgs, title=None, is3d=False):
        self.set_title(title)
        self.snap = None
        self.cur = self.chan = 0
        self.dirty = True
        self.scrchanged = False
        self.roi = None
        self.mark = None
        self.msk = None
        self.mskmode = None
        self.lut = ColorManager.get_lut('grays')
        self.log = False
        
        self.tool = None
        self.data = {}
        self.unit = (1, 'pix')

        self.back = None
        self.chan_range = []
        self.chan_mode = 'min'
        self.set_imgs(imgs)

    def update(self): self.dirty = True
    
    def set_title(self, title):
        self.title = ImageManager.name(title)

    def set_imgs(self, imgs):
        self.is3d = not isinstance(imgs, list)
        self.scrchanged = True
        self.snap = None
        self.imgs = imgs

        self.size = self.imgs[0].shape[:2]
        self.height, self.width = self.size
        self.imgtype = get_img_type(self.imgs)
        if self.imgs[0].ndim==2: self.channels = 1
        else: self.channels = self.imgs[0].shape[2]
        self.dtype = self.imgs[0].dtype
        if self.dtype == np.uint8: self.range = (0, 255)
        else: self.range = self.get_updown('all', 'one', step=512)
        if self.dtype == np.uint8:
            self.chan_range = [(0, 255)] * self.channels
        else: self.chan_range = self.get_updown('all', 'all', step=512)
        self.chan = (0, [0,1,2])[self.channels==3]

    def get_updown(self, slices='all', chans='one', step=1):
        if slices is None: slices = self.cur
        if chans is None: chans = self.chan
        return get_updown(self.imgs, slices, chans, step)

    def histogram(self, rg=None, slices=None, chans=None, step=1):
        if slices is None: slices = self.cur
        if chans is None: chans = self.chan
        if rg is None: rg = self.range
        return histogram(self.imgs, rg, slices, chans, step)

    def get_imgtype(self):return self.imgtype

    def get_nslices(self):return len(self.imgs)

    def get_nchannels(self):return self.channels

    def set_cur(self, n):
        if n>=0 and n<len(self.imgs):self.cur=n

    def get_nbytes(self):
        return self.imgs[0].nbytes * len(self.imgs)

    @property
    def img(self):return self.imgs[self.cur]

    @property
    def range(self):
        rg = np.array(self.chan_range).reshape((-1,2))
        return (rg[:,0].min(), rg[:,1].max())

    @range.setter
    def range(self, value):
        self.chan_range = [value] * len(self.chan_range)

    def get_msk(self, mode='in'):
        if self.roi==None:return None
        if self.msk is None:
            self.msk = np.zeros(self.size, dtype=np.bool)
        if self.roi.update or mode!=self.mskmode:
            self.msk[:] = 0
            if isinstance(mode, int):
                self.roi.sketch(self.msk, w=mode, color=True)
            else: self.roi.fill(self.msk, color=True)
            if mode=='out':self.msk^=True
            self.roi.update = False
            self.mskmode=mode
        return self.msk

    def get_rect(self):
        if self.roi==None:return slice(None), slice(None)
        box = self.roi.get_box()
        l, r = max(0, int(box[0])), min(self.size[1], int(box[2]))
        t, b = max(0, int(box[1])), min(self.size[0], int(box[3]))
        return slice(t,b), slice(l,r)

    def get_subimg(self, s1=None, s2=None):
        if s1==None:
            s = self.get_rect()
            if s==None:return self.img
        return self.img[s[0], s[1]]

    def snapshot(self):
        if self.snap is None:
            self.snap = self.img.copy()
        else: self.snap[...] = self.img

    def reset(self, msk=False):
        if not self.snap is None:
            if msk and not self.get_msk('out') is None:
                msk = self.get_msk('out')
                self.imgs[self.cur][msk] = self.snap[msk]
            else : self.imgs[self.cur][:] = self.snap

    def lookup(self, img=None):
        if img is None: img = self.img
        if isinstance(self.chan, int):
            rg = self.chan_range[self.chan]
            k = 255.0/(max(1e-10, rg[1]-rg[0]))
            bf = np.clip(img, rg[0], rg[1])
            np.subtract(bf, rg[0], out=bf, casting='unsafe')
            np.multiply(bf, k, out=bf, casting='unsafe')
            return self.lut[bf.astype(np.uint8)]
        rgb = np.zeros(img.shape[:2]+(3,), dtype=np.uint8)
        for i in (0,1,2):
            rg = self.chan_range[self.chan[i]]
            k = 255.0/(max(1e-10, rg[1]-rg[0]))
            bf = np.clip(img[:,:,self.chan[i]], rg[0], rg[1])
            np.subtract(bf, rg[0], out=bf, casting='unsafe')
            np.multiply(bf, k, out=rgb[:,:,i], casting='unsafe')
        return rgb


    def swap(self):
        if self.snap is None:return
        if isinstance(self.imgs, list):
            self.snap, self.imgs[self.cur] = self.imgs[self.cur], self.snap
        else:
            buf = self.img.copy()
            self.img[:], self.snap[:] = self.snap, buf
    
    def __del__(self):
        print(self.title, '>>> delete ips')

if __name__=='__main__':
    from skimage.io import imread
    img = imread('results.bmp')
    ips = ImagePlus([img, 255-img])

    from ui.canvasframe import CanvasFrame
    import wx

    app = wx.PySimpleApp()
    frame = CanvasFrame()
    frame.set_ips(ips)
    frame.Show()
    app.MainLoop()