import numpy as np

default_lut = np.arange(256*3, dtype=np.uint8).reshape((3,-1)).T

def get_updown(imgs, slices='all', chans='all', step=1):
    c = chans if isinstance(chans, int) else slice(None)
    if isinstance(slices, int): imgs = [imgs[slices]]
    if step<=1: step = int(1/step+0.5)
    else: step = int(min(imgs[0].shape[:2])/step+0.5)
    s = slice(None, None, max(step, 1))
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

def lookup(img, cn, rgs, lut):
    if isinstance(cn, int): cn = [cn]
    img = img.reshape(img.shape[:2]+(-1,))
    buf = np.zeros(img.shape[:2]+(len(cn),), dtype=np.uint8)
    for i in range(len(cn)):
        rg = rgs[cn[i]]
        k = 255.0/(max(1e-10, rg[1]-rg[0]))
        bf = np.clip(img[:,:,cn[i]], rg[0], rg[1])
        np.subtract(bf, rg[0], out=bf, casting='unsafe')
        np.multiply(bf, k, out=buf[:,:,i], casting='unsafe')
    return buf if len(cn)==3 else lut[buf.reshape(img.shape[:2])]

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

class Image:
    def __init__(self, imgs=None, name='Image'):
        self.name = name
        self.cur = 0
        self.rg = [(0, 255)]
        self.set_imgs(imgs)
        self.roi = None
        self.mark = None
        self.unit = 1, 'pix'
        self.msk = None
        self.pos = (0,0)
        self.cn = 0
        
        self.lut = default_lut
        self.log = False
        self.mode = 'set'
        self.dirty = False
        self.snap = None
        self.back = None
        self.tool = None
        self.data = {}

    @property
    def box(self):
        (x, y), (h, w) = self.pos, self.shape
        return [x, y, x+w, y+h]
    
    @property
    def title(self): return self.name
    
    @property
    def img(self): return self.imgs[self.cur]

    @img.setter
    def img(self, value): 
        self.imgs[self.cur] = value
        self.reset()
        
    def set_imgs(self, imgs):
        self.imgs = [imgs] if imgs is None else imgs
        if not imgs is None: self.reset()

    @property
    def channels(self):
        if self.img.ndim==2: return 1
        else: return self.img.shape[2]

    @property
    def slices(self): return len(self.imgs)

    @property
    def isarray(self): return isinstance(self.imgs, np.ndarray)

    @property
    def nbytes(self):
        return sum([i.nbytes for i in self.imgs])

    @property
    def dtype(self): return self.img.dtype

    @property
    def shape(self): return self.img.shape[:2]

    @property
    def info(self):
        return '%s  %sx%s  S:%s/%s  C:%s/%s  %.2fM'%(str(self.dtype).upper(), *self.shape,
            self.cur+1, self.slices, self.cn, self.channels, self.nbytes/1024/1024)

    @property
    def range(self):
        rg = np.array(self.rg).reshape((-1,2))
        return (rg[:,0].min(), rg[:,1].max())

    @range.setter
    def range(self, value):
        self.rg = [value] * len(self.rg)

    def mask(self, mode='in'):
        if self.roi==None: return None
        if self.roi.msk != mode:
            self.msk = self.roi.to_mask(self.shape, mode)
        return self.msk    

    @property
    def rect(self):
        if self.roi is None: return slice(None), slice(None)
        box, shape = self.roi.box, self.shape
        l, r = max(0, int(box[0])), min(shape[1], int(box[2]))
        t, b = max(0, int(box[1])), min(shape[0], int(box[3]))
        return slice(t,b), slice(l,r)

    def subimg(self, s1=None, s2=None):
        s1 = s1 or self.rect[0]
        s2 = s2 or self.rect[1]
        if self.isarray: return self.imgs[s1, s2]
        else: return [i[s1, s2] for i in self.imgs]

    def update(self): self.dirty = True

    def reset(self):
        self.cn = [0, [0,1,2]][self.channels==3]
        if self.dtype == np.uint8: 
            self.rg = [(0, 255)] * self.channels
        else: 
            self.rg = self.get_updown('all', 'all', step=512)

    def snapshot(self):
        dif = self.snap is None
        dif = dif or self.snap.shape != self.img.shape
        dif = dif or self.snap.dtype != self.img.dtype
        if dif: self.snap = self.img.copy()
        else: self.snap[:] = self.img

    def swap(self):
        if self.snap is None:return
        buf = self.img.copy()
        self.img[:], self.snap[:] = self.snap, buf

    def histogram(self, rg=None, slices=None, chans=None, step=1):
        if slices is None: slices = self.cur
        if chans is None: chans = self.cn
        if rg is None: rg = self.range
        return histogram(self.imgs, rg, slices, chans, step)

    def get_updown(self, slices='all', chans='all', step=512):
        if slices is None: slices = self.cur
        if chans is None: chans = self.cn
        return get_updown(self.imgs, slices, chans, step)

    def lookup(self, img=None):
        if img is None: img = self.img
        return lookup(img, self.cn, self.rg, self.lut)

if __name__ == '__main__':
    img = Image(np.zeros((5,5)))
