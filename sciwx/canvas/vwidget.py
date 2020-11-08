import wx, wx.lib.agw.aui as aui
from .mcanvas import SCanvas as Canvas
from ..widgets import ToolBar, MenuBar
from sciapp import App

class VectorFrame(wx.Frame, App):
    def __init__(self, parent=None, autofit=False):
        App.__init__(self)
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = 'VectorFrame',
                            pos = wx.DefaultPosition,
                            size = wx.Size( 800, 600 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas =Canvas(self, autofit=autofit)
        sizer.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(sizer)
        self.set_shp = self.canvas.set_shp
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_ACTIVATE, self.on_valid)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_idle(self, event):
        if self.GetTitle()!=self.canvas.shape.name:
            self.SetTitle(self.canvas.shape.name)

    def set_title(self, title): self.SetTitle(title)

    def on_valid(self, event): pass

    def on_close(self, event): 
        event.Skip()

    def add_toolbar(self):
        toolbar = ToolBar(self)
        self.GetSizer().Insert(0, toolbar, 0, wx.EXPAND | wx.ALL, 0)
        return toolbar

    def add_menubar(self):
        menubar = MenuBar()
        self.SetMenuBar(menubar)
        return menubar

class VectorNoteBook(wx.lib.agw.aui.AuiNotebook):
    def __init__(self, parent):
        wx.lib.agw.aui.AuiNotebook.__init__( self, parent, wx.ID_ANY, 
            wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE )
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_valid) 
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.Bind( wx.EVT_IDLE, self.on_idle)
        self.SetArtProvider(aui.AuiSimpleTabArt())
        
    def on_idle(self, event):
        for i in range(self.GetPageCount()):
            title = self.GetPage(i).shape.name
            if self.GetPageText(i) != title:
                self.SetPageText(i, title)

    def canvas(self, i=None):
        if not i is None: return self.GetPage(i)
        else: return self.GetCurrentPage()
        
    def set_background(self, img):
        self.GetAuiManager().SetArtProvider(ImgArtProvider(img))

    def add_canvas(self, vcanvas=None):
        if vcanvas is None: vcanvas = Canvas(self)
        self.AddPage(vcanvas, 'Vector', True, wx.NullBitmap )
        return vcanvas

    def set_title(self, panel, title):
        self.SetPageText(self.GetPageIndex(panel), title)

    def on_valid(self, event): pass

    def on_close(self, event): pass

class VectorNoteFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = 'VectorNoteFrame',
                            pos = wx.DefaultPosition,
                            size = wx.Size( 800, 600 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = VectorNoteBook(self)
        self.canvas = self.notebook.canvas
        sizer.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 0 )
        self.SetSizer(sizer)
        self.add_canvas = self.notebook.add_canvas
        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def add_toolbar(self):
        toolbar = ToolBar(self)
        self.GetSizer().Insert(0, toolbar, 0, wx.EXPAND | wx.ALL, 0)
        return toolbar 

    def add_menubar(self):
        menubar = MenuBar()
        self.SetMenuBar(menubar)
        return menubar
        
    def on_close(self, event):
        while self.notebook.GetPageCount()>0:
            self.notebook.DeletePage(0)
        event.Skip()
    
if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    
    app = wx.App()
    cf = CanvasFrame(None, autofit=False)
    cf.set_imgs([astronaut(), 255-astronaut()])
    cf.set_cn(0)
    cf.Show()
    app.MainLoop()
    
    '''
    app = wx.App()
    cnf = CanvasNoteFrame(None)
    canvas = cnf.add_img()
    canvas.set_img(camera())

    canvas = cnf.add_img()
    canvas.set_img(camera())
    canvas.set_cn(0)
    
    cnf.Show()
    app.MainLoop()
    '''
