import wx, sys
import numpy as np
from numpy.linalg import norm
from scipy import interpolate

if sys.version_info[0]==2:memoryview=np.getbuffer

class CMapPanel(wx.Panel):
    """ HistCanvas: diverid from wx.core.Panel """
    def __init__(self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size(255,30), 
                            style = wx.TAB_TRAVERSAL )
        self.init_buf()
        self.offset = (0,0)
        self.cmap = np.vstack([np.arange(256)]*3).T.astype(np.uint8)
        self.idx = -1
        self.his = None
        self.update = False
        self.pts = [(0,0,0,0), (255,255,255,255)]
        self.Bind(wx.EVT_SIZE, self.on_size)  
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_ld)
        self.Bind( wx.EVT_LEFT_UP, self.on_lu )
        self.Bind( wx.EVT_MOTION, self.on_mv )
        self.Bind( wx.EVT_RIGHT_DOWN, self.on_rd )
        self.Bind( wx.EVT_LEFT_DCLICK, self.on_rdc )
        self.handle = self.handle_

    def init_buf(self):
        box = self.GetClientSize()
        self.buffer = wx.Bitmap(box.width, box.height)
        
    @classmethod
    def linear_color(cls, cs):
        cs = sorted(cs)
        cmap = np.vstack([np.arange(256)]*3).T
        for i in range(1, len(cs)):
            c1, c2 = cs[i-1][1:], cs[i][1:]
            rs, gs, bs = [np.linspace(c1[j], c2[j], cs[i][0]-cs[i-1][0]+1) for j in (0,1,2)]
            cmap[cs[i-1][0]:cs[i][0]+1] = np.array((rs, gs, bs)).T
        return cmap.astype(np.uint8)

    def on_size(self, event):
        self.init_buf()
        self.update = True
        
    def on_idle(self, event):
        if self.update == True:
            self.draw()
            self.update = False

    def pick(self, x, y):
        if abs(y-10)>3:return -1
        dis = np.abs(np.array(self.pts)[:,0]-x)
        if dis.min() > 3: return -1
        return np.argmin(dis)

    def on_ld(self, event):
        x,y = event.GetX()-self.offset[0], event.GetY()-self.offset[1]
        if abs(y-7)>8:return -1
        self.idx = self.pick(x, y)
        if self.idx==-1: 
            self.pts.append((x,)+tuple(self.cmap[x]))
            self.idx = len(self.pts)-1
            self.cmap[:] = self.linear_color(self.pts)
            self.update = True
            self.handle()

    def on_lu(self, event):
        self.idx = -1

    def on_rd(self, event):
        x,y = event.GetX()-self.offset[0], event.GetY()-self.offset[1]
        self.idx = self.pick(x, y)
        if self.idx==-1:return
        if not self.pts[self.idx][0] in (0, 255):
            del self.pts[self.idx]
            self.idx = -1
            self.cmap[:] = self.linear_color(self.pts)
            self.update = True
            self.handle()

    def on_rdc(self, event):
        x,y = event.GetX()-self.offset[0], event.GetY()-self.offset[1]
        self.idx = self.pick(x, y)
        if self.idx==-1:return
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            rst = dlg.GetColourData().GetColour()
            x = self.pts[self.idx][0]
            self.pts[self.idx] = (x,)+rst[:-1]
            self.idx=-1
            self.cmap[:] = self.linear_color(self.pts)
            self.update = True
        dlg.Destroy()
        self.handle()


    def on_mv(self, event):
        x,y = event.GetX()-self.offset[0], event.GetY()-self.offset[1]
        if self.pick(x, y)!=-1:
            self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        else: self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        if self.idx!=-1:
            oldx = self.pts[self.idx][0]
            if oldx == 0: x=0
            elif oldx==255: x=255
            else: x = np.clip(x, 1, 254)
            cl = self.pts[self.idx][1:]
            self.pts[self.idx] = (x,)+cl
            self.cmap[:] = self.linear_color(self.pts)
            self.update = True
            self.handle()
        

    def on_paint(self, event):
        wx.BufferedPaintDC(self, self.buffer)
        
    def set_hist(self, hist):
        self.hist = (hist*255/hist.max()).astype(np.uint8)
        self.update = True
        
    def set_pts(self, pts):
        self.x1, self.x2 = x1, x2
        self.update = True        

    def draw(self):
        ox, oy = self.offset
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.Clear()
        dc.SetPen(wx.Pen((100,100,100), width=1, style=wx.SOLID))  
        dc.SetBrush(wx.Brush((0,0,0), wx.BRUSHSTYLE_TRANSPARENT))
        arr = np.zeros((10,256,3),dtype=np.uint8)
        arr[:] = self.cmap
        bmp = wx.Bitmap.FromBuffer(256,10, memoryview(arr))
        dc.DrawBitmap(bmp, 0+ox, 0+oy)
        dc.DrawRectangle(0+ox, 0+oy, 256, 10)
        poly = np.array([(0,0),(-5,5),(5,5),(0,0)])
        polys = [poly+(ox+i[0],oy+10) for i in self.pts]
        brushes = [wx.Brush(i[1:]) for i in self.pts]
        dc.DrawPolygonList(polys,brushes=brushes)

        
    def handle_(self):pass
    
    def set_handle(self, handle):self.handle = handle

    def SetValue(self, value):pass

    def GetValue(self): return sorted(self.pts)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    hist = CMapPanel(frame)
    frame.Fit()
    frame.Show(True)
    hist.set_hist(np.random.rand(256)+2)
    app.MainLoop() 