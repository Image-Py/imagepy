import numpy as np
from time import time
from sciapp.object import Image

def get_img_type(imgs):
    if imgs[0].ndim==3 and imgs[0].dtype==np.uint8:return 'rgb'
    if imgs[0].dtype == np.uint8:return '8-bit'
    if imgs[0].dtype == np.uint16:return '16-bit'
    if imgs[0].dtype == np.int32:return '32-int'
    if imgs[0].dtype == np.float32:return '32-float'
    if imgs[0].dtype == np.float64:return '64-float'
    if imgs[0].dtype == np.complex128:return '128-complex'
    if imgs[0].dtype == np.complex64:return '64-complex'

class ImagePlus(Image):
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

    @property
    def itype(self):
        return get_img_type(self.imgs[0])

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

    def reset(self, msk=False):
        if not self.snap is None:
            if msk and not self.get_msk('out') is None:
                msk = self.get_msk('out')
                self.imgs[self.cur][msk] = self.snap[msk]
            else : self.imgs[self.cur][:] = self.snap
    
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