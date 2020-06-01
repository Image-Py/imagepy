from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
from matplotlib.figure import Figure

import wx, wx.lib.agw.aui as aui
import numpy as np

class PlotCanvas(FigureCanvas):
    def __init__(self, parent, id=-1, fig=None, title='Plot'):
        self.figure = fig or Figure()
        self.title = title
        FigureCanvas.__init__(self, parent, id, self.figure)

    def add_subplot(self, n=111, **key):
        return self.figure.add_subplot(n, **key)
        
class PlotFrame(wx.Frame):
    def __init__(self, parent, toolbar=True):
        wx.Frame.__init__(self, parent, -1,
                          'CanvasFrame', size=(550, 350))
        self.figure = PlotCanvas(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.figure, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()
        self.add_subplot = self.figure.add_subplot
        if toolbar: self.add_toolbar()
        self.Bind(wx.EVT_IDLE, self.on_idle)

    def on_idle(self, event):
        if self.GetTitle()!=self.figure.title:
            self.SetTitle(self.figure.title)

    def add_toolbar(self):
        self.toolbar = NavigationToolbar(self.figure)
        self.toolbar.Realize()
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.toolbar.update()

class PlotNoteBook(wx.lib.agw.aui.AuiNotebook):
    def __init__(self, parent):
        wx.lib.agw.aui.AuiNotebook.__init__( self, parent, wx.ID_ANY, 
            wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE )
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_valid) 
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.Bind( wx.EVT_IDLE, self.on_idle)
        self.SetArtProvider(aui.AuiSimpleTabArt())
        
    def on_idle(self, event):
        for i in range(self.GetPageCount()):
            title = self.GetPage(i).title
            if self.GetPageText(i) != title:
                self.SetPageText(i, title)

    def figure(self, i=None):
        if not i is None: return self.GetPage(i)
        else: return self.GetCurrentPage()
        
    def set_background(self, img):
        self.GetAuiManager().SetArtProvider(ImgArtProvider(img))

    def add_figure(self, figure=None):
        if figure is None: figure = PlotCanvas(self)
        self.AddPage(figure, 'Figure', True, wx.NullBitmap )
        return figure

    def set_title(self, panel, title):
        self.SetPageText(self.GetPageIndex(panel), title)

    def on_valid(self, event): pass

    def on_close(self, event): pass

    def mpl_connect(self, evt, method):
        if self.figure() is None: return
        self.figure().mpl_connect(
            'motion_notify_event', self.mouse_move)        

class PlotNoteFrame(wx.Frame):
    def __init__(self, parent, toolbar=True):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = 'CanvasNoteFrame',
                            pos = wx.DefaultPosition,
                            size = wx.Size( 800, 600 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = PlotNoteBook(self)
        self.figure = self.notebook.figure
        sizer.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 0 )
        self.SetSizer(sizer)
        self.add_figure = self.notebook.add_figure
        #if toolbar: self.add_toolbar()
        self.Layout()

    def add_toolbar(self):
        self.toolbar = NavigationToolbar(self.notebook)
        self.toolbar.Realize()
        self.GetSizer().Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.toolbar.update()
    
if __name__ == '__main__':
    app = wx.App()
    pframe = PlotFrame(None)
    ax = pframe.add_subplot()
    x = np.linspace(0,10,100)
    y = np.sin(x)
    ax.plot(x, y)
    ax.grid()
    ax.set_title('abc')
    pframe.Show()
    app.MainLoop()

