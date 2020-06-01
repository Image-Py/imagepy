from ..widgets import CurvePanel
import numpy as np, wx

class Curve(wx.Panel):
	title = 'Curve Adjust'
	def __init__(self, parent, app):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 255,0 ), style = wx.TAB_TRAVERSAL )
		
		self.app = app
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.curvepan = CurvePanel(self, l=240)
		bSizer1.Add(self.curvepan, 0, wx.ALL|wx.EXPAND, 0 )

		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		self.btn_apply = wx.Button( self, wx.ID_ANY, u"apply", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_apply.SetMaxSize( wx.Size( -1,40 ) )
		
		bSizer2.Add( self.btn_apply, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_clear = wx.Button( self, wx.ID_ANY, u"clear", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_clear.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_clear, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_reset = wx.Button( self, wx.ID_ANY, u"reset", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_reset.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_reset, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_invert = wx.Button( self, wx.ID_ANY, u"invert", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_invert.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_invert, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()

		self.curvepan.Bind(None, self.handle)
		self.btn_apply.Bind( wx.EVT_BUTTON, self.on_apply )
		self.btn_clear.Bind( wx.EVT_BUTTON, self.on_clear )
		self.btn_reset.Bind( wx.EVT_BUTTON, self.on_reset )
		self.btn_invert.Bind( wx.EVT_BUTTON, self.on_invert )

	def handle(self, event):
		ips = self.app.get_img()
		if ips is None:return
		lut = CurvePanel.lookup(self.curvepan.pts)
		lut = np.vstack((lut,lut,lut)).T
		ips.lut = lut
		ips.update()

	def on_apply(self, event):
		ips = self.app.get_img()
		if ips is None:return
		hist = ips.histogram()
		self.curvepan.set_hist(hist)
		self.handle(None)

	def on_clear(self, event):
		ips = self.app.get_img()
		if ips is None:return
		hist = ips.histogram()
		self.curvepan.set_hist(hist)
		ips.lut =  np.arange(256*3, dtype=np.uint8).reshape((3,-1)).T
		ips.update()

	def on_reset(self, event):
		self.curvepan.SetValue()
		ips = self.app.get_img()
		if ips is None:return
		hist = ips.histogram()
		self.curvepan.set_hist(hist)
		self.handle(None)

	def on_invert(self, event):
		self.curvepan.SetValue([(0,255),(255,0)])
		ips = self.app.get_img()
		if ips is None:return
		hist = ips.histogram()
		self.curvepan.set_hist(hist)
		self.handle(None)