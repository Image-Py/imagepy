from __future__ import absolute_import
from __future__ import print_function
import numpy as np
from .core.manager import WindowsManager, ColorManager

def get_img_type(imgs):
    if imgs[0].ndim==3 and imgs[0].dtype==np.uint8:return 'rgb'
    if imgs[0].dtype == np.uint8:return '8-bit'
    if imgs[0].dtype == np.uint16:return '16-bit'
    if imgs[0].dtype == np.int32:return '32-int'
    if imgs[0].dtype == np.float32:return '32-float'
    if imgs[0].dtype == np.float64:return '64-float'

class ImagePlus:
    """ImagePlus: a class to make operation more flexible """
    def __init__(self, imgs, title=None, is3d=False):
        self.set_title(title)
        self.snap = None
        self.cur = 0
        self.update = False
        self.scrchanged = False
        self.roi = None
        self.mark = None
        self.msk = None
        self.mskmode = None
        self.lut = ColorManager.get_lut('grays')
        self.backimg = None
        self.backmode = (0.5, 'Mean')
        self.tool = None
        self.data = None
        self.info = {}
        self.unit = (1, 'pix')
        self.range = (0, 255)
        self.set_imgs(imgs)

    def set_title(self, title):
        self.title = WindowsManager.name(title)

    def set_imgs(self, imgs):
        self.is3d = not isinstance(imgs, list)
        self.scrchanged = True
        self.snap = None
        self.imgs = imgs

        self.height, self.width = self.size = self.imgs[0].shape[:2]
        print(self.height, self.width)
        self.imgtype = get_img_type(self.imgs)
        self.channels = 1 if self.imgs[0].ndim==2 else self.imgs[0].shape[2]
        self.dtype = self.imgs[0].dtype

        if self.dtype == np.uint8:
            self.range = (0, 255)
        else: self.range = self.get_updown()

    def get_updown(self):
        arr = np.array(([(i.min(),i.max()) for i in self.imgs]))
        return arr[:,0].min(), arr[:,1].max()

    def get_imgtype(self):return self.imgtype

    def get_nslices(self):return len(self.imgs)

    def get_nchannels(self):return self.channels

    def set_cur(self, n):
        if n>=0 and n<len(self.imgs):self.cur=n

    def get_nbytes(self):
        return self.imgs[0].nbytes * len(self.imgs)

    @property
    def img(self):return self.imgs[self.cur]

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
        l, r = max(0, box[0]), min(self.size[1], box[2])
        t, b = max(0, box[1]), min(self.size[0], box[3])
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

    def histogram(self, arange=None, stack=False):
        if arange == None: arange=self.range
        if not stack:
            return np.histogram(self.img, np.linspace(arange[0], arange[1]+1, 257))[0]
        # if stack
        hists = []
        for i in self.imgs:
            hists.append(np.histogram(i, np.linspace(arange[0], arange[1]+1, 257))[0])
        return np.array(hists).sum(axis=0)

    def lookup(self, img=None):
        if img is None: img = self.img
        #print(self.channels, self.dtype, img.dtype)
        #if img.ndim==2 and img.dtype==np.uint8:
        #    return self.lut[img]
        #el
        if img.ndim==2:
            k = 255.0/(max(1, self.range[1]-self.range[0]))
            bf = np.clip(img, self.range[0], self.range[1])
            bf = ((bf - self.range[0]) * k).astype(np.uint8)
            #print(bf.max(), self.range)
            return self.lut[bf]
        if img.ndim==3 and self.dtype==np.uint8:
            return img

    def swap(self):
        if self.snap is None:return
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