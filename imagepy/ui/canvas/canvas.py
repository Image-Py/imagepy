import wx, numpy as np
from .boxutil import cross, multiply, lay, mat
from .imutil import mix_img
from .mark import drawmark
from time import time

class Canvas (wx.Panel):
    scales = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 8, 10, 15, 20, 30, 50]
    
    def __init__(self, parent, autofit=False):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL )
        self.img = None
        self.back = None
        self.mode = 'set'

        self.winbox = None
        self.conbox = None
        self.oribox = None
        
        self.outbak = None
        self.outimg = None
        self.outrgb = None
        self.outbmp = None
        self.outint = None

        self.buffer = None
        
        lut = np.arange(256*3)//3
        lut.shape = (256,3)
        lut = lut.astype(np.uint8)

        self.lut = lut
        self.rg = (0, 255)
        self.cn = 0
        self.log = False

        self._lut = lut
        self._rg = (0, 255)
        self._cn = 0
        self._log = False

        self.marks = {}
        
        self.scaidx = 6
        self.autofit = autofit
        self.scrbox = wx.DisplaySize()
        self.bindEvents()

    def bindEvents(self):
        for event, handler in [ \
                (wx.EVT_SIZE, self.on_size),
                (wx.EVT_MOUSE_EVENTS, self.on_mouseevent),
                (wx.EVT_IDLE, self.on_idle),
                (wx.EVT_PAINT, self.on_paint)]:
            self.Bind(event, handler)

    def on_mouseevent(self, me):
        if me.ButtonDown():
            if me.GetButton()==1:
                self.oldxy = me.GetX(), me.GetY()
            if me.GetButton()==3:
                self.fit()
        wheel = np.sign(me.GetWheelRotation())
        if wheel!=0:
            if wheel == 1:
                self.zoomout(me.GetX(), me.GetY())
            if wheel == -1:
                self.zoomin(me.GetX(), me.GetY())
        if me.Dragging():
            x, y = self.oldxy
            self.move(me.GetX()-x, me.GetY()-y)
            self.oldxy = me.GetX(), me.GetY()
            
    def initBuffer(self):
        box = self.GetClientSize()
        self.buffer = wx.Bitmap(*box)
        self.winbox = [0, 0, *box]

    def fit(self):
        oriw = self.oribox[2]-self.oribox[0]
        orih = self.oribox[3]-self.oribox[1]
        if not self.autofit: a,b,c,d = self.winbox
        else: 
            (a,b),(c,d) = (0,0), self.scrbox
            c, d = c*0.9, d*0.9
        for i in self.scales[6::-1]:
            if oriw*i<c-a and orih*i<d-b: break
        self.scaidx = self.scales.index(i)
        self.zoom(i, 0, 0)
        self.update()

    def set_img(self, img):
        self.img = img
        shp = list(img.shape[1::-1])
        if self.oribox and self.oribox[2:] == shp: return
        self.conbox = [0, 0, *shp]
        self.oribox = [0, 0, *shp]
        
        #if self.conbox is None: self.fit()

    def set_back(self, back): 
        self.back = back

    def set_log(self, log, b=False):
        if b: self._log = log
        else: self.log = log
        
    def set_rg(self, rg, b=False):
        if b: self._rg = rg
        else: self.rg = rg
    
    def set_lut(self, lut, b=False):
        if b: self._lut = lut
        else: self.lut = lut

    def set_cn(self, cn, b=False):
        if b: self._cn = cn
        else: self.cn = cn

    def set_mode(self, mode): self.mode = mode

    @property
    def scale(self):
        conw = self.conbox[2]-self.conbox[0]
        oriw = self.oribox[2]-self.oribox[0]
        conh = self.conbox[3]-self.conbox[1]
        orih = self.oribox[3]-self.oribox[1]
        l1, l2 = conw**2+conh**2, oriw**2+orih**2
        return l1**0.5 / l2**0.5

    def move(self, dx, dy):
        arr = np.array(self.conbox)
        arr = arr.reshape((2,2))+(dx, dy)
        self.conbox = arr.ravel().tolist()
        self.update()

    def on_size(self, event):
        if self.img is None: return
        self.initBuffer()
        self.update()

    def on_idle(self, event):pass

    def on_paint(self, event):
        if self.buffer is None: return
        wx.BufferedPaintDC(self, self.buffer)

    def draw_image(self, dc, img, back, mode):
        out, bak, rgb = self.outimg, self.outbak, self.outrgb
        csbox = cross(self.winbox, self.conbox)
        shp = csbox[3]-csbox[1], csbox[2]-csbox[0]
        o, m = mat(self.oribox, self.conbox, csbox)
        shp = tuple(np.array(shp).round().astype(np.int))
        if out is None or (out.shape, out.dtype) != (shp, img.dtype):
            self.outimg = np.zeros(shp, dtype=img.dtype)
        if not back is None and (
            bak is None or (bak.shape, bak.dtype) != (shp, back.dtype)):
            self.outbak = np.zeros(shp, dtype=back.dtype)
        if rgb is None or rgb.shape[:2] != shp:
            self.outrgb = np.zeros(shp+(3,), dtype=np.uint8)
            self.outint = np.zeros(shp, dtype=np.uint8)
            buf = memoryview(self.outrgb)
            self.outbmp = wx.Bitmap.FromBuffer(*shp[::-1], buf)
        
        #if not back is None: print('has back image')
        mix_img(back, m, o, shp, self.outbak, 
              self.outrgb, self.outint, self._rg,
                self._lut, self._log, cns=self._cn, mode='set')
        
        mix_img(self.img, m, o, shp, self.outimg,
              self.outrgb, self.outint, self.rg,
                self.lut, self.log, cns=self.cn, mode=self.mode)
        self.outbmp.CopyFromBuffer(memoryview(self.outrgb))
        dc.DrawBitmap(self.outbmp, *csbox[:2])
        
    def update(self, counter = [0,0]):
        counter[0] += 1
        start = time()
        lay(self.winbox, self.conbox)
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.Clear()
        self.draw_image(dc, self.img, self.back, 0)
        for i in self.marks:
            if self.marks[i] is None: continue
            if callable(self.marks[i]):
                self.marks[i](dc, self.to_panel_coor, k = self.scale)
            else:
                drawmark(dc, self.to_panel_coor, self.marks[i], k=self.scale)
        dc.UnMask()
        counter[1] += time()-start
        if counter[0] == 10:
            print('frame rate:',int(10/max(0.001,counter[1])))
            counter[0] = counter[1] = 0
        
    def center(self, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
        dx = (self.winbox[2]-self.winbox[0])/2 - x
        dy = (self.winbox[3]-self.winbox[1])/2 - y
        for i,j in zip((0,1,2,3),(dx,dy,dx,dy)):
            self.conbox[i] += j
        lay(self.winbox, self.conbox)
        
    def zoom(self, k, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
        box = np.array(self.conbox).reshape((2,2))
        box = (box - (x,y)) / self.scale * k + (x, y)
        self.conbox = box.ravel().tolist()
        lay(self.winbox, self.conbox)
        if not self.autofit: return
        a,b,c,d = self.conbox
        if c-a<self.scrbox[0]*0.9 and d-b<self.scrbox[1]*0.9:
            self.SetInitialSize((c-a+4, d-b+4))
        
    def zoomout(self, x, y, coord='win', grade=True):
        self.scaidx = min(self.scaidx + 1, len(self.scales)-1)
        self.zoom(self.scales[self.scaidx], x, y, coord)
        self.update()

    def zoomin(self, x, y, coord='win'):
        self.scaidx = max(self.scaidx - 1, 0)
        self.zoom(self.scales[self.scaidx], x, y, coord)
        self.update()

    def to_data_coor(self, x, y):
        x = (x - self.conbox[0])/self.scale
        y = (y - self.conbox[1])/self.scale
        return x, y

    def to_panel_coor(self, x, y):
        x = x * self.scale + self.conbox[0]
        y = y * self.scale + self.conbox[1]
        return x, y

    def __del__(self):
        self.img = self.back = None
        print('========== canvas del')

if __name__=='__main__':
    from skimage.data import astronaut, camera
    from numpy.fft import fft2, ifft2, fftshift, ifftshift
    import matplotlib.pyplot as plt

    img = camera()
    img = fftshift(fft2(img))
    farr = img.view(dtype=np.float64)
    #a = farr.reshape((512,2,512)).transpose(0,2,1)
    # farr.shape = img.shape+(-1,)
    #plt.imshow(np.log(np.abs(a[:,:,1])))
    #plt.show()
    
    app = wx.App()
    frame = wx.Frame(None)
    canvas = Canvas(frame)
    
    canvas.set_img(img)
    # canvas.set_rg((-128, 127))
    canvas.set_rg((0,31015306))
    canvas.set_cn(0)
    canvas.set_log(True)
    frame.Show(True)
    frame.SetSize(512,512)
    app.MainLoop()
