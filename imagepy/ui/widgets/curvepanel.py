import wx
import numpy as np
from numpy.linalg import norm
from scipy import interpolate

class CurvePanel(wx.Panel):
    """ HistCanvas: diverid from wx.core.Panel """
    def __init__(self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size(281,281), 
                            style = wx.TAB_TRAVERSAL )
        self.init_buf()
        self.offset = (20,5)
        self.idx = -1
        self.his = None
        self.update = False
        self.pts = [(0,0), (255,255)]
        self.Bind(wx.EVT_SIZE, self.on_size)  
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_ld)
        self.Bind( wx.EVT_LEFT_UP, self.on_lu )
        self.Bind( wx.EVT_MOTION, self.on_mv )
        self.Bind( wx.EVT_RIGHT_DOWN, self.on_rd )
        self.handle = self.handle_

    def init_buf(self):
        box = self.GetClientSize()
        self.buffer = wx.Bitmap(box.width, box.height)
        
    def on_size(self, event):
        self.init_buf()
        self.update = True
        
    def on_idle(self, event):
        if self.update == True:
            self.draw()
            self.update = False

    def pick(self, x, y):
        dis = norm(np.array(self.pts)-(x,y), axis=1)
        if dis[np.argmin(dis)] > 3: return -1
        return np.argmin(dis)

    def on_ld(self, event):
        x,y = event.GetX()-self.offset[0], event.GetY()-self.offset[1]
        self.idx = self.pick(x, 255-y)
        if self.idx==-1: 
            self.pts.append((x, 255-y))
            self.idx = len(self.pts)-1
            self.update = True

    def on_lu(self, event):
        self.idx = -1

    def on_rd(self, event):
        x,y = event.GetX()-self.offset[0], event.GetY()-self.offset[1]
        self.idx = self.pick(x, 255-y)
        print(self.idx)
        if not self.pts[self.idx][0] in (0, 255):
            del self.pts[self.idx]
            self.idx = -1
            self.update = True

    def on_mv(self, event):
        x,y = event.GetX()-self.offset[0], event.GetY()-self.offset[1]
        if self.pick(x, 255-y)!=-1:
            self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        else: self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        if self.idx!=-1:
            oldx = self.pts[self.idx][0]
            if oldx == 0: x=0
            elif oldx==255: x=255
            else: x = np.clip(x, 1, 254)
            y = np.clip(y, 0, 255)
            self.pts[self.idx] = (x, 255-y)
            self.update = True
        

    def on_paint(self, event):
        wx.BufferedPaintDC(self, self.buffer)
        
    def set_hist(self, hist):
        self.hist = (hist*256/hist.max()).astype(np.uint8)
        self.update = True
        
    def set_pts(self, pts):
        self.x1, self.x2 = x1, x2
        self.update = True        

    def draw(self):
        if self.hist is None:
            return
        ox, oy = self.offset
        # get client device context buffer
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.Clear()
        # w, h = self.GetClientSize()
        
        # the main draw process 
        dc.SetPen(wx.Pen((100,100,100), width=1, style=wx.SOLID))        
        for i in range(256):
            dc.DrawLine(i+ox,256+oy,i+ox,256-self.hist[i]+oy)
        ys = self.GetValue()
        if ys is None:return
        dc.SetBrush(wx.Brush((0,0,0)))
        dc.SetPen(wx.Pen((0,0,0), width=1))
        for i in self.pts: dc.DrawCircle(i[0]+ox, 255-i[1]+oy, 2)
        dc.DrawPointList(list(zip(np.arange(256)+ox, 255-ys+oy)))

        dc.SetPen(wx.Pen((0,0,0), width=1, style=wx.SOLID))
        for i in range(0,257, 64):
            dc.DrawLine(0+ox, i+oy, 256+ox, i+oy)
            dc.DrawLine(i+ox, 0+oy, i+ox, 256+oy)
        dc.SetBrush(wx.Brush((0,0,0), wx.BRUSHSTYLE_TRANSPARENT))
        arr = np.zeros((10,256,3),dtype=np.uint8)
        arr[:] = np.vstack([np.arange(256)]*3).T
        bmp = wx.Bitmap.FromBuffer(256,10, memoryview(arr))
        dc.DrawBitmap(bmp, 0+ox, 260+oy)
        dc.DrawRectangle(0+ox, 260+oy, 256, 10)
        arr = arr.transpose((1,2,0))[::-1].copy()
        bmp = wx.Bitmap.FromBuffer(10, 256, memoryview(arr))
        dc.DrawBitmap(bmp, -15+ox, 0+oy)
        dc.DrawRectangle(-15+ox, 0+oy, 10, 256)
        
    def handle_(self, key):pass
    
    def set_handle(self, handle):self.handle = handle

    def SetValue(self, value):pass


    def GetValue(self):
        kind = 'linear' if len(self.pts)==2 else 'quadratic'
        x, y = np.array(self.pts).T
        try:
            f = interpolate.interp1d(x, y, kind=kind)
        except: return None
        return np.clip(f(np.arange(256)), 0, 255)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    hist = CurvePanel(frame)
    frame.Fit()
    frame.Show(True)
    hist.set_hist(np.random.rand(256)+2)
    app.MainLoop() 