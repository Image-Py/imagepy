from ...ui.widgets import ViewPort
from imagepy import IPy
import numpy as np
import wx

class Plugin ( wx.Panel ):
	title = 'Navigator'
	scales = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 8, 10]
	def __init__( self, parent ):
		

		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 255,200 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.viewport = ViewPort( self)
		bSizer3.Add( self.viewport, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.slider = wx.Slider( self, wx.ID_ANY, 6, 0, 13, wx.DefaultPosition, wx.DefaultSize, wx.SL_LEFT|wx.SL_VERTICAL )
		bSizer3.Add( self.slider, 0, wx.ALL|wx.EXPAND, 0 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_apply = wx.Button( self, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.btn_apply.SetMaxSize( wx.Size( -1,40 ) )
		
		bSizer2.Add( self.btn_apply, 0, wx.ALL, 5 )

		self.btn_fit = wx.Button( self, wx.ID_ANY, u"Fit", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.btn_fit.SetMaxSize( wx.Size( -1,40 ) )
		
		bSizer2.Add( self.btn_fit, 0, wx.ALL, 5 )
		
		self.btn_one = wx.Button( self, wx.ID_ANY, u"Normal", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.btn_one.SetMaxSize( wx.Size( -1,40 ) )
		
		bSizer2.Add( self.btn_one, 0, wx.ALL, 5 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.label = wx.StaticText( self, wx.ID_ANY, u" 100.00%", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label.Wrap( -1 )
		bSizer2.Add( self.label, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()

		self.slider.Bind( wx.EVT_SCROLL_CHANGED, self.on_zoom )
		self.btn_apply.Bind( wx.EVT_BUTTON, self.on_apply )
		self.btn_fit.Bind( wx.EVT_BUTTON, self.on_fit )
		self.btn_one.Bind( wx.EVT_BUTTON, self.on_one )
		self.viewport.set_handle(self.on_handle)
	
	def on_apply(self, event):
		win = IPy.get_window()
		if win is None: return
		img = win.canvas.ips.img
		step = max(max(img.shape[:2])//300,1)
		self.viewport.set_img(win.canvas.ips.lookup(img[::step,::step]), img.shape)
		self.viewport.set_box(win.canvas.imgbox, win.canvas.box)

	def on_zoom(self, event):
		k = self.scales[self.slider.GetValue()]
		self.label.SetLabel('%.2f%%'%(k*100))
		win = IPy.get_window()
		if win is None: return
		a,b,c,d = win.canvas.box
		x, y = win.canvas.to_data_coor(c/2, d/2)
		win.canvas.scaleidx = self.slider.GetValue()
		win.canvas.zoom(k, x, y)
		win.canvas.ips.update = 'pix'
		self.viewport.set_box(win.canvas.imgbox, win.canvas.box)

	def on_fit(self, event):
		win = IPy.get_window()
		if win is None: return
		win.canvas.self_fit()
		win.canvas.ips.update = 'pix'
		self.slider.SetValue(win.canvas.scaleidx)
		k = self.scales[self.slider.GetValue()]
		self.label.SetLabel('%.2f%%'%(k*100))
		self.viewport.set_box(win.canvas.imgbox, win.canvas.box)

	def on_one(self, event):
		win = IPy.get_window()
		if win is None: return
		a,b,c,d = win.canvas.box
		x, y = win.canvas.to_data_coor(c/2, d/2)
		win.canvas.scaleidx = self.scales.index(1)
		win.canvas.zoom(1, x, y)
		win.canvas.ips.update = 'pix'
		self.slider.SetValue(win.canvas.scaleidx)
		self.label.SetLabel('%.2f%%'%100)
		self.viewport.set_box(win.canvas.imgbox, win.canvas.box)

	def on_handle(self):
		win = IPy.get_window()
		if win is None: return
		x, y = self.viewport.GetValue()
		print(x, y)
		win.canvas.center(x, y)
		win.canvas.ips.update = 'pix'
		self.viewport.set_box(win.canvas.imgbox, win.canvas.box)