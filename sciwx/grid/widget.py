import wx, wx.lib.agw.aui as aui
from .grid import Grid

class MGrid(wx.Panel):
    def __init__(self, parent=None, autofit=False):
        wx.Frame.__init__ ( self, parent)
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.lab_info = wx.StaticText( self, wx.ID_ANY,
            'information', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_info.Wrap( -1 )
        self.Bind(wx.EVT_IDLE, self.on_idle)
        sizer.Add( self.lab_info, 0, wx.EXPAND, 0 )
        
        self.grid = Grid(self)
        sizer.Add( self.grid, 1, wx.EXPAND |wx.ALL, 0 )
        self.SetSizer(sizer)
        self.select = self.grid.select
        self.set_data = self.grid.set_data

    @property
    def table(self): return self.grid.table

    @property
    def name(self): return self.grid.table.name

    def on_idle(self, event):
        if self.table.data is None: return
        if self.lab_info.GetLabel() != self.table.info:
            self.lab_info.SetLabel(self.table.info)

class GridFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = 'GridFrame',
                            pos = wx.DefaultPosition,
                            size = wx.Size( 800, 600 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = MGrid(self)
        sizer.Add(self.grid, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(sizer)
        self.set_data = self.grid.set_data
        self.Bind(wx.EVT_IDLE, self.on_idle)

    def on_idle(self, event):
        if self.GetTitle()!=self.grid.table.name:
            self.SetTitle(self.grid.table.name)
    
    def set_title(self, tab): self.SetTitle(tab.name)

    def on_valid(self, event): event.Skip()

    def on_close(self, event): event.Skip()

    def Show(self):
        self.Fit()
        wx.Frame.Show(self)
    
class GridNoteBook(wx.lib.agw.aui.AuiNotebook):
    def __init__(self, parent):
        wx.lib.agw.aui.AuiNotebook.__init__( self, parent, wx.ID_ANY, 
            wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE )
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_valid) 
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.Bind( wx.EVT_IDLE, self.on_idle)
        self.SetArtProvider(aui.AuiSimpleTabArt())
        
    def on_idle(self, event):
        for i in range(self.GetPageCount()):
            title = self.GetPage(i).table.title
            if self.GetPageText(i) != title:
                self.SetPageText(i, title)

    def grid(self, i=None):
        if not i is None: return self.GetPage(i)
        else: return self.GetCurrentPage()
        
    def set_background(self, img):
        self.GetAuiManager().SetArtProvider(ImgArtProvider(img))

    def add_grid(self, grid=None):
        if grid is None: grid = MGrid(self)
        self.AddPage(grid, 'Image', True, wx.NullBitmap )
        return grid

    def set_title(self, panel, title):
        self.SetPageText(self.GetPageIndex(panel), title)

    def on_valid(self, event): pass

    def on_close(self, event): pass

class GridNoteFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = 'CanvasNoteFrame',
                            pos = wx.DefaultPosition,
                            size = wx.Size( 800, 600 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = GridNoteBook(self)
        self.grid = self.notebook.grid
        sizer.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 0 )
        self.SetSizer(sizer)
        self.add_grid = self.notebook.add_grid
        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def add_toolbar(self):
        toolbar = ToolBar(self)
        self.GetSizer().Insert(0, toolbar, 0, wx.EXPAND | wx.ALL, 0)
        return toolbar 

    def on_close(self, event):
        while self.notebook.GetPageCount()>0:
            self.notebook.DeletePage(0)
        event.Skip()

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    df = pd.DataFrame(np.arange(100).reshape((20,5)))
    app = wx.App()
    cf = GridFrame(None)
    cf.set_data(df)
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
