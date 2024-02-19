from ..widgets import HistPanel, CMapPanel, FloatSlider, CMapSelCtrl
import wx, numpy as np
from sciapp import Source

class Histogram( wx.Panel ):
	title = 'Histogram Widget'

	def __init__( self, parent, app):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 255,0 ), style = wx.TAB_TRAVERSAL )
		self.app = app
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.histpan = HistPanel(self)
		bSizer1.Add(self.histpan, 0, wx.ALL|wx.EXPAND, 5 )

		self.sli_high = FloatSlider(self, (0,255), 0, '')
		self.sli_high.SetValue(255)
		bSizer1.Add( self.sli_high, 0, wx.ALL|wx.EXPAND, 0 )
		
		self.sli_low = FloatSlider(self, (0,255), 0, '')
		self.sli_low.SetValue(0)
		bSizer1.Add( self.sli_low, 0, wx.ALL|wx.EXPAND, 0 )
		
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		self.btn_8bit = wx.Button( self, wx.ID_ANY, u"0-255", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_8bit.SetMaxSize( wx.Size( -1,40 ) )
		
		bSizer2.Add( self.btn_8bit, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_minmax = wx.Button( self, wx.ID_ANY, u"min-max", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_minmax.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_minmax, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_slice = wx.Button( self, wx.ID_ANY, u"slice", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_slice.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_slice, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_stack = wx.Button( self, wx.ID_ANY, u"stack", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_stack.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_stack, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND |wx.ALL, 5 )

		self.cmapsel = CMapSelCtrl(self)
		
		bSizer1.Add(self.cmapsel, 0, wx.ALL|wx.EXPAND, 5 )

		self.cmap = CMapPanel(self)
		bSizer1.Add(self.cmap, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.sli_high.Bind( wx.EVT_SCROLL, self.on_low )
		self.sli_low.Bind( wx.EVT_SCROLL, self.on_high )
		self.btn_8bit.Bind( wx.EVT_BUTTON, self.on_8bit )
		self.btn_minmax.Bind( wx.EVT_BUTTON, self.on_minmax )
		self.btn_slice.Bind( wx.EVT_BUTTON, self.on_slice )
		self.btn_stack.Bind( wx.EVT_BUTTON, self.on_stack )
		self.cmap.set_handle(self.on_cmap)
		self.cmapsel.Bind(wx.EVT_COMBOBOX,  self.on_cmapsel)
		self.range = (0, 255)
	
	def on_cmap(self):
		ips = self.app.get_img()
		if ips is None: return
		cmap = CMapPanel.linear_color(self.cmap.GetValue())
		ips.lut = cmap
		ips.update()

	def on_cmapsel(self, event):
		ips = self.app.get_img()
		if ips is None: return
		key = self.cmapsel.GetSelection()
		ips.lut = self.cmapsel.vs[key]
		ips.update()
	
	# Virtual event handlers, overide them in your derived class
	def on_low( self, event ):
		ips = self.app.get_img()
		if ips is None: return
		if self.sli_high.GetValue()<self.sli_low.GetValue():
			self.sli_high.SetValue(self.sli_low.GetValue())
		ips.range = (self.sli_low.GetValue(), self.sli_high.GetValue())
		ips.chan_rg = ips.range
		lim1 = 1.0 * (self.sli_low.GetValue() - self.range[0])/(self.range[1]-self.range[0])
		lim2 = 1.0 * (self.sli_high.GetValue() - self.range[0])/(self.range[1]-self.range[0])
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update()
	
	def on_high( self, event ):
		ips = self.app.get_img()
		if ips is None: return
		if self.sli_low.GetValue()>self.sli_high.GetValue():
			self.sli_low.SetValue(self.sli_high.GetValue())
		ips.range = (self.sli_low.GetValue(), self.sli_high.GetValue())
		ips.chan_rg = ips.range
		lim1 = 1.0 * (self.sli_low.GetValue() - self.range[0])/(self.range[1]-self.range[0])
		lim2 = 1.0 * (self.sli_high.GetValue() - self.range[0])/(self.range[1]-self.range[0])
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update()
	
	def on_8bit( self, event ):
		ips = self.app.get_img()
		if ips is None: return
		self.range = ips.range = (0,255)
		hist = ips.histogram(step=1024)
		self.histpan.SetValue(hist)
		self.sli_low.set_para((0,255), 0)
		self.sli_high.set_para((0,255), 0)
		self.sli_low.SetValue(0)
		self.sli_high.SetValue(255)
		self.histpan.set_lim(0,255)
		ips.update()
	
	def on_minmax( self, event ):
		ips = self.app.get_img()
		if ips is None: return
		minv, maxv = ips.get_updown()[0]
		self.range = ips.range = (minv, maxv)
		hist = ips.histogram(step=1024)
		self.histpan.SetValue(hist)
		self.sli_low.set_para(self.range, 10)
		self.sli_high.set_para(self.range, 10)
		self.sli_low.SetValue(minv)
		self.sli_high.SetValue(maxv)
		self.histpan.set_lim(0,255)
		ips.update()
	
	def on_slice( self, event ):
		ips = self.app.get_img()
		if ips is None: return
		hist = ips.histogram(step=1024)
		self.histpan.SetValue(hist)
	
	def on_stack( self, event ):
		ips = self.app.get_img()
		if ips is None: return
		hists = ips.histogram(slices='all', chans='all', step=512)
		self.histpan.SetValue(hists)