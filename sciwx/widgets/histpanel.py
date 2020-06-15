import wx
import numpy as np

class HistPanel(wx.Panel):
    """ HistCanvas: diverid from wx.core.Panel """
    def __init__(self, parent, hist=None, size=(256, 80), app=None):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = (size[0], size[1]+1), 
                            style = wx.TAB_TRAVERSAL )
        self.init_buf()
        self.hist = None
        self.w, self.h = size
        if not hist is None: self.SetValue(hist)
        self.dirty = False
        self.x1, self.x2 = 0, self.w-1
        self.Bind(wx.EVT_SIZE, self.on_size)  
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        # self.Bind = lambda z, x:0 

    def update(self): self.dirty = True

    def init_buf(self):
        box = self.GetClientSize()
        if min(box)==0: return
        self.buffer = wx.Bitmap(box.width, box.height)
        
    def on_size(self, event):
        self.init_buf()
        self.update()
        
    def on_idle(self, event):
        if self.dirty == True:
            self.draw()
            self.dirty = False
            
    def on_paint(self, event):
        wx.BufferedPaintDC(self, self.buffer)
        
    def SetValue(self, hist):
        self.hist = (hist*self.h/hist.max())
        self.logh = (np.log(self.hist+1.0))*(self.h/(np.log(self.h+1)))
        self.update()
        
    def set_lim(self, x1, x2):
        self.x1, self.x2 = x1, x2
        self.update()
        
    def draw(self):        
        # get client device context buffer
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.Clear()
        # w, h = self.GetClientSize()
    
        # the main draw process 
           
        if not self.hist is None:
            hist = self.hist[np.linspace(0, len(self.hist)-1, self.w, dtype=np.int16)]
            dc.SetPen(wx.Pen((200,200,200), width=1, style=wx.SOLID)) 
            for i in range(self.w):
                dc.DrawLine(i,self.h,i,self.h-self.logh[i])
            dc.SetPen(wx.Pen((100,100,100), width=1, style=wx.SOLID)) 
            for i in range(self.w):
                dc.DrawLine(i,self.h,i,self.h-self.hist[i])            
        dc.SetPen(wx.Pen((0,0,0), width=1, style=wx.SOLID))
        dc.DrawLine(self.x1, self.h, self.x2, 0)
        dc.DrawLines([(0,0),(self.w-1,0),(self.w-1,self.h),(0,self.h),(0,0)])

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    hist = HistPanel(frame)
    hist.SetValue(np.random.rand(256))
    frame.Fit()
    frame.Show(True)
    app.MainLoop() 
