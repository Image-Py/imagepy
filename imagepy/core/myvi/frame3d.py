import wx, os
from .canvas3d import Canvas3D
from . import util
from . import canvas3d
import numpy as np

class Frame3D(wx.Frame):
	frms = {}

	def __init__(self, parent, title='Frame3D', manager=None):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		sizer = wx.BoxSizer( wx.VERTICAL )
		root = os.path.abspath(os.path.dirname(__file__))

		self.SetIcon(wx.Icon(os.path.join(root, 'imgs/logo.ico'), wx.BITMAP_TYPE_ICO))
		self.viewer = canvas3d.Viewer3D( self , manager)
		sizer.Add( self.viewer, 1, wx.EXPAND |wx.ALL, 0 )
		self.Bind(wx.EVT_CLOSE, self.on_closing)
		
		self.SetSizer( sizer )
		self.Layout()
		
		self.Centre( wx.BOTH )

	@classmethod
	def figure(cls, parent, title):
		if not title in cls.frms:
			cls.frms[title] = Frame3D(parent, title)
			cls.frms[title].Show()
		# wx.Yield()
		return cls.frms[title]
	
	def on_closing(self, event):
		if self.GetTitle() in Frame3D.frms:
			Frame3D.frms.pop(self.GetTitle())
		event.Skip()

if __name__ == '__main__':
    app = wx.App(False)
    frm = Frame3D(None, title='GLCanvas Sample')
    frm.Show()
    app.MainLoop()
