import wx
import numpy as np

class HistCanvas(wx.Panel):
    """ HistCanvas: diverid from wx.core.Panel """
    def __init__(self, parent, hist=None):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size(256,81), 
                            style = wx.TAB_TRAVERSAL )
        self.init_buf()
        self.hist = None
        if not hist is None: self.SetValue(hist)
        self.dirty = False
        self.x1, self.x2 = 0, 255
        self.Bind(wx.EVT_SIZE, self.on_size)  
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind = lambda z, x:0 

    def update(self): self.dirty = True

    def init_buf(self):
        box = self.GetClientSize()
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
        self.hist = (hist*80.0/hist.max())
        self.logh = (np.log(self.hist+1.0))*(80/(np.log(81)))
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
        print("drawing histogram")
           
        if not self.hist is None:
            dc.SetPen(wx.Pen((200,200,200), width=1, style=wx.SOLID)) 
            for i in range(256):
                dc.DrawLine(i,80,i,80-self.logh[i])
            dc.SetPen(wx.Pen((100,100,100), width=1, style=wx.SOLID)) 
            for i in range(256):
                dc.DrawLine(i,80,i,80-self.hist[i])            
        dc.SetPen(wx.Pen((0,0,0), width=1, style=wx.SOLID))
        dc.DrawLine(self.x1, 80, self.x2, 0)
        dc.DrawLines([(0,0),(255,0),(255,80),(0,80),(0,0)])