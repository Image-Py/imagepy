import wx
from imagepy.core.manager import WidgetsManager
from imagepy.menus.Plugins.Macros.recorder_wgt import Plugin as recorder
from imagepy.menus.Plugins.Manager.console_wgt import Plugin as console
from imagepy.menus.Plugins.Manager.plglist_wgt import Plugin as plglist
from imagepy.menus.Plugins.Manager.plgtree_wgt import Plugin as plgtree
from imagepy.menus.Plugins.Manager.toltree_wgt import Plugin as toltree

class DevelopToolSute ( wx.Panel ):
	title = 'Develop Tool Sute'
	single = True
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 808,300 ), style = wx.TAB_TRAVERSAL )
		
		sizer = wx.BoxSizer( wx.VERTICAL )
		
		mrecorder = recorder(self)
		self.notebook = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )
		self.notebook.AddPage( mrecorder, mrecorder.title, True, wx.NullBitmap )
		self.notebook.AddPage( console(self), console.title, False, wx.NullBitmap )
		self.notebook.AddPage( plglist(self), plglist.title, False, wx.NullBitmap )
		self.notebook.AddPage( plgtree(self), plgtree.title, False, wx.NullBitmap )
		self.notebook.AddPage( toltree(self), toltree.title, False, wx.NullBitmap )
		WidgetsManager.addref(mrecorder)
		sizer.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 0 )
		self.SetSizer( sizer )
		self.Fit()
		self.Layout()
		
wgts = [recorder, console, plglist, plgtree, toltree, '-', DevelopToolSute]