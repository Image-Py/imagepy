# -*- coding: utf-8 -*-
import os,wx 
from .. import IPy, root_dir
import numpy as np
from math import ceil
from ..core.manager import PlotManager

class LineCanvas(wx.Panel):
    """LineCanvas: derived from wx.core.Panel"""
    def __init__(self, parent):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size(256,80), 
                            style = wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
        self.init_buf()
        self.data, self.extent = [], [0,0,1,1]
        self.set_title_label('Graph', 'X-unit', 'Y-unit')
        self.dirty = False
        
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_MOTION, self.on_move )

    def update(self):self.dirty = True

    def init_buf(self):
        box = self.GetClientSize()
        self.width, self.height = box.width, box.height
        self.buffer = wx.Bitmap(self.width, self.height)
        
    def on_size(self, event):
        self.init_buf()
        self.draw()
            
    def on_paint(self, event):
        wx.BufferedPaintDC(self, self.buffer)
        
    def trans(self, x, y):
        l, t, r, b = 35,35,15,35
        w = self.width - l - r
        h = self.height - t - b
        left, low, right, high = self.extent
        x = (x-l)*1.0/w*(right-left)+left
        y = (t+h-y)*1.0/(h)*(high-low)+low
        return x, y

    def clear(self):
        del self.data[:]

    def on_move(self, event):
        self.handle_move(*self.trans(event.x, event.y))

    def handle_move(self, x, y):pass

    def on_idle(self, event):
        if self.dirty == True:
            self.draw()
            self.dirty = False

    def set_title_label(self, title, labelx, labely):
        self.title, self.labelx, self.labely = title, labelx, labely

    def paint(self):
        if len(self.data)==0 :
            return
        ext = np.array([[x.min(), y.min(), x.max(), y.max()] for x,y,c,w in self.data])
        d = ext[:,3].max() - ext[:,1].min()
        top, bot = ext[:,3].max() + 0.1 * d, ext[:,1].min() - 0.1 * d
        if top == bot: top, bot = top+1, bot-1
        self.extent = [ext[:,0].min(), bot, ext[:,2].max(), top]
        self.update()

    def add_data(self, xs, ys=None, color=(0,0,255), lw=2):
        if ys is None:
            ys, xs = xs, np.arange(len(xs))
        self.data.append((xs, ys, color, lw))
        
    def draw_coord(self, dc, w, h, l, t, r, b):
        xs = [5, 10, 20, 40, 50, 100, 200, 400, 500, 1000, 2000, 4000, 10000]
        n, dx, dy = len(self.data), 0, 0
        left, low, right, high = self.extent
        for i in xs[::-1]: 
            if (right-left)*1.0/i<=10:dx=i
        for i in xs[::-1]: 
            if (high-low)*1.0/i<=10:dy=i
        dc.SetPen(wx.Pen((0, 0, 0), width=1, style=wx.SOLID))
        dc.DrawRectangle(l, t, w+1, h+1)
        dc.SetPen(wx.Pen((100, 100, 100), width=1, style=wx.SOLID))
        for i in range(int(ceil(left*1.0/dx)*dx), int(right)+1, dx):
            x = l+(i-left)*1.0/(right-left)*w
            dc.DrawLine(x, t, x, t+h)
            dc.DrawText(str(i), x-5, t+h)
        for i in range(int(ceil(low*1.0/dy)*dy), int(high)+1, dy):
            y = h+t-(i-low)*1.0/(high-low)*h
            dc.DrawLine(l, y, l+w, y)
            dc.DrawText(str(i), 5, y-5)

        titlefont = wx.Font(18, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dc.SetFont(titlefont)
        dw,dh = dc.GetTextExtent(self.title)
        dc.DrawText(self.title, l+w/2-dw/2, 3)
        
        lablelfont = wx.Font(14, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dc.SetFont(lablelfont)
        dw,dh = dc.GetTextExtent(self.labelx)
        dc.DrawText(self.labelx, l+w-dw, t+h+15)
        dc.DrawText(self.labely, 5, 10)

    def draw(self):
        l, t, r, b = 35,35,15,35
        w = self.width - l - r
        h = self.height - t - b
        if self.data is None:return
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.Clear()
        
        left, low, right, high = self.extent
        self.draw_coord(dc, w, h, l, t, r, b)
        for xs, ys, c, lw in self.data:
            ys = h+t - (ys - low)*(h/(high-low))
            xs = l+(xs-left)*(1.0/(right-left)*w)
            pts = list(zip(xs, ys))
            dc.SetPen(wx.Pen(c, width=lw, style=wx.SOLID))
            dc.DrawLines(pts)

    def save(self, path):
        self.buffer.SaveFile(path, wx.BITMAP_TYPE_PNG)
        

class PlotFrame ( wx.Frame ):
    """PlotFrame:derived from wx.core.Frame"""
    frms = {}

    @classmethod
    def get_frame(cls, title, gtitle='Graph', labelx='X-Unit', labely='Y-Unit'):
        if PlotManager.get(title) == None:
            PlotManager.add(cls(IPy.curapp, title))
            PlotManager.get(title).set_title_label(gtitle, labelx, labely)
        return PlotManager.get(title)

    def __init__( self, parent, title):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, 
                            title = title, pos = wx.DefaultPosition, 
                            size = wx.Size( 500,300 ) )
        self.title = title
        logopath = os.path.join(root_dir, 'data/logo.ico')
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.canvas = LineCanvas( self)
        #self.canvas.set_data(np.random.rand(256)*100)
        #self.canvas.set_lim(0, 0)
        sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 5 )
        sizer2 = wx.BoxSizer( wx.HORIZONTAL )
        self.lab_info = wx.StaticText( self, wx.ID_ANY, "Information", 
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_info.Wrap( -1 )
        sizer2.Add( self.lab_info, 0, wx.ALL, 5 )
        sizer2.AddStretchSpacer(1)
        self.btn_save = wx.Button( self, wx.ID_ANY, "Save", 
                                   wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer2.Add( self.btn_save, 0, wx.ALL, 5 )
        self.btn_cancel = wx.Button( self, wx.ID_ANY, "Cancel", 
                                     wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer2.Add( self.btn_cancel, 0, wx.ALL, 5 )
        sizer.Add( sizer2, 0, wx.ALL|wx.EXPAND, 5 )
        self.SetSizer( sizer )
        self.Layout()
        self.Centre( wx.BOTH )

        self.canvas.handle_move = self.handle_move
        self.Bind(wx.EVT_CLOSE, self.on_closing)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)

        self.set_title_label = self.canvas.set_title_label
        self.add_data = self.canvas.add_data
        self.clear = self.canvas.clear

    def draw(self):
        self.canvas.paint()
        self.Show()

    def handle_move(self, x, y):
        self.lab_info.SetLabel('X = %.1f, Y = %.1f' %(x, y))

    def on_cancel(self, event):
        self.Close()

    def on_save(self, event):
        para = {'path':'./'}
        filt = 'PNG files (*.png)|*.png'
        IPy.getpath('Save..', filt, 'save', para)
        self.canvas.save(para['path'])

    def on_closing(self, event):
        PlotManager.remove(self.GetTitle())
        event.Skip()

if __name__ == '__main__':
    app = wx.App(False)
    xs = np.linspace(10,20,50)
    ys = np.sin(xs)+100

    plotframe =  PlotFrame.get_frame('first', 'Histogram', 'Line length', 'value of pix')
    plotframe.add_data(xs, ys, (0,0,255), 1)
    plotframe.draw()
    plotframe.draw()
    app.MainLoop()