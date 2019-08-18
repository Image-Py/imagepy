from .tablewindow import *
#import aui as aui
import wx.lib.agw.aui as aui

class TablePanel ( wx.Panel ):
    def __init__( self, parent):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 819,488 ), style = wx.TAB_TRAVERSAL )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        WTableManager.add(self)

        bSizer = wx.BoxSizer( wx.VERTICAL )

        self.lab_info = wx.StaticText( self, wx.ID_ANY, 'MyLabel asdfasfa ', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_info.Wrap( -1 )
        bSizer.Add( self.lab_info, 0, wx.ALL|wx.EXPAND, 0 )
        self.grid = GridBase( self)
        self.grid.set_handler(self.set_info)
        bSizer.Add( self.grid, 1, wx.ALL|wx.EXPAND, 0 )
        

        self.SetSizer( bSizer )
        self.Layout()

        self.handle = None
    
    def set_handler(self, handle=None):
        self.handle = handle

    def set_tps(self, tps):
        self.tps = tps
        self.grid.set_tps(tps)

    def __del__( self ):
        print('Table Panel Del')
    
    def set_info(self, tps):
        self.lab_info.SetLabel('%sx%s; %.2fK'%(tps.data.shape+(tps.get_nbytes()/1024.0,)))
        if not self.handle is None: self.handle(tps)

class TableFrame(wx.Frame):
	"""CanvasFrame: derived from the wx.core.Frame"""
	## TODO: Main frame ???
	def __init__(self, parent=None):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
			title = wx.EmptyString,
			pos = wx.DefaultPosition,
			size = wx.Size( -1,-1 ),
			style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.tablepanel = TablePanel(self)
		logopath = os.path.join(root_dir, 'data/logo.ico')
		self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
		self.Bind(wx.EVT_ACTIVATE, self.on_valid)
		#self.SetAcceleratorTable(IPy.curapp.shortcut)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.tablepanel.set_handler(self.set_title)
		#self.canvaspanel.set_handler(self.set_title)

	def set_tps(self, tps):
		self.tablepanel.set_tps(tps)

	def set_title(self, tps):
		self.SetTitle(tps.title)

	def on_valid(self, event):
		if event.GetActive():
			TableManager.add(self.tablepanel.tps)

	def on_close(self, event):
		self.tablepanel.set_handler()
		self.tablepanel.grid.set_handler()
		WTableManager.remove(self.tablepanel)
		event.Skip()

class TableNoteBook(aui.AuiNotebook):
	def __init__(self, parent):
		aui.AuiNotebook.__init__( self, parent, wx.ID_ANY, 
			wx.DefaultPosition, wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE )
		self.Bind( aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_pagevalid) 
		self.Bind( aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)

	def add_page(self, panel, tps):
		self.AddPage(panel, tps.title, True, wx.NullBitmap )
		panel.set_handler(lambda tps, pan=panel: self.set_title(tps, pan))

	def set_title(self, tps, panel):
		title = tps.title
		self.SetPageText(self.GetPageIndex(panel), title)

	def on_pagevalid(self, event):
		TableManager.add(event.GetEventObject().GetPage(event.GetSelection()).tps)

	def on_close(self, event):
		event.GetEventObject().GetPage(event.GetSelection()).set_handler()
		event.GetEventObject().GetPage(event.GetSelection()).grid.set_handler()
		WTableManager.remove(event.GetEventObject().GetPage(event.GetSelection()))