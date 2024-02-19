from ..widgets import ViewPort as ViewPortCtrl
import wx, numpy as np

class ViewPort ( wx.Panel ):
	title = 'Navigator'
	scales = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 8, 10, 15, 20, 30, 50]
	def __init__( self, parent , app):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 255,200 ), style = wx.TAB_TRAVERSAL )
		
		self.app = app
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.viewport = ViewPortCtrl( self)
		bSizer3.Add( self.viewport, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.slider = wx.Slider( self, wx.ID_ANY, 6, 0, len(self.scales), wx.DefaultPosition, wx.DefaultSize, wx.SL_LEFT|wx.SL_VERTICAL|wx.SL_SELRANGE|wx.SL_INVERSE )
		bSizer3.Add( self.slider, 0, wx.RIGHT|wx.EXPAND, 5 )
		
		
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

		self.slider.Bind( wx.EVT_SCROLL, self.on_zoom )
		self.btn_apply.Bind( wx.EVT_BUTTON, self.on_apply )
		self.btn_fit.Bind( wx.EVT_BUTTON, self.on_fit )
		self.btn_one.Bind( wx.EVT_BUTTON, self.on_one )
		self.viewport.Bind('View_EVT', self.on_handle)
	
	def on_apply(self, event):
		win = self.app.get_img_win()
		if win is None: return
		image = win.image
		step = max(max(image.shape[:2])//300,1)
		self.viewport.set_img(image.lookup(image.img[::step,::step]), image.shape)
		self.viewport.set_box(win.canvas.conbox, win.canvas.winbox)

	def on_zoom(self, event):
		self.on_apply(event)
		k = self.scales[self.slider.GetValue()]
		self.label.SetLabel('%.2f%%'%(k*100))
		win = self.app.get_img_win()
		if win is None: return
		a,b,c,d = win.canvas.winbox
		win.canvas.scaidx = self.slider.GetValue()
		win.canvas.zoom(k, (a+c)/2, (b+d)/2)
		win.image.update()
		self.viewport.set_box(win.canvas.conbox, win.canvas.winbox)

	def on_fit(self, event):
		self.on_apply(event)
		win = self.app.get_img_win()
		if win is None: return
		win.canvas.fit()
		win.image.update()
		self.slider.SetValue(win.canvas.scaidx)
		k = self.scales[self.slider.GetValue()]
		self.label.SetLabel('%.2f%%'%(k*100))
		self.viewport.set_box(win.canvas.conbox, win.canvas.winbox)

	def on_one(self, event):
		self.on_apply(event)
		win = self.app.get_img_win()
		if win is None: return
		a,b,c,d = win.canvas.winbox
		win.canvas.scaidx = self.scales.index(1)
		win.canvas.zoom(1, (a+c)/2, (b+d)/2)
		win.image.update()
		self.slider.SetValue(win.canvas.scaidx)
		self.label.SetLabel('%.2f%%'%100)
		self.viewport.set_box(win.canvas.conbox, win.canvas.winbox)

	def on_handle(self, loc, update=False):
		if update: self.on_apply(update)
		win = self.app.get_img_win()
		if win is None: return
		win.canvas.center(*loc, 'data')
		win.image.update()
		self.viewport.set_box(win.canvas.conbox, win.canvas.winbox)